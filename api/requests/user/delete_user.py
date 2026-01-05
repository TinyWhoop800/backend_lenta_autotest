from api.endpoints import Endpoints
from utils.allure_curl import attach_curl
import allure


@allure.step("Удаление пользователя")
def delete_user(api_client, app_config, token):
    """Удаление пользователя - возвращает requests.Response"""
    endpoint = Endpoints.DELETE_USER.value
    headers = app_config["headers"].copy()
    headers["Authorization"] = f"Bearer {token}"
    response = api_client.session.delete(
        f"{api_client.base_url}{endpoint}",
        headers=headers
    )
    attach_curl(response, "curl: DELETE /users/me")
    return response
