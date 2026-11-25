from datetime import datetime
from uuid import UUID, uuid4

from app.db.database import Base
from app.models.enums import Sex, UserRole
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    LargeBinary,
    SmallInteger,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    email_hash: Mapped[bytes] = mapped_column(LargeBinary, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(default=UserRole.patient, nullable=False)
    consent_version: Mapped[str] = mapped_column(String, nullable=False)
    consent_accepted_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

class PatientProfile(Base):
    __tablename__ = "patient_profiles"
    __table_args__ = (
        CheckConstraint("year_of_birth BETWEEN 1920 AND 2025", name="ck_year_of_birth"),
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    year_of_birth: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    sex: Mapped[Sex | None] = mapped_column(nullable=True)
    diagnosis_code: Mapped[str | None] = mapped_column(String(8), nullable=True)
    diagnosis_confirmed_by_doctor: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )