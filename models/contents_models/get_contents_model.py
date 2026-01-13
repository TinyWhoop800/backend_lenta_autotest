# TODO: Нет ручки в swagger


from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Genres(BaseModel):
    id: int
    title: str


class Datum(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    releaseYear: Optional[str] = None
    urlAlias: Optional[str] = None
    poster: Optional[str] = None
    countEpisodes: Optional[int] = None
    lastEpisodeId: Optional[int] = None
    lastEpisodeNumber: Optional[int] = None
    genres: List[Genres]
    isFavorite: bool
    favoritesCount: Optional[int] = None
    hasTrailer: bool
    countAvailableEpisodes: Optional[int] = None
    countPaidEpisodes: Optional[int] = None


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


class GetContentsModel(BaseModel):
    data: List[Datum]
    links: Links
    meta: Meta
