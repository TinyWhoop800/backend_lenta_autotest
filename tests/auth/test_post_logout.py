# from assertions.response_validator import check_status, check_schema, check_time
# from api.requests.auth.post_logout import positive_post_logout_with_token, negative_post_logout_without_token
# import allure
# from models.auth.post_logout import Logout
#
# @allure.epic("Auth")
# @allure.feature("Positive: /logout")
# class TestPositivePostLogout:
#
#     @allure.title("Выход из аккаунта с токеном")
#     def test_positive_post_logout(self, app_config, api_client, authorized_token):
#         with allure.step("POST /logout"):
#             login_response = positive_post_logout_with_token(api_client, app_config, authorized_token)
#             login_json = login_response.json()
#
#         with allure.step("Проверить ответ"):
#             check_status(login_response, 200)
#             check_schema(login_json, Logout)
#             check_time(login_response, 1)
#
#
# # @allure.epic("Auth")
# # @allure.feature("Negative: /logout")
# # class TestNegativePostLogout:
# #
# #     @allure.title("Выход из аккаунта без токена")
# #     def test_positive_post_logout(self, app_config, api_client):
# #         with allure.step("POST /logout"):
# #             login_response = positive_post_logout_with_token(api_client, app_config)
# #             login_json = login_response.json()
# #
# #             with allure.step("Проверить ответ"):
# #                 check_status(login_response, 200)
# #                 check_schema(login_json, PostGuestLogin)
# #                 check_time(login_response, 1)
# #                 token = login_json["token"]
# #
# #         with allure.step("DELETE /users/me"):
# #             delete_response = delete_user(api_client, app_config, token)
# #             delete_json = delete_response.json()
# #
# #             with allure.step("Проверить ответ"):
# #                 check_status(delete_response, 200)
# #                 check_schema(delete_json, DeleteUser)
# #                 check_time(delete_response, 1)