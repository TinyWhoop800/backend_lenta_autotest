from config.apps import APPS_LENTA
from api.requests.collections.get_collections import get_collections_raw
from assertions.response_validator import check_status, check_schema
from models.collections_model.get_collections_model import GetCollectionsModel
from clients.api_client import APIClient
from config.settings import settings
from dataclasses import dataclass
import pytest
import logging

logger = logging.getLogger(__name__)

_collections_test_data = {}


@dataclass
class CollectionTestParams:
    """Параметры для одного теста collections"""
    collection_id: str
    app_config: dict


@dataclass
class PreparedApiClient:
    """Полностью подготовленный клиент для теста"""
    client: APIClient
    token: str
    app_config: dict
    collection_id: str


def _load_collections_data():
    """Загружает collections данные ДО всех тестов"""
    global _collections_test_data

    if _collections_test_data:
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
            resp = get_collections_raw(temp_client)
            check_status(resp, 200)
            validated = check_schema(resp.json(), GetCollectionsModel)
            collection_ids = [collection.id for collection in validated.data]

            _collections_test_data[key] = {
                "app": app,
                "collection_ids": collection_ids
            }
            logger.info(f"✓ Loaded {len(collection_ids)} collections for {key}")
        except Exception as e:
            logger.error(f"ERROR loading collections for {key}: {e}")
        finally:
            temp_client.close()


def pytest_configure(config):
    """Вызывается САМЫМ ПЕРВЫМ перед collection"""
    _load_collections_data()


def pytest_generate_tests(metafunc):
    if "prepared_api_client_collections" not in metafunc.fixturenames:
        return

    argvalues = []

    for key, data in _collections_test_data.items():
        for collection_id in data["collection_ids"]:
            argvalues.append(
                pytest.param(
                    (collection_id, data["app"]),
                    id=f"{key}-{collection_id}"
                )
            )

    if argvalues:
        metafunc.parametrize("prepared_api_client_collections", argvalues, indirect=True)


@pytest.fixture
def prepared_api_client_collections(request, api_client_factory, session_tokens):
    """ГЛАВНЫЙ фикстур для тестов collections"""
    collection_id, app_config = request.param

    api_client = api_client_factory(app_config)
    key = f"{app_config['app_name']}_{app_config['platform']}"
    token = session_tokens[key]

    return PreparedApiClient(
        client=api_client,
        token=token,
        app_config=app_config,
        collection_id=collection_id
    )
