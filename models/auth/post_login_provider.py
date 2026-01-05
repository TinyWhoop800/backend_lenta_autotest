from pydantic import BaseModel

class PostLoginProvider(BaseModel):
    token: str