import allure
from api.requests.coin_packeges.post_coin_packages import post_coin_package
from assertions.response_validator import check_status, check_time
from tests.test_data.coin_packages_data import (
    INVALID_COIN_IDS,
    INVALID_PAYMENT_TYPES,
)
import pytest

#TODO: Переделать с использованием ручки /yookassa/payment-methods, чтобы вытаскивать платежные методы при помощи этой ручки
#TODO: Статус 500 на тест. стенде, на бэкенде нужно изменить статус

@allure.epic("Coin Packages")
@allure.feature("POST /coin-packages - Positive")
class TestPostCoinPackagesPositive:

    @allure.title("Получение платежной ссылки с валидным id coin-packages")
    def test_post_coin_packages_valid_id(
            self,
            api_client,
            session_tokens,
            payment_type,
            coin_id,
            test_app_config,
    ):
        """
        Тест для всех комбинаций:
        payment_type × coin_id × app_config
        """
        key = f"{test_app_config['app_name']}_{test_app_config['platform']}"
        token = session_tokens[key]

        with allure.step(
                f"POST /coin-packages: {key} | {payment_type} | {coin_id[:8]}"
        ):
            response = post_coin_package(
                api_client=api_client,
                app_config=test_app_config,
                token=token,
                coin_package_id=coin_id,
                payment_type=payment_type,
            )

        with allure.step("Проверки ответа"):
            check_status(response, 200)
            check_time(response, 1)


@allure.epic("Coin Packages")
@allure.feature("POST /coin-packages - Negative")
class TestPostCoinPackagesNegative:

    @pytest.mark.parametrize("invalid_coin_id", INVALID_COIN_IDS)
    @allure.title("Невалидный coin_id = 404")
    def test_invalid_coin_id(
        self, api_client, app_config, app_token, invalid_coin_id
    ):
        response = post_coin_package(
            api_client, app_config, app_token, invalid_coin_id, "sbp"
        )
        check_status(response, 404)

    @pytest.mark.parametrize("invalid_payment", INVALID_PAYMENT_TYPES)
    @allure.title("Невалидный payment_type = 400")
    def test_invalid_payment_type(
        self, api_client, app_config, app_token, invalid_payment
    ):
        response = post_coin_package(
            api_client, app_config, app_token, VALID_COIN_IDS[0], invalid_payment
        )
        check_status(response, 400)

    @allure.title("Без токена = 401")
    def test_no_auth(
        self, api_client, app_config, payment_type, coin_id
    ):
        response = post_coin_package(
            api_client, app_config, "", coin_id, payment_type
        )
        check_status(response, 401)