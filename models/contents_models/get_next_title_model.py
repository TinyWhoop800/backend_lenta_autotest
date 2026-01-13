from typing import Any, Optional
from pydantic import BaseModel


class GetNextTitleModel(BaseModel):
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