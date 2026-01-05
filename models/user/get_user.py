from pydantic import BaseModel
from typing import Optional

class GetUser(BaseModel):
    id: Optional[str] = None
    uuid: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    language: Optional[str] = None
    provider_name: Optional[str] = None
    device_id: str
    is_guest: bool