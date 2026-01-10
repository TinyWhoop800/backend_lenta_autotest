# tests/auth/test_logout_negative.py
from assertions.response_validator import check_status
import allure
from api.requests.auth.post_logout import post_logout_without_token


@allure.epic("Authentication")
@allure.feature("Logout")
@allure.story("Negative scenarios")
class TestLogoutNegative:

    @allure.title("Logout without token should fail")
    @allure.description(
        "User should not be able to logout without providing valid token. "
        "Expected: 401 Unauthorized"
    )
    def test_logout_without_token_returns_401(self, app_config, api_client):
        """Logout без токена должен вернуть 401"""
        with allure.step("Attempt logout without token"):
            response = post_logout_without_token(api_client, app_config)

        with allure.step("Verify error response"):
            check_status(response, 401)

            response_json = response.json()
            assert "error" in response_json or "message" in response_json
