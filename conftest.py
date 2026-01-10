import pytest
import logging
from config.apps import APPS_LENTA
from clients.api_client import APIClient
from config.settings import settings
from api.requests.auth.post_guest_login import post_guest_login
from api.requests.user.delete_user import delete_user
from assertions.response_validator import check_status


logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def api_client():
    """Создать API клиент на сессию"""
    client = APIClient(
        base_url=settings.BASE_URL,
        retries=3,
        backoff_factor=0.3
    )
    logger.info(f"API Client initialized with base_url: {settings.BASE_URL}")
    yield client
    client.close()


@pytest.fixture(params=APPS_LENTA, ids=lambda app: f"{app['app_name']}_{app['platform']}")
def app_config(request):
    """Параметризированный фикстур со всеми app конфигами"""
    return request.param


@pytest.fixture(scope="session")
def session_tokens(api_client):
    """
    Получить токены для всех app_config и хранить их на сессию.

    В конце сессии удалить всех пользователей.
    """
    tokens = {}

    # Логин для каждого конфига
    for app_config in APPS_LENTA:
        key = f"{app_config['app_name']}_{app_config['platform']}"
        logger.info(f"Getting token for: {key}")

        login_response = post_guest_login(api_client, app_config)
        check_status(login_response, 200)

        token = login_response.json()["token"]
        tokens[key] = token
        logger.debug(f"Token obtained for {key} (length: {len(token)})")

    yield tokens

    # Cleanup: удалить всех пользователей
    logger.info("Cleaning up: deleting all test users")
    for app_config in APPS_LENTA:
        key = f"{app_config['app_name']}_{app_config['platform']}"
        try:
            delete_user(api_client, app_config, tokens[key])
            logger.info(f"User deleted: {key}")
        except Exception as e:
            logger.warning(f"Failed to delete user {key}: {e}")


@pytest.fixture
def app_token(app_config, session_tokens):
    """
    Токен для текущей app_config.

    Автоматически выбирает нужный токен из session_tokens
    на основе текущего параметризированного app_config.
    """
    key = f"{app_config['app_name']}_{app_config['platform']}"
    token = session_tokens[key]
    logger.debug(f"Using token for: {key}")
    return token
