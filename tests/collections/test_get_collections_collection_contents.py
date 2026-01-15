from assertions.response_validator import check_status, check_schema, check_time
import allure
from api.requests.collections.get_collections_collection_contents import get_collections_collection_contents
from models.collections_model.get_collections_collection_contents_model import GetCollectionsCollectionContentsModel
from tests.test_data.collection_data import INVALID_COLLECTION_IDS
import pytest


@allure.epic("Collections")
@allure.feature("GET /collections/collection/content - Positive")
class TestGetCollectionsCollectionContentPositive:

    @allure.story("Получение статуса: 200")
    @allure.title("Получение информации о коллекции")
    def test_get_collections_collection_content_status_200(self, prepared_api_client_collections):
        """Успешное получение пакетов монет"""
        with allure.step(f"GET /collections/{prepared_api_client_collections.collection_id}/content"):
            response = get_collections_collection_contents(
                prepared_api_client_collections.client,
                prepared_api_client_collections.token,
                prepared_api_client_collections.collection_id
            )

        with allure.step("Проверки ответа"):
            check_status(response, 200)

            response_json = response.json()
            validated_data = check_schema(response_json, GetCollectionsCollectionContentsModel)

            # check_time(response, 1)


@allure.epic("Collections")
@allure.feature("GET /collections/collection/content - Negative")
class TestGetCollectionsCollectionContentNegative:

    @allure.story("Получение статуса: 404")
    @allure.title("Невалидный collection_id")
    @pytest.mark.parametrize("invalid_id", INVALID_COLLECTION_IDS)
    def test_get_collections_collection_content_status_404(self, api_client, app_token, invalid_id):
        """Получение ошибки 404"""
        with allure.step(f"GET /collections/{invalid_id}"):
            response = get_collections_collection_contents(api_client, app_token, invalid_id)

        with allure.step("Проверки ответа"):
            check_status(response, 404)