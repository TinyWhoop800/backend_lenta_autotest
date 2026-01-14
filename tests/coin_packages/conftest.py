from config.apps import APPS_LENTA
from api.requests.coin_packages.get_coin_packages import get_coin_packages_raw
from assertions.response_validator import check_status, check_schema
from models.coin_packages_model.get_coin_packages_model import GetCoinPackagesModel
from clients.api_client import APIClient
from config.settings import settings
from dataclasses import dataclass
import pytest
import logging

logger = logging.getLogger(__name__)

_coin_test_data = {}


@dataclass
class CoinTestParams:
    """Параметры для одного теста coin_packages"""
    payment_type: str
    coin_id: str
    app_config: dict


@dataclass
class PreparedApiClient:
    """Полностью подготовленный клиент для теста"""
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

    logger.info("Loading coin packages data...")

    for app in APPS_LENTA:
        if "payment_types" not in app or not app["payment_types"]:
            continue

        key = f"{app['app_name']}_{app['platform']}"
        temp_client = APIClient(
            base_url=settings.BASE_URL,
            default_headers=app["headers"],
            retries=3,
            backoff_factor=0.3
        )

        try:
            resp = get_coin_packages_raw(temp_client)
            check_status(resp, 200)
            validated = check_schema(resp.json(), GetCoinPackagesModel)
            coin_ids = [pkg.id for pkg in validated.coinPackages]

            _coin_test_data[key] = {
                "app": app,
                "coin_ids": coin_ids,
                "payment_types": app["payment_types"]
            }
            logger.info(f"Loaded {len(coin_ids)} coin packages for {key}")
        except Exception as e:
            logger.error(f"ERROR loading coin data for {key}: {e}")
        finally:
            temp_client.close()


def pytest_configure(config):
    """Вызывается САМЫМ ПЕРВЫМ перед collection"""
    _load_coin_data()


def pytest_generate_tests(metafunc):
    """Генерирует параметры для тестов coin_packages"""
    if "coin_params" not in metafunc.fixturenames:
        return

    argvalues = []

    for key, data in _coin_test_data.items():
        for payment_type in data["payment_types"]:
            for coin_id in data["coin_ids"]:
                argvalues.append(
                    pytest.param(
                        CoinTestParams(
                            payment_type=payment_type,
                            coin_id=coin_id,
                            app_config=data["app"]
                        ),
                        id=f"{key}-{payment_type}-{coin_id[:8]}"
                    )
                )

    if argvalues:
        metafunc.parametrize("coin_params", argvalues)


@pytest.fixture
def coin_params(request):
    """Fixture для получения параметров теста"""
    return request.param


@pytest.fixture
def prepared_api_client(coin_params, api_client_factory, session_tokens):
    """ГЛАВНЫЙ фикстур для тестов coin_packages"""
    api_client = api_client_factory(coin_params.app_config)
    key = f"{coin_params.app_config['app_name']}_{coin_params.app_config['platform']}"
    token = session_tokens[key]

    return PreparedApiClient(
        client=api_client,
        token=token,
        app_config=coin_params.app_config,
        payment_type=coin_params.payment_type,
        coin_id=coin_params.coin_id
    )
