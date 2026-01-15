from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("GET /genres")
def get_genres(api_client, token):
    """Получение Жанров"""
    api_client.set_token(token)
    response = api_client.get(Endpoints.GET_GENRES)
    attach_curl(response, f"curl: GET {Endpoints.GET_GENRES.value}")
    attach_response_details(response)
    return response

def get_genres_raw(api_client):
    """Получение Жанров без авторизации"""
    response = api_client.get(Endpoints.GET_GENRES, with_auth=False)
    return response