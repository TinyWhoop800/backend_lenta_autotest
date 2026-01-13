from assertions.response_validator import check_status, check_schema, check_time, check_array_length
import allure
from api.requests.search.get_search_hints import get_search_hints
from models.search_models.get_search_hints_model import GetSearchHintsModel


@allure.epic("Search")
@allure.feature("GET /search/hints")
@allure.story("Позитивные сценарии")
class TestGetCoinPackagesPositive:

    @allure.title("Получение 15 тайтлов массивом")
    def test_get_search_hints_status_200(self, api_client, app_token):
        """Успешное получение 15 тайтлов массивом"""
        with allure.step("GET requests /search/hints"):
            response = get_search_hints(api_client, app_token)

        with allure.step("Проверки ответа"):
            check_status(response, 200)

            response_json = response.json()
            validated_data = check_schema(response_json, GetSearchHintsModel)

            check_array_length(validated_data.root, 15)

            # check_time(response, 1)
