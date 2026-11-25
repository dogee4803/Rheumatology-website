# app/models/screening.py
from datetime import datetime
from uuid import UUID, uuid4

from app.db.database import Base
from app.models.enums import ScreeningLevel, SessionStatus
from sqlalchemy import (
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, TEXT
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column


class ScreeningSession(Base):
    __tablename__ = "screening_sessions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    session_token: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), unique=True, nullable=False
    )
    user_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus, name="session_status"),
        nullable=False,
        default=SessionStatus.in_progress,
    )
    started_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (Index("ix_screening_sessions_token", "session_token"),)


class ScreeningAnswer(Base):
    __tablename__ = "screening_answers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("screening_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_code: Mapped[str] = mapped_column(String(8), nullable=False)
    value: Mapped[dict] = mapped_column(JSONB, nullable=False)
    weighted_score: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("session_id", "question_code", name="uq_screening_answer"),
    )


class ScreeningResult(Base):
    __tablename__ = "screening_results"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    session_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("screening_sessions.id"),
        unique=True,
        nullable=False,
    )
    block_scores: Mapped[dict] = mapped_column(JSONB, nullable=False)
    total_score: Mapped[int] = mapped_column(Integer, nullable=False)
    red_flag_codes: Mapped[list[str]] = mapped_column(
        ARRAY(TEXT),
        nullable=False,
        default=list,
        server_default=text("'{}'::text[]"),
    )
    level: Mapped[ScreeningLevel] = mapped_column(
        Enum(ScreeningLevel, name="screening_level"), nullable=False
    )
    weights_version: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
