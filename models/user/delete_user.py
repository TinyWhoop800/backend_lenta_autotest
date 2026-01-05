from pydantic import BaseModel


class DeleteUserData(BaseModel):
    userId: int

class DeleteUser(BaseModel):
    message: str
    data: DeleteUserData