from typing import List, Optional

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
    countEpisodes: int
    lastEpisodeId: Optional[int] = None
    lastEpisodeNumber: Optional[int] = None
    genres: List[Genres]
    isFavorite: bool
    favoritesCount: int
    hasTrailer: bool
    countAvailableEpisodes: int
    countPaidEpisodes: int


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
    links: List[Link]  # нет описания в схеме ответа
    path: str
    per_page: int
    to: int
    total: int
    collectionId: int


class GetCollectionsCollectionContentsModel(BaseModel):
    data: List[Datum]
    links: Links
    meta: Meta
