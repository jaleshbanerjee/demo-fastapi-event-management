from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/eventdb"

# For SQLite (file-based DB)
DATABASE_URL = "sqlite+aiosqlite:///./event.db"


engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
