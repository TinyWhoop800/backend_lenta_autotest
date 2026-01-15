from assertions.response_validator import check_status, check_schema, check_time
import allure
from api.requests.coin_packages.get_coin_packages import get_coin_packages
from models.coin_packages_model.get_coin_packages_model import GetCoinPackagesModel


@allure.epic("Coin Packages")
@allure.feature("GET /coin-packages - Positive")
class TestGetCoinPackagesPositive:

    @allure.story("Получение статуса: 200")
    @allure.title("Успешное получение пакетов с монетами")
    def test_get_coin_packages_success(self, api_client, app_token):
        """Успешное получение пакетов монет"""
        with allure.step("GET requests /coin-packages"):
            response = get_coin_packages(api_client, app_token)

        with allure.step("Проверки ответа"):
            check_status(response, 200)

            response_json = response.json()
            validated_data = check_schema(response_json, GetCoinPackagesModel)

            check_time(response, 1)
