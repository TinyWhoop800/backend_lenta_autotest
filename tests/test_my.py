from models.auth.post_guest_login import PostGuestLogin
from models.user.delete_user import DeleteUser
from assertions.response_validator import check_status, check_schema, check_time
from api.requests.auth.post_guest_login import post_guest_login
from api.requests.user.delete_user import delete_user


def test_first(app_config, api_client):
    # Guest login
    login_response = post_guest_login(api_client, app_config)
    login_json = login_response.json()

    check_status(login_response, 200)
    check_schema(login_json, PostGuestLogin)
    check_time(login_response, 1)

    token = login_json["token"]

    # Delete user
    delete_response = delete_user(api_client, app_config, token)
    delete_json = delete_response.json()

    check_status(delete_response, 200)
    check_schema(delete_json, DeleteUser)
    check_time(delete_response, 1)