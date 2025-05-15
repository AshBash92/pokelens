from pydantic import BaseModel

class CardCreate(BaseModel):
    id: str
    name: str
    rarity: str
    market_price: float

    model_config = {
        'from_attributes': True
    }

class CardOut(BaseModel):
    id: str
    name: str
    rarity: str
    market_price: float

    model_config = {
        'from_attributes': True
    }