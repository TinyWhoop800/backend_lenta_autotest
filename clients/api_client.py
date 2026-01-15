import requests
from typing import Union, Optional, Dict, Any
from api.endpoints import Endpoints
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import allure
import logging

logger = logging.getLogger(__name__)


class APIClient:
    """
    API клиент с встроенным управлением headers и токенами.
    """

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

        # Применяем дефолтные headers к сессии
        self.session.headers.update(self.default_headers)

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

    def _get_headers(self, with_auth: bool = True) -> Dict[str, str]:
        """
        Берём дефолтные headers из self.default_headers
        """
        headers = self.session.headers.copy()
        if with_auth and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _prepare_url(
            self,
            endpoint: Union[str, Endpoints],
            path_params: Optional[Dict[str, Any]] = None  # ← path_params вместо url_params
    ) -> str:
        """Подготовить URL с подстановкой PATH параметров"""
        if isinstance(endpoint, Endpoints):
            endpoint = endpoint.value

        if path_params:
            try:
                endpoint = endpoint.format(**path_params)
            except KeyError as e:
                raise ValueError(f"Missing URL parameter: {e}") from e

        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url}{endpoint}"

    def get(
            self,
            endpoint: Union[str, Endpoints],
            with_auth: bool = True,
            path_params: Optional[Dict[str, Any]] = None,
            query_params: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> requests.Response:
        """
        GET запрос.

        Args:
            endpoint: Endpoint или Enum
            with_auth: Добавлять ли Authorization header
            path_params: Параметры для подстановки в URL path (типа /contents/{id})
            query_params: Query параметры (типа ?page=1&limit=10)
            **kwargs: Остальные параметры для requests.get()
        """
        url = self._prepare_url(endpoint, path_params)
        headers = self._get_headers(with_auth)
        logger.debug(f"GET {url}")
        return self.session.get(url, headers=headers, params=query_params, **kwargs)

    def post(
            self,
            endpoint: Union[str, Endpoints],
            with_auth: bool = True,
            path_params: Optional[Dict[str, Any]] = None,
            query_params: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> requests.Response:
        """
        POST запрос.

        Args:
            endpoint: Endpoint или Enum
            with_auth: Добавлять ли Authorization header
            path_params: Параметры для подстановки в URL path
            query_params: Query параметры
            **kwargs: Остальные параметры для requests.post()
        """
        url = self._prepare_url(endpoint, path_params)
        headers = self._get_headers(with_auth)
        logger.debug(f"POST {url}")
        return self.session.post(url, headers=headers, params=query_params, **kwargs)

    def delete(
            self,
            endpoint: Union[str, Endpoints],
            with_auth: bool = True,
            path_params: Optional[Dict[str, Any]] = None,
            query_params: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> requests.Response:
        """
        DELETE запрос.

        Args:
            endpoint: Endpoint или Enum
            with_auth: Добавлять ли Authorization header
            path_params: Параметры для подстановки в URL path
            query_params: Query параметры
            **kwargs: Остальные параметры для requests.delete()
        """
        url = self._prepare_url(endpoint, path_params)
        headers = self._get_headers(with_auth)
        logger.debug(f"DELETE {url}")
        return self.session.delete(url, headers=headers, params=query_params, **kwargs)

    def close(self):
        """Закрыть сессию"""
        self.session.close()
        logger.debug("API Client session closed")
