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
def api_client_factory():
    """
    Фабрика для создания API клиентов.
    """
    clients = {}

    def create_client(app_config):
        """Создать клиент для конкретной app_config"""
        key = f"{app_config['app_name']}_{app_config['platform']}"

        if key not in clients:
            client = APIClient(
                base_url=settings.BASE_URL,
                default_headers=app_config["headers"],
                retries=3,
                backoff_factor=0.3
            )
            clients[key] = client
            logger.info(f"Created API client for: {key}")

        return clients[key]

    yield create_client

    # Cleanup
    for key, client in clients.items():
        client.close()
        logger.info(f"Closed API client: {key}")


# ВАЖНО: app_config параметризирован ТОЛЬКО для тестов, которые его явно запрашивают
# Для тестов, которые получают параметры через pytest_generate_tests (как coin_packages),
# этот фикстур НЕ должен применяться автоматически
@pytest.fixture(params=APPS_LENTA, ids=lambda app: f"{app['app_name']}_{app['platform']}")
def app_config(request):
    """
    Параметризированный фикстур со всеми app конфигами.

    ВАЖНО: Используется ТОЛЬКО для тестов, которые:
    - Явно запрашивают app_config в сигнатуре
    - НЕ получают параметры через pytest_generate_tests

    Для coin_packages параметры идут через pytest_generate_tests,
    поэтому тесты там должны получать app_config через test_app_config параметр,
    а не через эту фикстуру.
    """
    return request.param


@pytest.fixture
def api_client(app_config, api_client_factory):
    """
    Клиент для текущей app_config.

    Зависит от app_config, поэтому тоже параметризируется по приложениям.
    """
    return api_client_factory(app_config)


@pytest.fixture(scope="session")
def session_tokens(api_client_factory):
    """
    Получить токены для всех app_config и хранить их на сессию.
    """
    tokens = {}

    for app_config in APPS_LENTA:
        key = f"{app_config['app_name']}_{app_config['platform']}"
        logger.info(f"Getting token for: {key}")

        client = api_client_factory(app_config)

        login_response = post_guest_login(client)
        check_status(login_response, 200)

        token = login_response.json()["token"]
        tokens[key] = token
        logger.debug(f"Token obtained for {key} (length: {len(token)})")

    yield tokens

    # Cleanup
    logger.info("Cleaning up: deleting all test users")
    for app_config in APPS_LENTA:
        key = f"{app_config['app_name']}_{app_config['platform']}"
        try:
            client = api_client_factory(app_config)
            delete_user(client, tokens[key])
            logger.info(f"User deleted: {key}")
        except Exception as e:
            logger.warning(f"Failed to delete user {key}: {e}")


@pytest.fixture
def app_token(app_config, session_tokens):
    """
    Токен для текущей app_config.

    Зависит от app_config, поэтому параметризируется вместе с ним.
    """
    key = f"{app_config['app_name']}_{app_config['platform']}"
    token = session_tokens[key]
    logger.debug(f"Using token for: {key}")
    return token
