from assertions.response_validator import check_status, check_schema, check_time
import allure
from api.requests.contents.get_next_title import get_next_title
from models.contents_models.get_next_title_model import GetNextTitleModel


@allure.epic("Contents")
@allure.feature("GET /next-title - Positive")
class TestGetNextTitlePositive:

    @allure.story("Получение статуса: 200")
    @allure.title("Получение одного тайтла")
    def test_get_next_title_status_200(self, api_client, app_token):
        """Успешное получение одного тайтла"""
        with allure.step("GET requests /next-title"):
            response = get_next_title(api_client, app_token)

        with allure.step("Проверки ответа"):
            check_status(response, 200)

            response_json = response.json()
            validated_data = check_schema(response_json, GetNextTitleModel)

            # check_time(response, 1)
