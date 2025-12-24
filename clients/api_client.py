import requests
from typing import Union  # Добавьте этот импорт
from api.endpoints import Endpoints


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _prepare_url(self, endpoint: str) -> str:
        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url}{endpoint}"

    def post(self, endpoint: Union[str, Endpoints], **kwargs):
        # ЕСЛИ endpoint - это Enum, берем его значение
        if isinstance(endpoint, Endpoints):
            endpoint = endpoint.value
        url = self._prepare_url(endpoint)
        return self.session.post(url, **kwargs)

    def get(self, endpoint: Union[str, Endpoints], **kwargs):
        if isinstance(endpoint, Endpoints):
            endpoint = endpoint.value
        url = self._prepare_url(endpoint)
        return self.session.get(url, **kwargs)

    def delete(self, endpoint: Union[str, Endpoints], **kwargs):
        if isinstance(endpoint, Endpoints):
            endpoint = endpoint.value
        url = self._prepare_url(endpoint)
        return self.session.delete(url, **kwargs)

    def close(self):
        self.session.close()