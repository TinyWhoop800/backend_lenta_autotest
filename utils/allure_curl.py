import allure
import curlify

def attach_curl(response, name: str = "curl"):
    """Добавляет curl-запрос в Allure как attachment."""
    curl_cmd = curlify.to_curl(response.request)
    allure.attach(
        curl_cmd,
        name=name,
        attachment_type=allure.attachment_type.TEXT
    )