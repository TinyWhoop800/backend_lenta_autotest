from typing import Any, List, Optional
from pydantic import BaseModel, Field


class Datum(BaseModel):
    id: int
    title: str


class Links(BaseModel):
    first: str
    last: str
    prev: Optional[str] = None
    next: Optional[str] = None


class Meta(BaseModel):
    current_page: int
    from_: int = Field(..., alias='from')
    last_page: int
    # TODO: В ответе приходит еще Links
    path: str
    per_page: int
    to: int
    total: int


class GetGenresModel(BaseModel):
    data: List[Datum]
    links: Links
    meta: Meta
