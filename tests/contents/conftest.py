from config.apps import APPS_LENTA
from api.requests.contents.get_content import get_content_raw
from assertions.response_validator import check_status, check_schema
from models.contents_models.get_contents_model import GetContentsModel
from clients.api_client import APIClient
from config.settings import settings
from api.requests.auth.post_guest_login import post_guest_login_raw
from api.requests.user.delete_user import delete_user_raw
from dataclasses import dataclass
import pytest
import logging

logger = logging.getLogger(__name__)

_collections_test_data = {}


@dataclass
class PreparedApiClientCollections:
    """
    Объект со всем необходимым для теста collections.

    Содержит клиент, токен и список collection_id для текущего приложения.
    """
    client: APIClient
    token: str
    app_config: dict
    collection_id: int


def _load_collections_data():
    """Загружает collections данные ДО всех тестов"""
    global _collections_test_data

    if _collections_test_data:
        return

    tokens = {}

    # Получаем токены для всех приложений
    for app in APPS_LENTA:
        key = f"{app['app_name']}_{app['platform']}"

        temp_client = APIClient(
            base_url=settings.BASE_URL,
            default_headers=app["headers"],
            retries=3,
            backoff_factor=0.3
        )

        try:
            login_response = post_guest_login_raw(temp_client)
            if login_response.status_code == 200:
                tokens[key] = login_response.json()["token"]
        finally:
            temp_client.close()

    # Собираем collection данные
    for app in APPS_LENTA:
        key = f"{app['app_name']}_{app['platform']}"
        token = tokens.get(key)
        if not token:
            continue

        temp_client = APIClient(
            base_url=settings.BASE_URL,
            default_headers=app["headers"],
            retries=3,
            backoff_factor=0.3
        )

        try:
            resp = get_collections_raw(temp_client, token)
            check_status(resp, 200)
            validated = check_schema(resp.json(), GetCollectionsModel)

            # Извлекаем collection_id из data массива
            collection_ids = [collection.id for collection in validated.data]

            _collections_test_data[key] = {
                "app": app,
                "collection_ids": collection_ids
            }
            logger.info(f"Loaded {len(collection_ids)} collections for {key}")
        except Exception as e:
            logger.error(f"ERROR loading collections for {key}: {e}")
        finally:
            temp_client.close()

    # Cleanup
    for app in APPS_LENTA:
        key = f"{app['app_name']}_{app['platform']}"
        token = tokens.get(key)
        if not token:
            continue

        temp_client = APIClient(
            base_url=settings.BASE_URL,
            default_headers=app["headers"],
            retries=3,
            backoff_factor=0.3
        )

        try:
            delete_user_raw(temp_client, token)
        except Exception as e:
            logger.warning(f"Failed to cleanup user {key}: {e}")
        finally:
            temp_client.close()


def pytest_configure(config):
    """Вызывается САМЫМ ПЕРВЫМ перед collection"""
    _load_collections_data()


def pytest_generate_tests(metafunc):
    """
    Генерирует параметры для тестов collections.

    Создаёт комбинации: collection_id × app_config
    """
    if "prepared_api_client_collections" not in metafunc.fixturenames:
        return

    argvalues = []
    ids = []

    for key, data in _collections_test_data.items():
        for collection_id in data["collection_ids"]:
            # Каждый параметр — полная информация для одного теста
            argvalues.append({
                "collection_id": collection_id,
                "app_config": data["app"]
            })
            ids.append(f"{key}-collection_{collection_id}")

    if argvalues:
        metafunc.parametrize(
            "prepared_api_client_collections",
            argvalues,
            ids=ids,
            indirect=True
        )


@pytest.fixture
def prepared_api_client_collections(request, api_client_factory, session_tokens):
    """
    Фикстур для тестов collections.

    Принимает параметры из pytest_generate_tests (через indirect=True),
    сам создаёт клиент, берёт токен, и возвращает готовый объект.
    """
    param = request.param
    app_config = param["app_config"]
    collection_id = param["collection_id"]

    # Создаём клиент с нужными headers
    api_client = api_client_factory(app_config)

    # Берём токен
    key = f"{app_config['app_name']}_{app_config['platform']}"
    token = session_tokens[key]

    # Возвращаем готовый объект
    return PreparedApiClientCollections(
        client=api_client,
        token=token,
        app_config=app_config,
        collection_id=collection_id
    )
