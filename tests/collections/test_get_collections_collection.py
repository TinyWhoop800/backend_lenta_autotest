from assertions.response_validator import check_status, check_schema, check_time
import allure
from api.requests.collections.get_collections_collection import get_collections_collection
from models.collections_model.get_collections_collection_model import GetCollectionsCollectionModel
from tests.test_data.collection_data import INVALID_COLLECTION_IDS
import pytest


@allure.epic("Collections")
@allure.feature("GET /collections/collection")
@allure.story("Позитивные сценарии")
class TestGetCollectionsCollectionPositive:

    @allure.title("Получение спец. коллекции")
    def test_get_collections_collection_status_200(self, prepared_api_client_collections):
        """Успешное получение пакетов монет"""
        with allure.step(f"GET /collections/{prepared_api_client_collections.collection_id}"):
            response = get_collections_collection(
                prepared_api_client_collections.client,
                prepared_api_client_collections.token,
                prepared_api_client_collections.collection_id
            )

        with allure.step("Проверки ответа"):
            check_status(response, 200)

            response_json = response.json()
            validated_data = check_schema(response_json, GetCollectionsCollectionModel)

            # check_time(response, 1)


@allure.epic("Collections")
@allure.feature("GET /collections/collection")
@allure.story("Негативные сценарии")
class TestGetCollectionsCollectionNegative:

    @allure.title("Получение ошибки 404")
    @pytest.mark.parametrize("invalid_id", INVALID_COLLECTION_IDS)
    def test_get_collections_collection_status_404(self, api_client, app_token, invalid_id):
        """Получение ошибки 404"""
        with allure.step(f"GET /collections/{invalid_id}"):
            response = get_collections_collection(api_client, app_token, invalid_id)

        with allure.step("Проверки ответа"):
            check_status(response, 404)