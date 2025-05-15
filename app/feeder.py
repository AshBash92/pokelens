import asyncio
import aiohttp

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models import engine
from app.schemas import CardCreate
from app.crud import create_card

API_URL = "https://api.pokemontcg.io/v2/cards"

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def fetch_cards():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            data = await response.json()
            return data['data']

async def save_cards_to_db():
    cards_data = await fetch_cards()

    async with async_session() as db:
        for card in cards_data[:10]:  # Limit to first 10 cards
            market_price = card.get('cardmarket', {}).get('prices', {}).get('averageSellPrice')
            
            if market_price is None:
                continue  # Skip cards without market price

            card_obj = CardCreate(
                id=card['id'],
                name=card['name'],
                rarity=card.get('rarity', 'Unknown'),
                market_price=market_price
            )

            try:
                from app.crud import upsert_card
                await upsert_card(db, card_obj)

                print(f"Saved: {card['name']}")
            except Exception as e:
                print(f"Error saving {card['name']}: {e}")

if __name__ == "__main__":
    asyncio.run(save_cards_to_db())