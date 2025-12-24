from clients.api_client import APIClient
from api.endpoints import Endpoints
from assertions.response_validator import check_status, check_time, check_schema


def delete_user(api_client: APIClient, headers: dict, user_token: str):
    """
    Удалить пользователя
    user_token: токен пользователя, которого удаляем
    """
    # Копируем заголовки и добавляем токен
    auth_headers = headers.copy()
    auth_headers["Authorization"] = f"Bearer {user_token}"

    response = api_client.delete(Endpoints.DELETE_USER, headers=auth_headers)
    check_status(response, 200)
    return response