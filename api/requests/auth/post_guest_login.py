from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("POST /guest/login")
def post_guest_login(api_client):
    """
    Guest login - возвращает requests.Response.

    Этот endpoint не требует авторизации (with_auth=False).
    """
    response = api_client.post(
        Endpoints.POST_GUEST_LOGIN,
        with_auth=False
    )
    attach_curl(response, "curl: POST /guest/login")
    attach_response_details(response)
    return response
