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

async def create_user(
        db: asyncio.AsyncSession,
        email: str = ...,
        phone: str = ...,
        username: str = ...,
        first_name: str = ...,
        last_name: str = ...,
        middle_name: str = ...,
        hashed_password: str = ...,
        permissions: int = ...,
        is_active: bool = ...,
        is_deleted: bool = ...,
        is_banned: bool = ...,
        is_confirmed: bool = ...,
    ) -> models.User:
    try:
        new_user = models.User(
            email=email,
            phone=phone,
            username=username,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            hashed_password=hashed_password,
            permissions=permissions,
            is_active=is_active,
            is_deleted=is_deleted,
            is_banned=is_banned,
            is_confirmed=is_confirmed,
        )

        db.add(new_user)
        await db.commit()

        return new_user
    except exc.IntegrityError as e:
        raise e

async def get_user(
        db: asyncio.AsyncSession, 
        user_id: int = ...,
        user_email: str = ...,
        username: str = ...,
        phone: str = ...,
    ) -> models.User:
    if user_id != ...:
        return await db.get(models.User, user_id)
    elif user_email != ...:
        return (await db.execute(sql.select(models.User).where(models.User.email == user_email))).scalars().first()
    elif username != ...:
        return (await db.execute(sql.select(models.User).where(models.User.username == username))).scalars().first()
    elif phone != ...:
        return (await db.execute(sql.select(models.User).where(models.User.phone == phone))).scalars().first()
    raise ValueError('Please specify user_id or user_email')

async def get_users(
        db: asyncio.AsyncSession, 
        start_id = ...,
        end_id = ...,
    ) -> list[models.User]:
    return (await db.execute(sql.select(models.User).offset(start_id).limit(
        abs(end_id - start_id) + 1
    ))).scalars().all()

async def update_user(
            db: asyncio.AsyncSession,
            user: models.User = ...,
            email: str = ...,
            phone: str = ...,
            username: str = ...,
            first_name: str = ...,
            last_name: str = ...,
            middle_name: str = ...,
            hashed_password: str = ...,
            permissions: int = ...,
            is_active: bool = ...,
            is_deleted: bool = ...,
            is_banned: bool = ...,
            is_confirmed: bool = ...,
        ) -> models.User:
    if email != ...:
        user.email = email
    if phone != ...:
        user.phone = phone
    if username != ...:
        user.username = username
    if first_name != ...:
        user.first_name = first_name
    if last_name != ...:
        user.last_name = last_name
    if middle_name != ...:
        user.middle_name = middle_name
    if hashed_password != ...:
        user.hashed_password = hashed_password
    if permissions != ...:
        user.permissions = permissions
    if is_active != ...:
        user.is_active = is_active
    if is_deleted != ...:
        user.is_deleted = is_deleted
    if is_banned != ...:
        user.is_banned = is_banned
    if is_confirmed != ...:
        user.is_confirmed = is_confirmed

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

async def delete_user(
            db: asyncio.AsyncSession,
            user: models.User =...,
        ):
    db.delete(user)
    await db.commit()
