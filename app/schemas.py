from pydantic import BaseModel

class CardCreate(BaseModel):
    id: str
    name: str
    rarity: str
    market_price: float

class CardOut(BaseModel):
    id: str
    name: str
    rarity: str
    market_price: float

    class Config:
        orm_mode = True