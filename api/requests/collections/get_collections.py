from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("GET /collections")
def get_collections(api_client, token):
    """Получение коллекций"""
    api_client.set_token(token)
    response = api_client.get(Endpoints.GET_COLLECTIONS)
    attach_curl(response, f"curl: GET {Endpoints.GET_COIN_PACKAGES.value}")
    attach_response_details(response)
    return response

"""
Raw версия get_coin_packages БЕЗ Allure attachments.
Используется при загрузке тестовых данных в conftest.
"""

def get_collections_raw(api_client):
    """Получение коллекций (БЕЗ Allure, БЕЗ токена)"""
    response = api_client.get(Endpoints.GET_COLLECTIONS, with_auth=False)
    return response
