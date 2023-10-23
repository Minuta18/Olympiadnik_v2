from passlib import context
import fastapi
import app

router = fastapi.APIRouter(prefix=f'{app.PREFIX}/users')
pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")

async def init_models():
    async with app.engine.begin() as conn:
        await conn.run_sync(app.base.metadata.create_all)

async def destroy_models():
    async with app.engine.begin() as conn:
        await conn.run_sync(app.base.metadata.drop_all)
