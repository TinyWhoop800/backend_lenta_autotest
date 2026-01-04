from pydantic import BaseModel
from typing import List


class CoinPackage(BaseModel):
    id: str
    title: str
    price: str
    coins: int
    bonusCoins: int
    appStoreIdentifier: str
    googlePlayIdentifier: str


class GetCoinPackagesModel(BaseModel):
    coinPackages: List[CoinPackage]
    paymentMethod: str
