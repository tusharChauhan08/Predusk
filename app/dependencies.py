from app.db.session import SessionLocal
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

# DB SESSION DEPENDENCY
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session