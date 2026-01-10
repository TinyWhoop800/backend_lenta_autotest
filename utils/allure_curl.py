# utils/allure_curl.py
import allure
import curlify
import logging

logger = logging.getLogger(__name__)


def attach_curl(response, name: str = "curl", log_level: str = "debug") -> str:
    """
    Добавляет curl-запрос в Allure как attachment и логирует.

    Args:
        response: requests.Response объект
        name: Название attachment в Allure
        log_level: Уровень логирования (debug, info)

    Returns:
        curl_cmd: Строка curl-команды
    """
    curl_cmd = curlify.to_curl(response.request)

    # Attach to Allure
    allure.attach(
        curl_cmd,
        name=name,
        attachment_type=allure.attachment_type.TEXT
    )

    # Log to console/file
    log_func = getattr(logger, log_level, logger.debug)
    log_func(f"\n{name}:\n{curl_cmd}")

    return curl_cmd


def attach_response_details(response, name: str = "Response Details") -> None:
    """
    Добавляет полные детали ответа в Allure (status, headers, body, elapsed time).

    Args:
        response: requests.Response объект
        name: Название attachment
    """
    details = f"""
Status Code: {response.status_code}
Elapsed Time: {response.elapsed.total_seconds():.3f}s

Headers:
{format_dict(response.headers)}

Body:
{response.text[:2000]}
"""
    allure.attach(
        details,
        name=name,
        attachment_type=allure.attachment_type.TEXT
    )


def format_dict(d: dict, indent: int = 2) -> str:
    """Форматировать dict для читаемости"""
    return "\n".join(f"{' ' * indent}{k}: {v}" for k, v in d.items())
