# from assertions.response_validator import check_status, check_schema
# import allure
# import pytest
# from api.requests.auth.post_guest_login import post_guest_login
# from api.requests.user.delete_user import delete_user
# from models.user.delete_user import DeleteUser
# from api.endpoints import Endpoints
#
#
# @allure.epic("User Management")
# @allure.feature("Delete user")
# class TestDeleteUser:
#
#     @pytest.fixture
#     def new_guest_token(self, api_client):
#         """
#         Создать новый гостевой токен для этого теста.
#         """
#         response = post_guest_login(api_client)
#         check_status(response, 200)
#         token = response.json()["token"]
#
#         yield token
#
#     @allure.title("Delete user account successfully")
#     @allure.description("Authorized user should be able to delete their account")
#     def test_delete_user_success(self, api_client, new_guest_token):
#         """Успешное удаление пользователя"""
#
#         with allure.step("Delete user account"):
#             response = delete_user(api_client, new_guest_token)
#
#         with allure.step("Verify deletion"):
#             check_status(response, 200)
#             validated = check_schema(response.json(), DeleteUser)
#
#             # assert validated.data.userId > 0
#             # assert "success" in validated.message.lower() or "deleted" in validated.message.lower()
#
#     @allure.title("Deleted user cannot access protected endpoints")
#     def test_deleted_user_cannot_access(self, api_client, new_guest_token):
#         """Удалённый пользователь не может получить доступ к protected endpoints"""
#
#         delete_user(api_client, new_guest_token)
#
#         with allure.step("Try to access protected endpoint with deleted user token"):
#             api_client.set_token(new_guest_token)
#             response = api_client.get(Endpoints.GET_USER)
#
#         with allure.step("Verify access denied"):
#             check_status(response, 401)
