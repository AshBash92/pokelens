from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import models, crud, deps

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with models.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.get("/cards", response_model=List[crud.CardOut])
async def get_cards(db: AsyncSession = Depends(deps.get_db)):
    return await crud.get_all_cards(db)

@app.post("/cards", response_model=crud.CardOut)
async def add_card(card: crud.CardCreate, db: AsyncSession = Depends(deps.get_db)):
    return await crud.create_card(db, card)