from pydantic import BaseModel

class PostGuestLogin(BaseModel):
    token: str