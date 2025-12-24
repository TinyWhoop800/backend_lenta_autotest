from pydantic import BaseModel

def check_status(response, expected_code = 200):
    """Простая проверка статус кода"""
    assert response.status_code == expected_code, f"Ожидался {expected_code}, получили {response.status_code}. Ответ: {response.text}"

def check_schema(response, model: BaseModel):
    """Проверка по Pydantic модели"""
    data = response.json()
    validated = model(**data)
    return validated

def check_time(response, max_seconds: float = 1.0):
    """Проверка времени ответа"""
    response_time = response.elapsed.total_seconds()
    assert response_time < max_seconds, f"Response too slow: {response_time:.2f}s > {max_seconds}s"