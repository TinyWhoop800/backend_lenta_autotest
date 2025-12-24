from api.endpoints import Endpoints


def delete_user(api_client, app_config, token):
    """Удаление пользователя - возвращает requests.Response"""
    endpoint = Endpoints.DELETE_USER.value
    headers = app_config["headers"].copy()
    headers["Authorization"] = f"Bearer {token}"
    response = api_client.session.delete(
        f"{api_client.base_url}{endpoint}",
        headers=headers
    )
    return response  # ← Возвращаем Response, а не JSON
