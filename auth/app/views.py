from passlib import context
import fastapi
from fastapi import security
import typing
import app
import datetime
import jose
import asyncio
import models
import crud
import app.schemas as schemas

router = fastapi.APIRouter(prefix=f'{app.PREFIX}/auth')
pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")

async def init_models():
    async with app.engine.begin() as conn:
        await conn.run_sync(app.base.metadata.create_all)

async def destroy_models():
    async with app.engine.begin() as conn:
        await conn.run_sync(app.base.metadata.drop_all)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_access_token(data: dict, expires: datetime.timedelta|None = None):
    to_encode = data.copy()
    if expires:
        expire = datetime.utcnow() + expires
    else:
        expire = datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jose.jwt.encode(to_encode, app.SECRET_KEY, algorithm=app.HS256)

    return encoded_jwt

async def authenticate(
            db: asyncio.AsyncSession,
            username: str = ...,
            email: str = ...,
            phone: str = ...,
            password: str = ...,        
        ) -> models.User|None:
    user = None
    if not isinstance(username, ...):
        user = await crud.get_user(db, username=username)
    elif not isinstance(username, ...):
        user = await crud.get_user(db, user_email=email)
    elif not isinstance(phone, ...):
        user = await crud.get_user(db, phone=phone)
    if user is None:
        return user
    return user if verify_password(password, user.hashed_password) else None

@router.post('/get_token', response_model=schemas.Token)
async def get_token(
            form_data: typing.Annotated[security.OAuth2PasswordRequestForm, fastapi.Depends()],
            db: asyncio.AsyncSession = fastapi.Depends(crud.get_session),
        ):
    username = form_data.username
    password = form_data.password
    
    user = await authenticate(db, username=username, password=password)
    if user is None:
        raise fastapi.HTTPException(
            status_code=401,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        
    token = ...
        
    return {
        'error': False,
        'access_token': token,
        'token_type': 'beares',
    }