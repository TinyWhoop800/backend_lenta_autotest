from clients.api_client import APIClient
from api.endpoints import Endpoints
from assertions.response_validator import check_status, check_schema, check_time

def get_guest_user_token(api_client: APIClient, headers: dict):
    request_headers = headers
    response = api_client.post(Endpoints.POST_GUEST_LOGIN, headers=headers)
    guest_token = response.json()['token']
    return guest_token
