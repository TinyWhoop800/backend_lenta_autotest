from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("GET /coin-packages")
def get_coin_packages(api_client, token):
    """Получение пакетов монет"""
    api_client.set_token(token)
    response = api_client.get(Endpoints.GET_COIN_PACKAGES)
    attach_curl(response, f"curl: GET {Endpoints.GET_COIN_PACKAGES.value}")
    attach_response_details(response)
    return response


"""
Raw версия get_coin_packages БЕЗ Allure attachments.
Используется при загрузке тестовых данных в conftest.
"""

def get_coin_packages_raw(api_client, token):
    """
    Получить доступные пакеты монет (БЕЗ Allure attachments).

    Используется ТОЛЬКО при загрузке данных в pytest_configure,
    где Allure ещё не инициализирован.
    """
    api_client.set_token(token)
    response = api_client.get(Endpoints.GET_COIN_PACKAGES)
    return response
