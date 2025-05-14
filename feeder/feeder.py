import aiohttp, asyncio

API_URL = "https://api.pokemontcg.io/v2/cards"

async def fetch_cards():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            data = await response.json()
            for card in data['data'][:10]:
                print(f"{card['name']} - Market Price: {card.get('cardmarket', {}).get('prices', {}).get('averageSellPrice')}")

if __name__ == "__main__":
    asyncio.run(fetch_cards())