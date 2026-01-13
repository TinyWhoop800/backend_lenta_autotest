from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("GET /search/hints")
def get_search_hints(api_client, token):
    """Получение коллекций"""
    api_client.set_token(token)
    response = api_client.get(Endpoints.GET_SEARCH_HINTS)
    attach_curl(response, f"curl: GET {Endpoints.GET_SEARCH_HINTS.value}")
    attach_response_details(response)
    return response
