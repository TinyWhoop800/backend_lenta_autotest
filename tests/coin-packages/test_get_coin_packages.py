from assertions.response_validator import check_status, check_schema, check_time
import allure
from api.requests.coin_packeges.get_coin_packages import positive_get_coin_packages
from models.coin_packeges_model.get_coin_packages import GetCoinPackagesModel


@allure.epic("Coin Packages")
@allure.feature("Positive: GET /coin-packages")
class TestPositiveGetCoinPackages:

    @allure.title("Получение пакетов монет")
    def test_positive_get_coin_packages(self, app_config, api_client, app_token):
        with allure.step("GET /coin-packages"):
            login_response = positive_get_coin_packages(api_client, app_config, app_token)

        with allure.step("Проверить ответ"):
            check_status(login_response, 200)
            login_json = login_response.json()
            check_schema(login_json, GetCoinPackagesModel)
            check_time(login_response, 1)