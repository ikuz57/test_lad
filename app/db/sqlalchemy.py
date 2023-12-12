from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from core.config import settings as s


DATABASE_URL = (
    f'postgresql+asyncpg://{s.DB_USER}:{s.DB_PASS}@{s.DB_HOST}:{s.DB_PORT}/'
    f'{s.DB_NAME}'
)

async_engine = create_async_engine(DATABASE_URL, echo=True)

async_session_factory = async_sessionmaker(async_engine)
