import asyncio

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.models import db
from config import POSTGRES_URI

async def connect():
    engine = create_engine(POSTGRES_URI)
    db.bind = engine
    if db.bind is None:
        raise ValueError("Failed to bind database")

    async def create_all_tables():
        await db.gino.create_all()

    await asyncio.to_thread(create_all_tables)

async def disconnect():
    await db.pop_bind().close()


def get_session() -> sessionmaker:
    return db.gino.create_engine()