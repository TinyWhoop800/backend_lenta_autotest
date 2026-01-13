from api.endpoints import Endpoints
from utils.allure_curl import attach_curl, attach_response_details
import allure


@allure.step("GET /collections/{collection_id}/contents")
def get_collections_collection_contents(api_client, token, collection_id):
    """Получение коллекций"""
    api_client.set_token(token)
    response = api_client.get(
        Endpoints.GET_COLLECTIONS_COLLECTION_CONTENTS,
        with_auth=True,
        url_params={"collection": collection_id}
    )
    attach_curl(response, f"curl: GET /collections/{collection_id}/contents")
    attach_response_details(response)
    return response
