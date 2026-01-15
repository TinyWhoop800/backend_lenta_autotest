from typing import Any, List, Optional
from pydantic import BaseModel, Field


class Datum(BaseModel):
    id: int
    episodeNumber: int
    title: str
    streamUrl: Optional[str] = None
    previewImageUrl: str
    price: Any
    isLiked: bool
    likesCount: Any
    subtitles: Optional[str] = None
    titres: Optional[str] = None


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
    links: List[Link]  # Нет в свагере
    path: str
    per_page: int
    to: int
    total: int
    contentID: Any
    description: str


class GetContentsContentEpisodesModel(BaseModel):
    data: List[Datum]
    links: Links
    meta: Meta
