from app.db.database import get_db
from app.schemas.screening import SessionCreateResponse
from app.services import questionnaire, screening_service
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/screening", tags=["screening"])

@router.get("/questionnaire")
async def get_questionnaire():
    """Отдает JSON-контракт анкеты"""
    return questionnaire.load_questionnaire()

@router.post("/sessions", response_model=SessionCreateResponse)
async def start_session(db: AsyncSession = Depends(get_db)):
    """Создает новую сессию для прохождения скрининга (гостевую)"""
    session = await screening_service.create_session(db)
    return SessionCreateResponse(
        session_token=session.session_token, 
        status=session.status.value
    )