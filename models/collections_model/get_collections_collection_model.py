from typing import Optional

from pydantic import BaseModel


class GetCollectionsCollectionModel(BaseModel):
    id: int
    title: str
    type: str
    contentCount: int
    description: Optional[str] = None
    urlAlias: Optional[str] = None
