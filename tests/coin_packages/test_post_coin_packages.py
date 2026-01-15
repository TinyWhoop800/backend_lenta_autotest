import allure
from api.requests.coin_packages.post_coin_packages import post_coin_package
from assertions.response_validator import check_status, check_time, check_schema
from models.coin_packages_model.post_coin_packages_model import PostCoinPackagesModel
from tests.test_data.coin_packages_data import (
    INVALID_COIN_IDS,
)
import pytest

#TODO: Переделать с использованием ручки /yookassa/payment-methods, чтобы вытаскивать платежные методы при помощи этой ручки
#TODO: Статус 500 на тест. стенде, на бэкенде нужно изменить статус

@allure.epic("Coin Packages")
@allure.feature("POST /coin-packages - Positive")
class TestPostCoinPackagesPositive:

    @allure.story("Получение статуса: 200")
    @allure.title('Получение платежной ссылки с валидным id coin-packages: "{prepared_api_client.coin_id}"')
    def test_post_coin_packages_valid_id(self, prepared_api_client):
        with allure.step(
                f"POST /coin-packages: {prepared_api_client.app_config['app_name']} "
                f"| {prepared_api_client.payment_type} "
                f"| {prepared_api_client.coin_id[:8]}"
        ):
            response = post_coin_package(
                api_client=prepared_api_client.client,
                token=prepared_api_client.token,
                coin_package_id=prepared_api_client.coin_id,
                payment_type=prepared_api_client.payment_type,
            )

        with allure.step("Проверки ответа"):
            check_status(response, 200)
            response_json = response.json()
            check_schema(response_json, PostCoinPackagesModel)


@allure.epic("Coin Packages")
@allure.feature("POST /coin-packages - Negative")
class TestPostCoinPackagesNegative:

    @allure.story("Получение статуса: 401")
    @allure.title('Без авторизации: "{prepared_api_client.coin_id}"')
    def test_post_coin_packages_valid_id_no_auth_status_401(self, prepared_api_client):
        with allure.step("POST /coin-packages без токена"):
            response = post_coin_package(
                prepared_api_client.client,
                "",
                prepared_api_client.coin_id,
                prepared_api_client.payment_type
            )
        with allure.step("Проверить 401 Unauthorized"):
            check_status(response, 401)

    @allure.story("Получение статуса: 404")
    @pytest.mark.parametrize("invalid_coin_id", INVALID_COIN_IDS)
    @allure.title('Невалидный coin_id: "{invalid_coin_id}"')
    def test_invalid_coin_id_status_404(self, api_client, app_token, invalid_coin_id):
        """Каждый невалидный coin_id со случайным payment_type"""
        with allure.step(f"POST /coin-packages с невалидным coin_id"):
            response = post_coin_package(
                api_client,
                app_token,
                invalid_coin_id,
                "bank_card"
            )

        with allure.step("Проверить 404 Not Found"):
            check_status(response, 404)