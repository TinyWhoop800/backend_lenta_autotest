from pydantic import BaseModel


class LogoutData(BaseModel):
    userId: int

class Logout(BaseModel):
    message: str
    data: LogoutData