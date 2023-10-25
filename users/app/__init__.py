from os import environ
from sqlalchemy.ext import declarative
from sqlalchemy.ext import asyncio
from sqlalchemy import orm
import logging
import dotenv
import datetime

dotenv.load_dotenv('./.env')

PREFIX = environ.get('PREFIX', default='/api')
TESTING = environ.get('TESTING', default='false') == 'true'

DATABASE_URL = 'postgresql+psycopg://{}:{}@{}:{}/{}'.format(
    environ.get('DB_USER', default='root'),  # Root is always exists
    environ.get('DB_PASSWORD', default=''),
    environ.get('DB_HOST', default='localhost'),
    environ.get('DB_PORT', default='3306'),  # Standard mysql port
    environ.get('DB_MAIN', default='main') if not TESTING
    else environ.get('DB_TEST', default='test'),
)

OPENAPI_URL = '{}/auth/openapi.json'.format(PREFIX)
DOCS_URL = '{}/auth/docs'.format(PREFIX)

ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=30)

# TODO: change secret key in production
SECRET_KEY = 'f7724738e073cb1ed50634eb8cb28ac9dcacbb2014f0f02f27bbf19c35e02bcc'
ALG = 'HS256'

# All database operations should be asynchronous to make service faster
engine = asyncio.create_async_engine(DATABASE_URL)
base = declarative.declarative_base()
session = orm.sessionmaker(
    bind=engine,
    class_=asyncio.AsyncSession,
    expire_on_commit=False
)

logger = logging.getLogger(__name__)