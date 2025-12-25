import allure
from pydantic import BaseModel, ValidationError
from typing import Type, Dict, Any

@allure.step(f"Проверить статус код")
def check_status(response, expected_code: int):
    """Проверка статус кода"""
    assert response.status_code == expected_code, \
        f"Ожидался {expected_code}, получили {response.status_code}"

@allure.step("Проверить JSON схему")
def check_schema(response_json: dict, model_class):
    """Стандартная Pydantic валидация"""
    validated = model_class.model_validate(response_json)

@allure.step(f"Проверить время ответа")
def check_time(response, max_seconds: float):
    """Проверка времени ответа"""
    elapsed = response.elapsed.total_seconds()
    assert elapsed <= max_seconds, f"Время {elapsed:.2f}s > {max_seconds}s"
