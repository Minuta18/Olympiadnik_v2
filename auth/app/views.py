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

async def init_models():
    async with app.engine.begin() as conn:
        await conn.run_sync(app.base.metadata.create_all)

async def destroy_models():
    async with app.engine.begin() as conn:
        await conn.run_sync(app.base.metadata.drop_all)

def generate_token(
        type: str,
        subject: typing.Any,
        payload: typing.Any,
        ttl: typing.Any,
    ):
    current_timestamp = datetime.datetime.utcnow().timestamp()
    data = {
        'iss': 'olimpiadnik.system@gmail.com',
        'sub': subject,
        'type': type,
        'iat': current_timestamp,
        'exp': payload['nbf'] if payload.get('nbf') else current_timestamp
    }
    data.update(dict(exp=data['nbf'] + int(ttl.total_seconds()))) if ttl else None
    payload.update(data)

    return jwt.encode(payload=payload, key=app.SECRET_KEY, algorithm='HS256')

async def login_by_access_token(
        db: asyncio.AsyncSession, 
        token: str
    ):
    try:
        payload = jwt.decode(token, app.SECRET_KEY, algorithms=['HS256'])
        if payload.get('type') != 'access':
            raise ValueError('This is not an access token')

        user = await crud.get_user(db, user_id=payload['sub'])
        return user
    except jwt.InvalidTokenError or KeyError:
        raise ValueError('Invalid access token')


@router.post('/get_token', response_model=schemas.Token)
async def get_token(
        form_data: typing.Annotated[security.OAuth2PasswordRequestForm, fastapi.Depends()],
        db: asyncio.AsyncSession = fastapi.Depends(crud.get_session),
    ):
    username = form_data.username
    password = form_data.password
    
    user = await authenticate(db, username=username, password=password) # TODO 
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