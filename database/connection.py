from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from contextlib import asynccontextmanager
from database.models import Base
from configs.config import settings



engine = None
AsyncSessionLocal = None
 

def init_engine(database_url: str = None, echo: bool = False, **kwargs):

    global engine, AsyncSessionLocal
    if database_url is None:
        database_url = settings.DATABASE_URL
    engine = create_async_engine(database_url, echo=echo, **kwargs)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    if engine is None or AsyncSessionLocal is None:
        raise RuntimeError("Engine or AsyncSessionLocal failed to initialize")


async def init_db():

    if engine is None:
        raise Exception("Engine not started. Should call init_engine() before init_db().")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



@asynccontextmanager
def get_engine():
    if engine is None:
        raise RuntimeError("❌ Engine not initialized. Call init_engine() before start using database.")
    yield engine


@asynccontextmanager
async def get_session():
    if AsyncSessionLocal is None:
        raise RuntimeError("❌ Session maker not initialized. Call init_engine() before start using database.")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def database():
    """Asynchronous context manager for database session handling."""
    if AsyncSessionLocal is None:
        raise Exception("Session maker not initialized. Call init_engine() before using database.")
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()