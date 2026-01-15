from assertions.response_validator import check_status, check_schema, check_time
import allure
from api.requests.genres.get_genres import get_genres
from models.genres_model.get_genres_model import GetGenresModel


@allure.epic("Genres")
@allure.feature("GET /genres - Positive")
class TestGetGenresPositive:

    @allure.story("Получение статуса: 200")
    @allure.title("Получение списка жанров")
    def test_get_genres_status_200(self, api_client, app_token):
        """Успешное получение списка жанров"""
        with allure.step("GET requests /genres"):
            response = get_genres(api_client, app_token)

        with allure.step("Проверки ответа"):
            check_status(response, 200)

            response_json = response.json()
            validated_data = check_schema(response_json, GetGenresModel)

            # check_time(response, 1)
