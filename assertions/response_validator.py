import allure
from pydantic import BaseModel, ValidationError
from typing import Type, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


@allure.step("Проверить статус код: ожидается {expected_code}")
def check_status(response, expected_code: int, message: str = "") -> None:
    """
    Проверка статус кода.

    Args:
        response: requests.Response
        expected_code: Ожидаемый статус код
        message: Дополнительное сообщение об ошибке

    Raises:
        AssertionError: Если статус код не совпадает
    """
    assert response.status_code == expected_code, \
        f"Ожидался {expected_code}, получили {response.status_code}. {message}"
    logger.debug(f"Status code check passed: {expected_code}")


@allure.step("Проверить JSON схему:")
def check_schema(
        response_json,
        model_class: Type[BaseModel]
) -> BaseModel:
    """
    Валидация JSON через Pydantic и возврат объекта.

    Args:
        response_json: Словарь, список или другие данные для валидации
        model_class: Pydantic модель

    Returns:
        BaseModel: Валидированный объект

    Raises:
        AssertionError: Если валидация не прошла
    """
    try:
        validated = model_class.model_validate(response_json)
        logger.debug(f"Schema validation passed")
        return validated
    except ValidationError as e:
        error_details = "\n".join([
            f"Field: {err.get('loc', ('root',))[0]}, Error: {err['msg']}"
            for err in e.errors()
        ])
        allure.attach(
            error_details,
            name="Schema Validation Errors",
            attachment_type=allure.attachment_type.TEXT
        )
        logger.error(f"Schema validation failed:\n{error_details}")
        # ← Вот это ключевое изменение
        raise AssertionError(f"Schema validation failed:\n{error_details}") from e


@allure.step("Проверить время ответа: < {max_seconds}s")
def check_time(response, max_seconds: float) -> float:
    """
    Проверка времени ответа.

    Args:
        response: requests.Response
        max_seconds: Максимально допустимое время в секундах

    Returns:
        float: Время ответа в секундах

    Raises:
        AssertionError: Если время ответа превышает лимит
    """
    elapsed = response.elapsed.total_seconds()
    assert elapsed <= max_seconds, \
        f"Время ответа {elapsed:.2f}s превышает лимит {max_seconds}s"
    logger.debug(f"Response time check passed: {elapsed:.3f}s <= {max_seconds}s")
    return elapsed


@allure.step("Проверить количество элементов: {key} == {expected_count}")
def check_array_length(
        response_json: Any,
        expected_count: int,
        key: Optional[str] = None
) -> int:
    """
    Проверить количество элементов в массиве или объекте.

    Args:
        response_json: JSON ответ (список или словарь)
        expected_count: Ожидаемое количество элементов
        key: Опциональный ключ для вложенного массива (поддерживает nested: "data.items")
             Если не указан, считает корневой массив/объект

    Returns:
        int: Фактическое количество элементов

    Raises:
        AssertionError: Если количество не совпадает
    """
    if key:
        # Поддержка nested ключей: "data.items"
        keys = key.split(".")
        actual_array = response_json

        try:
            for k in keys:
                actual_array = actual_array[k]
        except (KeyError, TypeError, IndexError):
            raise AssertionError(f"Key '{key}' not found in response")
    else:
        actual_array = response_json

    # Считаем элементы в зависимости от типа
    if isinstance(actual_array, (list, dict)):
        actual_count = len(actual_array)
    else:
        raise AssertionError(f"Expected list or dict, got {type(actual_array).__name__}")

    assert actual_count == expected_count, \
        f"Expected {expected_count} elements, got {actual_count}"

    logger.debug(f"Array length check passed: {actual_count} == {expected_count}")
    return actual_count


@allure.step("Проверить значение в JSON: {key} == {expected_value}")
def check_json_value(
        response_json: dict,
        key: str,
        expected_value: Any,
        case_sensitive: bool = True
) -> Any:
    """
    Проверить конкретное значение в JSON ответе.

    Args:
        response_json: Словарь ответа
        key: Ключ (поддерживает nested: "data.user.id")
        expected_value: Ожидаемое значение
        case_sensitive: Учитывать ли регистр для строк

    Returns:
        Any: Найденное значение
    """
    # Поддержка nested ключей: "data.user.id"
    keys = key.split(".")
    actual_value = response_json

    try:
        for k in keys:
            actual_value = actual_value[k]
    except (KeyError, TypeError):
        raise AssertionError(f"Key '{key}' not found in response")

    # Сравнение с учётом case sensitivity
    if isinstance(expected_value, str) and isinstance(actual_value, str):
        if not case_sensitive:
            expected_value = expected_value.lower()
            actual_value = actual_value.lower()

    assert actual_value == expected_value, \
        f"Expected {key}={expected_value}, got {actual_value}"
    logger.debug(f"JSON value check passed: {key}={actual_value}")
    return actual_value


@allure.step("Проверить наличие ключей: {keys}")
def check_json_keys(response_json: dict, keys: list) -> None:
    """
    Проверить наличие всех ключей в JSON ответе.

    Args:
        response_json: Словарь ответа
        keys: Список ключей для проверки

    Raises:
        AssertionError: Если какой-то ключ отсутствует
    """
    missing_keys = [k for k in keys if k not in response_json]
    assert not missing_keys, f"Missing keys in response: {missing_keys}"
    logger.debug(f"All required keys present: {keys}")


@allure.step("Проверить HTTP Header: {header_name}")
def check_header(response, header_name: str, expected_value: Optional[str] = None) -> str:
    """
    Проверить наличие и значение HTTP header.

    Args:
        response: requests.Response
        header_name: Название header
        expected_value: Ожидаемое значение (опционально)

    Returns:
        str: Значение header
    """
    assert header_name in response.headers, \
        f"Header '{header_name}' not found. Available: {list(response.headers.keys())}"

    actual_value = response.headers[header_name]

    if expected_value is not None:
        assert actual_value == expected_value, \
            f"Header '{header_name}': expected '{expected_value}', got '{actual_value}'"

    logger.debug(f"Header check passed: {header_name}={actual_value}")
    return actual_value
