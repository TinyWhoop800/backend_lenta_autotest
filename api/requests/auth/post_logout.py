from pydantic import BaseModel
from typing import List

class Datum(BaseModel):
    userId: int

class PostLogout(BaseModel):
    message: str
    data: List[Datum]