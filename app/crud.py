from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

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

async def upsert_card(db: AsyncSession, card_data: CardCreate) -> Card:
    # Try to find the card first
    result = await db.execute(select(Card).where(Card.id == card_data.id))
    existing_card = result.scalar_one_or_none()

    if existing_card:
        # Card exists → update it
        existing_card.market_price = card_data.market_price
        db.add(existing_card)
        await db.commit()
        await db.refresh(existing_card)
        return existing_card
    else:
        # Card doesn't exist → insert new
        new_card = Card(**card_data.dict())
        db.add(new_card)
        await db.commit()
        await db.refresh(new_card)
        return new_card