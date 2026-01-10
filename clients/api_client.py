import requests
from typing import Union, Optional, Dict, Any
from api.endpoints import Endpoints
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import allure
import logging

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(
            self,
            base_url: str,
            default_headers: Optional[Dict[str, str]] = None,
            retries: int = 3,
            backoff_factor: float = 0.3
    ):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.default_headers = default_headers or {}
        self.token = None

        # Настройка retry logic для 429 и других ошибок
        self._setup_retries(retries, backoff_factor)

    def _setup_retries(self, retries: int = 3, backoff_factor: float = 0.3) -> None:
        """Установить retry strategy для handling 429"""
        retry_strategy = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429],
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        logger.debug(f"Retries configured: {retries} retries, {backoff_factor}s backoff")

    def set_token(self, token: str) -> None:
        """Установить токен для всех последующих запросов"""
        self.token = token
        logger.debug(f"Token set (length: {len(token)})")

    def clear_token(self) -> None:
        """Очистить токен"""
        self.token = None
        logger.debug("Token cleared")

    def _get_headers(
            self,
            headers: Optional[Dict[str, str]] = None,
            with_auth: bool = True
    ) -> Dict[str, str]:
        """Объединить дефолтные хидеры с переданными"""
        result = self.default_headers.copy()
        if headers:
            result.update(headers)
        if with_auth and self.token:
            result["Authorization"] = f"Bearer {self.token}"
        return result

    def _prepare_url(
            self,
            endpoint: Union[str, Endpoints],
            url_params: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Подготовить URL с подстановкой параметров.

        Примеры:
            /episodes/{episode} + {episode: "123"} -> /episodes/123
            /collections/{collection}/contents + {collection: "abc"} -> /collections/abc/contents
        """
        if isinstance(endpoint, Endpoints):
            endpoint = endpoint.value

        # Подстановка параметров в URL
        if url_params:
            try:
                endpoint = endpoint.format(**url_params)
            except KeyError as e:
                raise ValueError(f"Missing URL parameter: {e}") from e

        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url}{endpoint}"

    @allure.step("POST {endpoint}")
    def post(
            self,
            endpoint: Union[str, Endpoints],
            headers: Optional[Dict[str, str]] = None,
            with_auth: bool = True,
            url_params: Optional[Dict[str, Any]] = None,
            **kwargs
    ):
        """
        POST запрос.

        Args:
            endpoint: Endpoint или Enum
            headers: Дополнительные хидеры
            with_auth: Добавлять ли Authorization header
            url_params: Параметры для подстановки в URL
            **kwargs: Остальные параметры для requests.post()
        """
        url = self._prepare_url(endpoint, url_params)
        final_headers = self._get_headers(headers, with_auth)
        logger.debug(f"POST {url}")
        return self.session.post(url, headers=final_headers, **kwargs)

    @allure.step("GET {endpoint}")
    def get(
            self,
            endpoint: Union[str, Endpoints],
            headers: Optional[Dict[str, str]] = None,
            with_auth: bool = True,
            url_params: Optional[Dict[str, Any]] = None,
            **kwargs
    ):
        """GET запрос"""
        url = self._prepare_url(endpoint, url_params)
        final_headers = self._get_headers(headers, with_auth)
        logger.debug(f"GET {url}")
        return self.session.get(url, headers=final_headers, **kwargs)

    @allure.step("DELETE {endpoint}")
    def delete(
            self,
            endpoint: Union[str, Endpoints],
            headers: Optional[Dict[str, str]] = None,
            with_auth: bool = True,
            url_params: Optional[Dict[str, Any]] = None,
            **kwargs
    ):
        """DELETE запрос"""
        url = self._prepare_url(endpoint, url_params)
        final_headers = self._get_headers(headers, with_auth)
        logger.debug(f"DELETE {url}")
        return self.session.delete(url, headers=final_headers, **kwargs)

    def close(self):
        """Закрыть сессию"""
        self.session.close()
        logger.debug("API Client session closed")
