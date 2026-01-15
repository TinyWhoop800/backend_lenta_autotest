from assertions.response_validator import check_status, check_schema, check_time
import allure
from api.requests.contents.get_contents_content_episodes import get_contents_content_episodes
from models.contents_models.get_contents_content_episodes_model import GetContentsContentEpisodesModel
from tests.test_data.contents_data import INVALID_CONTENT_IDS
import pytest



@allure.epic("Contents")
@allure.feature("GET /contents/content/episodes - Positive")
class TestGetContentsContentEpisodesPositive:

    @allure.story("Получение статуса: 200")
    @allure.title('Получение информации о листе эпизодов')
    def test_get_contents_content_episodes_status_200(self, prepared_api_client_contents):
        """Успешное получение информации о листе эпизодов"""
        with allure.step(f"GET /contents/{prepared_api_client_contents.content_id}/episodes"):
            response = get_contents_content_episodes(
                prepared_api_client_contents.client,
                prepared_api_client_contents.token,
                prepared_api_client_contents.content_id
            )

        with allure.step("Проверки ответа"):
            check_status(response, 200)
            response_json = response.json()
            validated_data = check_schema(response_json, GetContentsContentEpisodesModel)

@allure.epic("Contents")
@allure.feature("GET /contents/content/episodes - Negative")
class TestGetContentsContentEpisodesNegative:

    @allure.story("Получение статуса: 404")
    @allure.title('Проверяем, что при невалидном content_id статус - 404')
    @pytest.mark.parametrize("invalid_content_id", INVALID_CONTENT_IDS)
    def test_get_contents_content_episodes_status_404(self, api_client, app_token, invalid_content_id):
        """Неуспешное получение информации о листе эпизодов"""
        with allure.step(f"GET /contents/{invalid_content_id}/episodes"):
            response = get_contents_content_episodes(api_client, app_token, invalid_content_id)

        with allure.step("Проверки ответа"):
            check_status(response, 404)