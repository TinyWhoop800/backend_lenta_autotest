from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("Удаление пользователя")
def delete_user(api_client, token):
    """Delete user account"""
    api_client.set_token(token)
    response = api_client.delete(
        Endpoints.DELETE_USER,
    )
    attach_curl(response, "curl: DELETE /user")
    attach_response_details(response)
    api_client.clear_token()
    return response


"""
Raw версия delete_user БЕЗ Allure attachments.
Используется при загрузке тестовых данных в conftest.
"""

def delete_user_raw(api_client, token):
    """
    Удалить пользователя (БЕЗ Allure attachments).

    Используется ТОЛЬКО при загрузке данных в pytest_configure,
    где Allure ещё не инициализирован.
    """
    api_client.set_token(token)
    response = api_client.delete(Endpoints.DELETE_USER)
    return response
