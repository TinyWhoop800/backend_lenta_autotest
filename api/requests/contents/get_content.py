from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("GET /contents")
def get_contents(api_client, token, page):
    """Получение списка контента"""
    api_client.set_token(token)
    response = api_client.get(
        Endpoints.GET_CONTENTS,
        query_params={'page': page}
    )
    attach_curl(response, f"curl: GET {Endpoints.GET_CONTENTS.value}")
    attach_response_details(response)
    return response


def get_content_raw(api_client, page):
    """Получение списка контента с пагинацией"""
    response = api_client.get(
        Endpoints.GET_CONTENTS,
        with_auth=False,
        query_params={'page': page}
    )
    return response