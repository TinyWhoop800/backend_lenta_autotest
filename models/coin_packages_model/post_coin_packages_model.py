from pydantic import BaseModel

class PostCoinPackagesModel(BaseModel):
    payment_link: str
