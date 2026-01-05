from api.endpoints import Endpoints
from utils.allure_curl import attach_curl
import allure


@allure.step("Positive get coin packages")
def positive_get_coin_packages(api_client, app_config, token):
    endpoint = Endpoints.GET_COIN_PACKAGES.value
    headers = app_config["headers"].copy()
    headers["Authorization"] = f"Bearer {token}"
    response = api_client.session.get(
        f"{api_client.base_url}{endpoint}",
        headers=headers
    )
    attach_curl(response, f"curl: GET {endpoint}")
    return response