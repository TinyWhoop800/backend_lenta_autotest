"""
POST /coin-packages - покупка пакета монет.

Отправляет multipart/form-data запрос с параметрами:
- coin_package_id: UUID пакета для покупки
- return_url: URL для возврата после оплаты
- payment_type: Метод оплаты (sbp, bank_card, sberbank, tinkoff_bank и т.д.)
"""


from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure
import logging

logger = logging.getLogger(__name__)


@allure.step("POST /coin-packages (coin_package_id={coin_package_id}, payment_type={payment_type})")
def post_coin_package(api_client, app_config, token, coin_package_id: str, payment_type: str, return_url: str = "kinolenta://"):

    api_client.set_token(token)

    form_data = {
        "coin_package_id": coin_package_id,
        "return_url": return_url,
        "payment_type": payment_type,
    }

    response = api_client.post(
        Endpoints.POST_COIN_PACKAGES,
        headers=app_config["headers"],
        data=form_data
    )

    # Логирование для Allure
    attach_curl(response,f"curl: POST /coin-packages (payment_type={payment_type})")
    attach_response_details(response)

    return response
