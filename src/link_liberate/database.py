from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import aiosqlite
import asyncio

SQLALCHEMY_DATABASE_URL = "sqlite:///./liberate.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Session_Local = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()


async def create_async_session():
    async with aiosqlite.connect(SQLALCHEMY_DATABASE_URL) as db:
        yield db


async def expire_uuid(uuid):
    print("Expiring uuid:", uuid)
    await asyncio.sleep(60)  # Default expiration time is 60 mins
    async with create_async_session() as db:
        await db.execute("DELETE FROM liberatedlinks WHERE uuid = ?", (uuid,))
        await db.commit()
