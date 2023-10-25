from passlib import context
import fastapi
import app
import datetime
import jose
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

@router.post('/get_token', response_model=schemas.Token)
def get_token():
    ...
