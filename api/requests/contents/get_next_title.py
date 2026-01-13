from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("GET /next-title")
def get_next_title(api_client, token):
    """Получение Тайтла"""
    api_client.set_token(token)
    response = api_client.get(Endpoints.GET_NEXT_TITLE)
    attach_curl(response, f"curl: GET {Endpoints.GET_NEXT_TITLE.value}")
    attach_response_details(response)
    return response