from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("GET /contents/{content_id}/episodes")
def get_contents_content_episodes(api_client, token, content_id):
    """Получение коллекций"""
    api_client.set_token(token)
    response = api_client.get(
        Endpoints.GET_CONTENTS_CONTENT_EPISODES,
        with_auth=True,
        path_params={"content": content_id}
    )
    attach_curl(response, f"curl: GET /collections/{content_id}")
    attach_response_details(response)
    return response
