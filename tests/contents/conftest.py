"""
Содержит:
- Загрузка данных со всех страниц пагинации
- Параметризация тестов по content_id
- Подготовка клиентов
"""

from config.apps import APPS_LENTA
from api.requests.contents.get_content import get_content_raw
from assertions.response_validator import check_status, check_schema
from models.contents_models.get_contents_model import GetContentsModel
from clients.api_client import APIClient
from config.settings import settings
from dataclasses import dataclass
import pytest
import logging
import traceback

_contents_test_data = {}

@dataclass
class ContentTestParams:
    """Параметры для одного теста collections"""
    content_id: str
    app_config: dict


@dataclass
class PreparedApiClient:
    """Полностью подготовленный клиент для теста"""
    client: APIClient
    token: str
    app_config: dict
    content_id: str


def _load_contents_data():
    """
    Загружает contents данные ДО всех тестов.

    Обходит все страницы пагинации и собирает все content_id.
    """
    global _contents_test_data

    if _contents_test_data:
        return

    for app in APPS_LENTA:
        key = f"{app['app_name']}_{app['platform']}"

        temp_client = APIClient(
            base_url=settings.BASE_URL,
            default_headers=app["headers"],
            retries=3,
            backoff_factor=0.3
        )

        try:
            content_ids = []
            page = 1

            resp = get_content_raw(temp_client, page=page)
            check_status(resp, 200)

            resp_json = resp.json()
            validated = check_schema(resp_json, GetContentsModel)

            last_page = validated.meta.last_page

            page_content_ids = [content.id for content in validated.data]
            content_ids.extend(page_content_ids)

            # Собираем content_id со ВСЕХ ОСТАЛЬНЫХ страниц
            for page in range(2, last_page + 1):
                resp = get_content_raw(temp_client, page=page)
                check_status(resp, 200)
                validated = check_schema(resp.json(), GetContentsModel)

                page_content_ids = [content.id for content in validated.data]
                content_ids.extend(page_content_ids)

            _contents_test_data[key] = {
                "app": app,
                "content_ids": content_ids
            }

        except Exception as e:
            traceback.print_exc()
        finally:
            temp_client.close()


def pytest_configure(config):
    """Вызывается САМЫМ ПЕРВЫМ перед collection"""
    _load_contents_data()


def pytest_generate_tests(metafunc):
    """Генерирует параметры для тестов contents"""
    if "prepared_api_client_contents" not in metafunc.fixturenames:
        return

    argvalues = []

    for key, data in _contents_test_data.items():
        for content_id in data["content_ids"]:
            argvalues.append(
                pytest.param(
                    (content_id, data["app"]),
                    id=f"{key}-{content_id}"
                )
            )

    if argvalues:
        metafunc.parametrize("prepared_api_client_contents", argvalues, indirect=True)


@pytest.fixture
def prepared_api_client_contents(request, api_client_factory, session_tokens):
    """ГЛАВНЫЙ фикстур для тестов contents"""
    content_id, app_config = request.param

    api_client = api_client_factory(app_config)
    key = f"{app_config['app_name']}_{app_config['platform']}"
    token = session_tokens[key]

    return PreparedApiClient(
        client=api_client,
        token=token,
        app_config=app_config,
        content_id=content_id
    )
