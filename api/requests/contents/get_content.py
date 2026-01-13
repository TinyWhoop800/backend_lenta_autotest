from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("GET /next-title")
def get_content(api_client, token, page_number):
    """Получение Списка контента"""
    api_client.set_token(token)
    page = f'page={page_number}'
    response = api_client.get(Endpoints.GET_NEXT_TITLE, with_auth=True,
        url_params=page)
    attach_curl(response, f"curl: GET {Endpoints.GET_CONTENT.value}")
    attach_response_details(response)
    return response


def get_content_raw(api_client, token, page_number):
    """Получение Списка контента"""
    api_client.set_token(token)
    page = f'page={page_number}'
    response = api_client.get(Endpoints.GET_NEXT_TITLE, with_auth=True,
        url_params=page)
    return response