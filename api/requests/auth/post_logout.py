from api.endpoints import Endpoints
from utils.allure_curl import attach_curl
import allure


@allure.step("Positive logout user (with a token)")
def positive_post_logout_with_token(api_client, app_config, token):
    endpoint = Endpoints.POST_LOGOUT.value
    headers = app_config["headers"].copy()
    headers["Authorization"] = f"Bearer {token}"
    response = api_client.session.post(
        f"{api_client.base_url}{endpoint}",
        headers=headers
    )
    attach_curl(response, "curl: POST /logout")
    return response


@allure.step("Negative logout user (without a token)")
def negative_post_logout_without_token(api_client, app_config):
    endpoint = Endpoints.POST_LOGOUT.value
    headers = app_config["headers"].copy()
    response = api_client.session.post(
        f"{api_client.base_url}{endpoint}",
        headers=headers
    )
    attach_curl(response, "curl: POST /logout")
    return response