from config.apps import APPS_LENTA
from api.requests.coin_packages.get_coin_packages import get_coin_packages_raw
from assertions.response_validator import check_status, check_schema
from models.coin_packages_model.get_coin_packages_model import GetCoinPackagesModel
from clients.api_client import APIClient
from config.settings import settings
from api.requests.auth.post_guest_login import post_guest_login_raw
from api.requests.user.delete_user import delete_user_raw
from dataclasses import dataclass
import pytest
import logging

logger = logging.getLogger(__name__)

_coin_test_data = {}


@dataclass
class PreparedApiClient:
    """
    Объект который содержит всё необходимое для теста.

    Это одно место, где мы инкапсулируем всю подготовку.
    """
    client: APIClient
    token: str
    app_config: dict
    payment_type: str
    coin_id: str


def _load_coin_data():
    """Загружает coin данные ДО всех тестов"""
    global _coin_test_data

    if _coin_test_data:
        return

    tokens = {}

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

    # Собираем coin данные
    for app in APPS_LENTA:
        if "payment_types" not in app or not app["payment_types"]:
            continue

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
            resp = get_coin_packages_raw(temp_client, token)
            check_status(resp, 200)
            validated = check_schema(resp.json(), GetCoinPackagesModel)
            coin_ids = [pkg.id for pkg in validated.coinPackages]

            _coin_test_data[key] = {
                "app": app,
                "coin_ids": coin_ids,
                "payment_types": app["payment_types"]
            }
        except Exception as e:
            logger.error(f"ERROR loading coin data for {key}: {e}")
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
    _load_coin_data()


def pytest_generate_tests(metafunc):
    """
    Генерирует параметры для тестов coin_packages.

    Создаёт комбинации: payment_type × coin_id × app_config
    """
    if "prepared_api_client" not in metafunc.fixturenames:
        return

    argvalues = []
    ids = []

    for key, data in _coin_test_data.items():
        for payment_type in data["payment_types"]:
            for coin_id in data["coin_ids"]:
                # Каждый параметр — полная информация для одного теста
                argvalues.append({
                    "payment_type": payment_type,
                    "coin_id": coin_id,
                    "app_config": data["app"]
                })
                ids.append(f"{key}-{payment_type}-{coin_id[:8]}")

    if argvalues:
        metafunc.parametrize(
            "prepared_api_client",
            argvalues,
            ids=ids,
            indirect=True
        )


@pytest.fixture
def prepared_api_client(request, api_client_factory, session_tokens):
    """
    ГЛАВНЫЙ фикстур для тестов coin_packages.

    Принимает параметры из pytest_generate_tests (через indirect=True),
    сам создаёт клиент, берёт токен, и возвращает готовый объект.
    """
    param = request.param
    app_config = param["app_config"]
    payment_type = param["payment_type"]
    coin_id = param["coin_id"]

    # Создаём клиент с нужными headers
    api_client = api_client_factory(app_config)

    # Берём токен
    key = f"{app_config['app_name']}_{app_config['platform']}"
    token = session_tokens[key]

    # Возвращаем готовый объект
    return PreparedApiClient(
        client=api_client,
        token=token,
        app_config=app_config,
        payment_type=payment_type,
        coin_id=coin_id
    )
