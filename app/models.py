import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column

DB_USER = os.getenv("POSTGRES_USER", "cards")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "cards")
DB_NAME = os.getenv("POSTGRES_DB", "cards")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Card(Base):
    __tablename__ = 'cards'
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    rarity: Mapped[str]
    market_price: Mapped[float]