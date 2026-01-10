from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("GET coin packages")
def get_coin_packages(api_client, app_config, token):
    """Получение пакетов монет"""
    api_client.set_token(token)
    response = api_client.get(
        Endpoints.GET_COIN_PACKAGES,
        headers=app_config["headers"]
    )
    attach_curl(response, f"curl: GET {Endpoints.GET_COIN_PACKAGES.value}")
    attach_response_details(response)
    return response
