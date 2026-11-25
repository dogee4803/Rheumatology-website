# app/models/diary.py
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from app.db.database import Base
from app.models.enums import DataSource, IntakeStatus, ReminderType
from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    ForeignKey,
    Index,
    Numeric,
    SmallInteger,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import BYTEA, JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column


class SymptomEntry(Base):
    __tablename__ = "symptom_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    entry_date: Mapped[date] = mapped_column(Date, nullable=False)
    pain_vas: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    morning_stiffness_min: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    swollen_joints_selfreport: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    painful_joints_selfreport: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    fatigue_vas: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    flares: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notes_enc: Mapped[bytes | None] = mapped_column(BYTEA, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("pain_vas BETWEEN 0 AND 10", name="ck_symptom_pain_vas"),
        CheckConstraint(
            "morning_stiffness_min BETWEEN 0 AND 1440",
            name="ck_symptom_morning_stiffness",
        ),
        CheckConstraint(
            "swollen_joints_selfreport >= 0", name="ck_symptom_swollen_joints"
        ),
        CheckConstraint(
            "painful_joints_selfreport >= 0", name="ck_symptom_painful_joints"
        ),
        CheckConstraint("fatigue_vas BETWEEN 0 AND 10", name="ck_symptom_fatigue_vas"),
        UniqueConstraint("user_id", "entry_date", name="uq_symptom_entry_per_day"),
        Index("ix_symptom_entries_user_date", "user_id", text("entry_date DESC")),
    )


class Medication(Base):
    __tablename__ = "medications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    dose: Mapped[str | None] = mapped_column(Text, nullable=True)
    schedule: Mapped[dict] = mapped_column(JSONB, nullable=False)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)


class MedicationIntakeLog(Base):
    __tablename__ = "medication_intake_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    medication_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("medications.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    scheduled_date: Mapped[date] = mapped_column(Date, nullable=False)
    taken_at: Mapped[datetime | None] = mapped_column(nullable=True)
    status: Mapped[IntakeStatus] = mapped_column(nullable=False)
    reason_skipped: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("medication_id", "scheduled_date", name="uq_intake_log"),
        Index("ix_intake_log_user_date", "user_id", "scheduled_date"),
    )


class LabResult(Base):
    __tablename__ = "lab_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    test_code: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    unit: Mapped[str | None] = mapped_column(Text, nullable=True)
    lab_date: Mapped[date] = mapped_column(Date, nullable=False)
    reference_range: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    entered_by: Mapped[DataSource] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    __table_args__ = (Index("ix_lab_results_user_date", "user_id", "lab_date"),)


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    visit_date: Mapped[date] = mapped_column(Date, nullable=False)
    doctor_specialty: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes_enc: Mapped[bytes | None] = mapped_column(BYTEA, nullable=True)
    next_visit_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[ReminderType] = mapped_column(nullable=False)
    related_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    scheduled_at: Mapped[datetime] = mapped_column(nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="pending")


class ReportExport(Base):
    __tablename__ = "report_exports"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    file_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    downloaded_at: Mapped[datetime | None] = mapped_column(nullable=True)
