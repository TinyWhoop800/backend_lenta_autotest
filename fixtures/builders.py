from models.post_logout import PostLogout
from typing import Any


class TestDataBuilder:
    def __init__(self, model_class):
        self.model_class = model_class
        self.data = {}

    def with_message(self, message: str) -> "TestDataBuilder":
        self.data["message"] = message
        return self

    def with_data(self, data: list) -> "TestDataBuilder":
        self.data["data"] = data
        return self

    def build(self) -> Any:
        return self.model_class(**self.data)
