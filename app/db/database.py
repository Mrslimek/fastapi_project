from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app import config


# Такая строка называется DSN
DATABASE_URL = (
    f"postgresql+asyncpg://{config.PG_USER}:{config.PG_PASSWORD}@{config.PG_HOST}"
)
# Созданной асинхронный движок для работы с psql
# Движок управляет соединением с бд, запросами в бд и управляет транзакциями
engine = create_async_engine(DATABASE_URL, echo=True)
# sessionmaker - фабрика, которая создает экземпяляры сессий
# expire_on_commit = False означает, что сессия не будет истекать после коммита
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    # Здесь можно будет описать метаданные моделей
    pass


# Получаем экземпляр сессии по требованию
async def get_db():
    async with SessionLocal() as session:
        yield session
