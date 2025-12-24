import pytest
from config.apps import APPS_LENTA
from clients.api_client import APIClient
from config.settings import settings

@pytest.fixture(scope="session")
def api_client():
    client = APIClient(settings.BASE_URL)
    yield client
    client.close()

@pytest.fixture(params=APPS_LENTA, ids=lambda app: f"{app['app_name']}_{app['platform']}")
def app_config(request):
    """Фикстура, которая автоматически проходит по всем приложениям"""
    return request.param

@pytest.fixture
def locale(app_config):
    """Локаль из конфига приложения"""
    return app_config["available_locale"][0]

@pytest.fixture
def headers(app_config):
    """Заголовки для текущего приложения"""
    headers_dict = app_config["headers"].copy()
    headers_dict["X-Locale"] = headers_dict["X-Locale"].format(locale="ru")
    return headers_dict