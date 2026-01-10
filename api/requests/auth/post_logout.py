from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("POST /logout (token)")
def post_logout_with_token(api_client, app_config, token):
    """Positive logout - с валидным токеном"""
    api_client.set_token(token)
    response = api_client.post(
        Endpoints.POST_LOGOUT,
        headers=app_config["headers"]
    )
    attach_curl(response, "curl: POST /logout")
    attach_response_details(response)
    api_client.clear_token()
    return response


@allure.step("POST /logout (no token)")
def post_logout_without_token(api_client, app_config):
    """Negative logout - без токена"""
    response = api_client.post(
        Endpoints.POST_LOGOUT,
        headers=app_config["headers"],
        with_auth=False
    )
    attach_curl(response, "curl: POST /logout (без токена)")
    attach_response_details(response)
    return response
