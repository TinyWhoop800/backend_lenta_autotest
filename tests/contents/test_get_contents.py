from assertions.response_validator import check_status, check_schema, check_time
import allure
from api.requests.contents.get_content import get_contents
from models.contents_models.get_contents_model import GetContentsModel


@allure.epic("Contents")
@allure.feature("GET /contents - Positive")
class TestGetContentsPositive:

    @allure.story("Получение статуса: 200")
    @allure.title("Успешное получение списка тайтлов")
    def test_get_contents_status_200(self, api_client, app_token):
        """Успешное получение списка контента"""
        with allure.step("GET requests /contents"):
            page = 1
            response = get_contents(api_client, app_token, page)

        with allure.step("Проверки ответа"):
            check_status(response, 200)

            response_json = response.json()
            validated_data = check_schema(response_json, GetContentsModel)

            # check_time(response, 1)
