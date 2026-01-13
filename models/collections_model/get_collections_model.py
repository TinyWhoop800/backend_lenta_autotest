from pydantic import BaseModel, Field
from typing import List, Optional


class Datum(BaseModel):
    id: int
    title: str
    type: str
    contentCount: int
    description: Optional[str] = None
    urlAlias: Optional[str] = None


class Links(BaseModel):
    first: str
    last: str
    prev: Optional[str] = None
    next: Optional[str] = None


class Link(BaseModel):
    url: Optional[str]
    label: str
    active: bool


class Meta(BaseModel):
    current_page: int
    from_: int = Field(..., alias='from')
    last_page: int
    links: List[Link] # Нет в swagger
    path: str
    per_page: int
    to: int
    total: int


class GetCollectionsModel(BaseModel):
    data: List[Datum]
    links: Links
    meta: Meta
