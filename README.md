# Backend Lenta AutoTest

API automation testing framework для сервиса Lenta (KinoLenta, ReelPix, RJOY).

## Структура проекта

```
.
├── api/
│   ├── endpoints.py           # Enum со всеми endpoints
│   └── requests/              # Функции-обёртки для API вызовов
│       ├── auth/
│       ├── coin_packages/
│       ├── user/
│       └── ...
├── clients/
│   └── api_client.py          # HTTP клиент с retry logic и управлением headers/tokens
├── models/
│   ├── auth/
│   ├── coin_packages/
│   └── ...                    # Pydantic модели для валидации ответов
├── assertions/
│   └── response_validator.py  # Функции проверки статуса, схемы, времени ответа
├── config/
│   ├── apps.py               # Конфиги приложений (headers, payment_type и т.д.)
│   └── settings.py           # Переменные окружения
├── tests/
│   ├── conftest.py           # Глобальные фикстуры (api_client, tokens и т.д.)
│   ├── auth/
│   ├── coin_packages/
│   │   ├── conftest.py       # Локальные фикстуры для coin_packages
│   │   └── test_*.py
│   ├── search/
│   └── ...
├── utils/
│   └── allure_curl.py        # Утилиты для Allure отчётов
├── tests/test_data/
│   └── coin_packages_data.py # Невалидные тестовые данные
└── .env                      # Переменные окружения

```

## Установка

```bash
# Клонируешь проект
git clone <repo>
cd backend_lenta_autotest

# Создаёшь виртуальное окружение
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Устанавливаешь зависимости
pip install -r requirements.txt
```

## Запуск тестов

```bash
# Все тесты
pytest

# Конкретный файл
pytest tests/coin_packages/test_post_coin_packages.py

# С определённым тегом
pytest -m "not slow"

# С Allure отчётом
pytest --alluredir=allure_results
allure serve allure_results
```

## Ключевые компоненты

### APIClient (`clients/api_client.py`)
- Управляет HTTP сессией и retry logic (для 429 ошибок)
- Хранит headers и токены
- Поддерживает подстановку параметров в URL

**Использование:**
```python
client = APIClient(
    base_url="https://api.example.com",
    default_headers={"X-Device-ID": "test"},
    retries=3
)
client.set_token(token)
response = client.get(Endpoints.GET_USER)
```

### Request функции (`api/requests/`)
- Обёртки над APIClient для конкретных endpoints
- Автоматически аттачат curl и детали ответа в Allure

**Пример:**
```python
def post_guest_login(api_client):
    response = api_client.post(Endpoints.POST_GUEST_LOGIN, with_auth=False)
    attach_curl(response, "curl: POST /guest/login")
    return response
```

### Response Validator (`assertions/response_validator.py`)
- `check_status()` — проверка статус кода
- `check_schema()` — валидация JSON через Pydantic
- `check_time()` — проверка времени ответа
- `check_array_length()` — проверка количества элементов в массиве
- `check_json_value()` — проверка конкретного значения (поддерживает nested)

### Fixtures (`conftest.py`)
- `api_client_factory` — фабрика для создания клиентов с нужными headers
- `api_client` — клиент для текущей app_config
- `app_config` — параметризованный фикстур со всеми приложениями
- `session_tokens` — токены для всех приложений (кешируется на сессию)
- `app_token` — токен для текущей app_config

### Parametrization (`tests/coin_packages/conftest.py`)
- `pytest_generate_tests()` — генерирует все комбинации для позитивных тестов
- `prepared_api_client` — фикстур с уже готовым клиентом и токеном

## Разработка новой ручки

1. Добавь endpoint в `api/endpoints.py`
2. Создай Pydantic модель в `models/`
3. Создай request функцию в `api/requests/`
4. Напиши тесты в `tests/`
5. Добавь невалидные данные в `tests/test_data/` если нужно

**Пример:**
```python
# api/endpoints.py
class Endpoints(Enum):
    GET_MY_NEW_ENDPOINT = "/my/new/endpoint"

# models/my_model.py
class MyResponse(BaseModel):
    data: str
    count: int

# api/requests/my_request.py
def get_my_endpoint(api_client):
    response = api_client.get(Endpoints.GET_MY_NEW_ENDPOINT)
    attach_curl(response, "curl: GET /my/new/endpoint")
    return response

# tests/test_my_endpoint.py
def test_my_endpoint(api_client, app_token):
    response = get_my_endpoint(api_client)
    check_status(response, 200)
    validated = check_schema(response.json(), MyResponse)
```

## Переменные окружения

```env
ENV=test
API_BASE_URL=https://lenta-test.iptv2021.com/api/v1
```

## Важные концепции

### Headers в APIClient
Headers хранятся в `APIClient`, а не передаются в каждый вызов:
```python
# Клиент уже знает все headers
client = APIClient(base_url=url, default_headers=app_config["headers"])
# Не нужно передавать app_config в request функции
response = client.get(endpoint)
```

### Токены управляются клиентом
```python
client.set_token(token)
response = client.post(endpoint)  # Токен добавится автоматически
client.clear_token()
```

### Parametrization для разных приложений
- Позитивные тесты: через `pytest_generate_tests()`
- Негативные тесты: через `@pytest.mark.parametrize()` + `app_config`

## Контакты / Поддержка

Проект использует:
- **pytest** — фреймворк для тестов
- **pydantic** — валидация данных
- **requests** — HTTP клиент
- **allure** — отчёты
