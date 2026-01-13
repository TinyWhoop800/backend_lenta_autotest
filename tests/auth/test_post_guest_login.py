from models.auth_models.post_guest_login import PostGuestLogin
from models.user.delete_user import DeleteUser
from assertions.response_validator import check_status, check_schema, check_time
from api.requests.auth.post_guest_login import post_guest_login
from api.requests.user.delete_user import delete_user
import allure


@allure.epic("Auth")
@allure.feature("Positive: /guest/login")
class TestPositivePostGuestLogin:

    @allure.title("Получение гостевого токена")
    def test_positive_post_guest_login(self, api_client):

        with allure.step("POST /auth_models/guest"):
            login_response = post_guest_login(api_client)
            login_json = login_response.json()

            with allure.step("Проверить ответ"):
                check_status(login_response, 200)
                check_schema(login_json, PostGuestLogin)
                check_time(login_response, 1)
                token = login_json["token"]

        with allure.step("DELETE /user"):
            delete_response = delete_user(api_client, token)
            delete_json = delete_response.json()

            with allure.step("Проверить ответ"):
                check_status(delete_response, 200)
                check_schema(delete_json, DeleteUser)
                check_time(delete_response, 1)
