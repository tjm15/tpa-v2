from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_async_engine(str(settings.database_url), echo=True, future=True)

# Use sessionmaker to create AsyncSession factory
AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency for FastAPI
async def get_db():
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        yield session
