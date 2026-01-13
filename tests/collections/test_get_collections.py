from assertions.response_validator import check_status, check_schema, check_time
import allure
from api.requests.collections.get_collections import get_collections
from models.collections_model.get_collections_model import GetCollectionsModel


@allure.epic("Collections")
@allure.feature("GET /collections")
@allure.story("Позитивные сценарии")
class TestGetCoinPackagesPositive:

    @allure.title("Успешное получение списка коллекций")
    def test_get_collections_status_200(self, api_client, app_token):
        """Успешное получение пакетов монет"""
        with allure.step("GET requests /collections"):
            response = get_collections(api_client, app_token)

        with allure.step("Проверки ответа"):
            check_status(response, 200)

            response_json = response.json()
            validated_data = check_schema(response_json, GetCollectionsModel)

            # check_time(response, 1)
