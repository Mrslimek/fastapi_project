from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from config import settings


# Такая строка называется DSN
DATABASE_URL = f"postgresql+asyncpg://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_HOST}/{settings.PG_NAME}"
# Созданной асинхронный движок для работы с psql
# Движок управляет соединением с бд, запросами в бд и управляет транзакциями
engine = create_async_engine(DATABASE_URL, echo=True)
# sessionmaker - фабрика, которая создает экземпяляры сессий
# expire_on_commit = False означает, что сессия не будет истекать после коммита
# TODO: Возможно, expire_on_commit стоит убрать,
# потому что, предположительно, у меня нет логики, при которой эта сессия нужна после коммита
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Получаем экземпляр сессии по требованию
async def get_db():
    async with SessionLocal() as session:
        yield session
