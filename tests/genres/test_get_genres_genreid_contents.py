from assertions.response_validator import check_status, check_schema, check_time
import allure
from api.requests.genres.get_genres_genreid_contents import get_genres_genreid_contents
from models.genres_model.get_genres_genreid_contents_model import GetGenresGenreIdContentsModel
from tests.test_data.collection_data import INVALID_COLLECTION_IDS
import pytest


@allure.epic("Genres")
@allure.feature("GET /genres/genreId/contents - Positive")
class TestGetGenresGenreIdContentsPositive:

    @allure.story("Получение статуса: 200")
    @allure.title("Получение контента жанра")
    def test_get_genre_genreid_contents_status_200(self, prepared_api_client_genre_id):
        """Успешное получение контента жанра"""
        with allure.step(f"GET /collections/{prepared_api_client_genre_id.genre_id}"):
            response = get_genres_genreid_contents(
                prepared_api_client_genre_id.client,
                prepared_api_client_genre_id.token,
                prepared_api_client_genre_id.genre_id
            )

        with allure.step("Проверки ответа"):
            check_status(response, 200)

            response_json = response.json()
            validated_data = check_schema(response_json, GetGenresGenreIdContentsModel)

            # check_time(response, 1)


# @allure.epic("Collections")
# @allure.feature("GET /collections/collection - Negative")
# class TestGetCollectionsCollectionNegative:
#
#     @allure.story("Получение статуса: 404")
#     @allure.title("Невалидный collection_id")
#     @pytest.mark.parametrize("invalid_id", INVALID_COLLECTION_IDS)
#     def test_get_collections_collection_status_404(self, api_client, app_token, invalid_id):
#         """Получение ошибки 404"""
#         with allure.step(f"GET /collections/{invalid_id}"):
#             response = get_collections_collection(api_client, app_token, invalid_id)
#
#         with allure.step("Проверки ответа"):
#             check_status(response, 404)