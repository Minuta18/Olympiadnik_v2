from passlib import context
import fastapi
from fastapi import security
import typing
import app
import datetime
import jwt
import models
import crud
from sqlalchemy.ext import asyncio
import app.schemas as schemas

router = fastapi.APIRouter(prefix=f'{app.PREFIX}/auth')
pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")

async def init_models():
    async with app.engine.begin() as conn:
        await conn.run_sync(app.base.metadata.create_all)

async def destroy_models():
    async with app.engine.begin() as conn:
        await conn.run_sync(app.base.metadata.drop_all)

...
