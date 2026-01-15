from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("GET /genres")
def get_genres_genreid_contents(api_client, token, genre_id):
    """Получение Жанров"""
    api_client.set_token(token)
    response = api_client.get(Endpoints.GET_GENRES_GENRE_ID_CONTENTS, with_auth=True, path_params={"genre_id": genre_id})
    attach_curl(response, f"curl: GET {Endpoints.GET_GENRES_GENRE_ID_CONTENTS.value}")
    attach_response_details(response)
    return response