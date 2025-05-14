from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Card
from .schemas import CardCreate

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

async def create_card(db: AsyncSession, card_data: CardCreate) -> Card:
    card = Card(**card_data.dict())
    db.add(card)
    await db.commit()
    await db.refresh(card)
    return card

async def get_all_cards(db: AsyncSession):
    result = await db.execute(select(Card))
    return result.scalars().all()