from typing import List, Optional
from pydantic import BaseModel

class Genres(BaseModel):
    id: int
    title: str

class GetContentsContentModel(BaseModel):
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
