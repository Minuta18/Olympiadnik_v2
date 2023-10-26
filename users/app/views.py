from passlib import context
import fastapi
import enum
from app import schemas
import app
from app import crud
from sqlalchemy import exc
from sqlalchemy.ext import asyncio
import re

router = fastapi.APIRouter(prefix=f'{app.PREFIX}/users')
pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")

EMAIL_VALIDATION = re.compile(r'''^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$''')
PHONE_VALIDATION = re.compile(r'''^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$''')

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

class Permissions(enum.Enum):
    default = 0
    teacher = 1
    admin = 2
    dev = 3

@router.post('/verify_password')
async def verify_password_endpoint(
        data: schemas.VerifyPasswordSchema,
        db: asyncio.AsyncSession = fastapi.Depends(crud.get_session),
    ):
    user = None
    if data.username is not None:
        user = crud.get_user(db, username=data.username)
    elif data.email is not None:
        user = crud.get_user(db, email=data.email)
    elif data.phone is not None:
        user = crud.get_user(db, phone=data.phone)
    else:
        raise fastapi.responses.JSONResponse(content={
            'error': True,
            'message': 'Username, email or phone is required',
        }, status_code=400)
    if verify_password(data.password, user.hashed_password):
        return {
            'error': False,
            'message': 'Password is correct'
        }
    else:
        return {
            'error': True,
            'message': 'Password is incorrect'
        }
    
@router.post('/create')
async def create_user(
        data: schemas.CreateUserSchema,
        db: asyncio.AsyncSession = fastapi.Depends(crud.get_session),
    ):
    try:
        if re.match(EMAIL_VALIDATION, data.email) == None:
            return fastapi.responses.JSONResponse(content={
                'error': True,
                'message': 'Invalid email'
            }, status_code=400)
        
        phone = ''.join([s for s in data.phone if s.isdigit()])
        if re.match(PHONE_VALIDATION, data.phone) == None:
            return fastapi.responses.JSONResponse(content={
                'error': True,
               'message': 'Invalid phone'
            }, status_code=400)

        usr = crud.create_user(
            db,
            email=data.email,
            phone=phone,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            middle_name=data.middle_name,
            hashed_password=get_password_hash(data.password),
            permissions=Permissions.default.value,
            is_active=1,
            is_deleted=False,
            is_banned=False,
            is_confirmed=False,
        )

        return {
            'error': False, 'id': usr.id, 'email': usr.email, 'phone': usr.phone,
            'username': usr.username, 'first_name': usr.first_name,
            'last_name': usr.last_name, 'middle_name': usr.middle_name,
            'hashed_password': usr.hashed_password, 'permissions': usr.permissions,
            'is_active': usr.is_active, 'is_deleted': usr.is_deleted,
            'is_banned': usr.is_banned, 'is_confirmed': usr.is_confirmed,
            'created_at': usr.created_at.isoformat(),
            'updated_at': usr.updated_at.isoformat(),
        }
    except exc.IntegrityError as e:
        raise fastapi.responses.JSONResponse(content={
            'error': True,
            'message': 'Username, email or phone already exists',
        }, status_code=400)
