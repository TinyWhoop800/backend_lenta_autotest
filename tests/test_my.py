# tests/test_first.py
import pytest
from clients.api_client import APIClient
from config.settings import settings
from config.apps import APPS_LENTA
from api.endpoints import Endpoints


def test_first(api_client, headers, app_config):
    """Самый первый тест - проверим что все работает"""

    # 1. Создаем клиент
    api_client = APIClient(settings.BASE_URL)

    # 2. Берем первое приложение
    app = APPS_LENTA[0]
    print(f"Тестируем: {app['app_name']} ({app['platform']})")

    # 3. Делаем заголовки
    headers = app["headers"].copy()

    endpoint = Endpoints.POST_GUEST_LOGIN
    print(f"Отправляю запрос на: {api_client.base_url}{endpoint.value}")  # <- .value здесь!
    print(f"Используя следующие headers: {headers}")

    response = api_client.post(endpoint, headers=headers)

    # 5. Проверяем
    assert response.status_code == 200, f"Ошибка: {response.status_code}"
    print(f"✓ Гость создан!")

    # 6. Берем токен
    token = response.json()['token']
    print(f"Токен: {token[:20]}...")

    # 7. Добавляем токен в заголовки
    auth_headers = headers.copy()
    auth_headers["Authorization"] = f"Bearer {token}"

    # 8. Пробуем получить информацию о пользователе
    user_response = api_client.get(
        Endpoints.GET_USER,
        headers=auth_headers
    )
    assert user_response.status_code == 200
    print(f"✓ Информация о пользователе получена")

    # 9. Удаляем пользователя
    delete_response = api_client.delete(
        Endpoints.DELETE_USER,
        headers=auth_headers
    )
    assert delete_response.status_code == 200
    print(f"✓ Пользователь удален")

    print(f"✅ Тест пройден!")


if __name__ == "__main__":
    test_first()