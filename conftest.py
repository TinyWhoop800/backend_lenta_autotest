import pytest
from config.apps import APPS_LENTA

@pytest.fixture(scope="session")
def api_client():
    from clients.api_client import APIClient
    from config.settings import settings
    client = APIClient(settings.BASE_URL)
    yield client
    client.close()

@pytest.fixture(params=APPS_LENTA, ids=lambda app: f"{app['app_name']}_{app['platform']}")
def app_config(request):
    return request.param
