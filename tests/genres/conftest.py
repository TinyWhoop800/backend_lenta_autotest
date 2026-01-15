from config.apps import APPS_LENTA
from api.requests.genres.get_genres import get_genres_raw
from assertions.response_validator import check_status, check_schema
from models.genres_model.get_genres_model import GetGenresModel
from clients.api_client import APIClient
from config.settings import settings
from dataclasses import dataclass
import pytest
import logging

logger = logging.getLogger(__name__)

_genre_id_test_data = {}


@dataclass
class GenreIdTestParams:
    """Параметры для одного теста collections"""
    genre_id: str
    app_config: dict


@dataclass
class PreparedApiClient:
    """Полностью подготовленный клиент для теста"""
    client: APIClient
    token: str
    app_config: dict
    genre_id: str


def _load_genre_id_data():
    """Загружает collections данные ДО всех тестов"""
    global _genre_id_test_data

    if _genre_id_test_data:
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
            resp = get_genres_raw(temp_client)
            check_status(resp, 200)
            validated = check_schema(resp.json(), GetGenresModel)
            genre_ids = [genre_id.id for genre_id in validated.data]

            _genre_id_test_data[key] = {
                "app": app,
                "genre_ids": genre_ids
            }
        except Exception as e:
            logger.error(f"ERROR loading genre for {key}: {e}")
        finally:
            temp_client.close()


def pytest_configure(config):
    """Вызывается САМЫМ ПЕРВЫМ перед collection"""
    _load_genre_id_data()


def pytest_generate_tests(metafunc):
    if "prepared_api_client_genre_id" not in metafunc.fixturenames:
        return

    argvalues = []

    for key, data in _genre_id_test_data.items():
        for genre_id in data["genre_ids"]:
            argvalues.append(
                pytest.param(
                    (genre_id, data["app"]),
                    id=f"{key}-{genre_id}"
                )
            )

    if argvalues:
        metafunc.parametrize("prepared_api_client_genre_id", argvalues, indirect=True)


@pytest.fixture
def prepared_api_client_genre_id(request, api_client_factory, session_tokens):
    """ГЛАВНЫЙ фикстур для тестов collections"""
    genre_id, app_config = request.param

    api_client = api_client_factory(app_config)
    key = f"{app_config['app_name']}_{app_config['platform']}"
    token = session_tokens[key]

    return PreparedApiClient(
        client=api_client,
        token=token,
        app_config=app_config,
        genre_id=genre_id
    )
