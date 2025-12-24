from api.endpoints import Endpoints


def post_guest_login(api_client, app_config):
    """Guest login - возвращает requests.Response"""
    endpoint = Endpoints.POST_GUEST_LOGIN.value
    headers = app_config["headers"].copy()
    response = api_client.session.post(
        f"{api_client.base_url}{endpoint}",
        headers=headers
    )
    return response
