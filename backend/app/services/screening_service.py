from uuid import uuid4

from app.models.screening import ScreeningSession
from sqlalchemy.ext.asyncio import AsyncSession


async def create_session(db: AsyncSession) -> ScreeningSession:
    session = ScreeningSession(session_token=uuid4())
    db.add(session)
    await db.flush()
    return session