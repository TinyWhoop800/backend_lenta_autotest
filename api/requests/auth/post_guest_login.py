from api.endpoints import Endpoints
from utils.allure_curl import attach_curl
import allure


@allure.step("Получение гостевого токена")
def post_guest_login(api_client, app_config):
    """Guest login - возвращает requests.Response"""
    endpoint = Endpoints.POST_GUEST_LOGIN.value
    headers = app_config["headers"].copy()
    response = api_client.session.post(
        f"{api_client.base_url}{endpoint}",
        headers=headers
    )
    attach_curl(response, "curl: POST /auth/guest")
    return response
