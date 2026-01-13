from pydantic import BaseModel, RootModel
from typing import List


class ModelItem(BaseModel):
    id: int
    title: str


class GetSearchHintsModel(RootModel[List[ModelItem]]):
    """Схема ответа со списком контента"""
    root: List[ModelItem]