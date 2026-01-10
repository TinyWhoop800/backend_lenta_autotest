from config.apps import APPS_LENTA
from api.requests.coin_packeges.get_coin_packages import get_coin_packages
from assertions.response_validator import check_status, check_schema
from models.coin_packeges_model.get_coin_packages_model import GetCoinPackagesModel
from clients.api_client import APIClient
from config.settings import settings
from api.requests.auth.post_guest_login import post_guest_login
from api.requests.user.delete_user import delete_user

_coin_test_data = {}


def _load_coin_data():
    """Загружает coin данные ДО всех тестов"""
    global _coin_test_data

    if _coin_test_data:
        return  # Уже загружено

    # Создаём временный API клиент для сбора данных
    temp_client = APIClient(
        base_url=settings.BASE_URL,
        retries=3,
        backoff_factor=0.3
    )

    try:
        # Получаем токены (используем функцию из глобального conftest)
        tokens = {}
        for app in APPS_LENTA:
            key = f"{app['app_name']}_{app['platform']}"
            login_response = post_guest_login(temp_client, app)
            if login_response.status_code == 200:
                tokens[key] = login_response.json()["token"]

        # Собираем coin данные
        for app in APPS_LENTA:
            if "payment_types" not in app or not app["payment_types"]:
                continue

            key = f"{app['app_name']}_{app['platform']}"
            token = tokens.get(key)
            if not token:
                continue

            try:
                resp = get_coin_packages(temp_client, app, token)
                check_status(resp, 200)
                validated = check_schema(resp.json(), GetCoinPackagesModel)
                coin_ids = [pkg.id for pkg in validated.coinPackages]

                _coin_test_data[key] = {
                    "app": app,
                    "coin_ids": coin_ids,
                    "payment_types": app["payment_types"]
                }
            except Exception as e:
                print(f"ERROR {key}: {e}")

        # Cleanup
        for app in APPS_LENTA:
            key = f"{app['app_name']}_{app['platform']}"
            try:
                if key in tokens:
                    delete_user(temp_client, app, tokens[key])
            except:
                pass

    finally:
        temp_client.close()


def pytest_configure(config):
    """Вызывается САМЫМ ПЕРВЫМ перед collection"""
    _load_coin_data()


def pytest_generate_tests(metafunc):
    """Генерирует параметры payment_type + coin_id"""
    if "payment_type" not in metafunc.fixturenames or "coin_id" not in metafunc.fixturenames:
        return

    argvalues = []
    ids = []

    for key, data in _coin_test_data.items():
        for payment_type in data["payment_types"]:
            for coin_id in data["coin_ids"]:
                argvalues.append((payment_type, coin_id, data["app"]))
                ids.append(f"{key}-{payment_type}-{coin_id[:8]}")

    if argvalues:
        metafunc.parametrize("payment_type,coin_id,test_app_config", argvalues, ids=ids)
