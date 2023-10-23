from sqlalchemy.ext import asyncio
from sqlalchemy import exc
from app import models
import sqlalchemy as sql
import app

async def get_session() -> asyncio.AsyncSession:
    '''
    This FastApi dependency returns a asynchronous SQL session

    :return: a `asyncio.AsyncSession`
    '''

    async with app.session() as session:
        yield session

async def init_models():
    '''
    This function drop and create all tables
    '''

    async with app.engine.begin() as conn:
        await conn.run_sync(app.base.metadata.drop_all)
        await conn.run_sync(app.base.metadata.create_all)