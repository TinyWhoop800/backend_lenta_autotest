def check_status(response, expected_code: int):
    """Проверка статус кода"""
    assert response.status_code == expected_code, \
        f"Ожидался {expected_code}, получили {response.status_code}"

def check_schema(response_json: dict, model_class):
    """Стандартная Pydantic валидация"""
    validated = model_class.model_validate(response_json)

def check_time(response, max_seconds: float):
    """Проверка времени ответа"""
    elapsed = response.elapsed.total_seconds()
    assert elapsed <= max_seconds, f"Время {elapsed:.2f}s > {max_seconds}s"
