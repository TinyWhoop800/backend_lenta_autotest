import pytest
from config.apps import APPS_LENTA
from clients.api_client import APIClient
from config.settings import settings
import allure
from api.requests.auth.post_guest_login import post_guest_login
from api.requests.user.delete_user import delete_user
from assertions.response_validator import check_status
from models.auth.post_guest_login import PostGuestLogin
from models.user.delete_user import DeleteUser

@pytest.fixture(scope="session")
def api_client():
    client = APIClient(settings.BASE_URL)
    yield client
    client.close()

@pytest.fixture(params=APPS_LENTA, ids=lambda app: f"{app['app_name']}_{app['platform']}")
def app_config(request):
    import time
    time.sleep(1)
    return request.param

@pytest.fixture(scope="session")
def session_tokens(api_client):
    tokens = {}
    for app_config in APPS_LENTA:
        login_response = post_guest_login(api_client, app_config)
        check_status(login_response, 200)
        tokens[f"{app_config['app_name']}_{app_config['platform']}"] = login_response.json()["token"]

    yield tokens
    for app_config in APPS_LENTA:
        token_key = f"{app_config['app_name']}_{app_config['platform']}"
        delete_user(api_client, app_config, tokens[token_key])

@pytest.fixture
def app_token(app_config, session_tokens):
    """Токен для текущей app_config"""
    key = f"{app_config['app_name']}_{app_config['platform']}"
    return session_tokens[key]

# @pytest.fixture(params=APPS_LENTA, ids=lambda app: f"{app['app_name']}_{app['platform']}")
# def app_config(request):
#     import time
#     time.sleep(1)
#     return request.param
#
#
# @pytest.fixture
# def authorized_token(app_config, api_client):
#     """Только авторизация БЕЗ cleanup"""
#     with allure.step("Получаем guest token"):
#         login_response = post_guest_login(api_client, app_config)
#         login_json = login_response.json()
#         check_status(login_response, 200)
#         token = login_json["token"]
#     yield token
#
# @pytest.fixture
# def guest_token(app_config, api_client):
#     with allure.step("Создаем аккаунт и получаем токен"):
#         login_response = post_guest_login(api_client, app_config)
#         login_json = login_response.json()
#         check_status(login_response, 200)
#         token = login_json["token"]
#     yield token
#     with allure.step("Удаляем аккаунт"):
#         delete_response = delete_user(api_client, app_config, token)
#         check_status(delete_response, 200)