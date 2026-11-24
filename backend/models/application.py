from datetime import datetime
import uuid
from typing import Optional, List

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, SmallInteger, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    application_number: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False, index=True
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    program_id: Mapped[int] = mapped_column(
        ForeignKey("programs.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    academic_year: Mapped[str] = mapped_column(String(9), nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String(35), default="DRAFT", nullable=False, index=True
    )
    motivation_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    qcm_score: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    qcm_completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    candidate: Mapped["User"] = relationship("User", back_populates="applications")
    reviews: Mapped[List["ApplicationReview"]] = relationship(
        "ApplicationReview", back_populates="application", cascade="all, delete-orphan"
    )
    interviews: Mapped[List["InterviewSlot"]] = relationship(
        "InterviewSlot", back_populates="application"
    )

    __table_args__ = (
        UniqueConstraint("candidate_id", "program_id", "academic_year", name="uq_candidate_program_year"),
        CheckConstraint(
            "status IN ('DRAFT', 'SUBMITTED', 'UNDER_REVIEW', 'INTERVIEW_REQUIRED', 'ACCEPTED', 'REJECTED', 'WAITLISTED', 'CANCELLED')",
            name="chk_application_status",
        ),
        CheckConstraint("qcm_score IS NULL OR (qcm_score >= 0 AND qcm_score <= 100)", name="chk_application_qcm_score"),
    )


class ApplicationReview(Base):
    __tablename__ = "application_reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reviewer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    decision: Mapped[str] = mapped_column(String(30), nullable=False)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    score: Mapped[Optional[float]] = mapped_column(Numeric(4, 2), nullable=True)
    decided_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)

    # Relationships
    application: Mapped["Application"] = relationship("Application", back_populates="reviews")
    reviewer: Mapped["User"] = relationship("User")

    __table_args__ = (
        CheckConstraint(
            "decision IN ('ACCEPTED', 'REJECTED', 'INTERVIEW_REQUIRED', 'WAITLISTED')",
            name="chk_review_decision",
        ),
        CheckConstraint("score IS NULL OR (score >= 0 AND score <= 20)", name="chk_review_score"),
    )


class InterviewSlot(Base):
    __tablename__ = "interview_slots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    application_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("applications.id", ondelete="SET NULL"), nullable=True, index=True
    )
    interviewer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    scheduled_at: Mapped[datetime] = mapped_column(nullable=False, index=True)
    duration_minutes: Mapped[int] = mapped_column(SmallInteger, default=30, nullable=False)
    modality: Mapped[str] = mapped_column(String(20), default="ONLINE", nullable=False)
    location_or_link: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="SCHEDULED", nullable=False)
    interview_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)

    # Relationships
    application: Mapped[Optional["Application"]] = relationship("Application", back_populates="interviews")
    interviewer: Mapped["User"] = relationship("User")

    __table_args__ = (
        CheckConstraint("duration_minutes BETWEEN 10 AND 180", name="chk_interview_duration"),
        CheckConstraint("modality IN ('ONLINE', 'PRESENTIAL')", name="chk_interview_modality"),
        CheckConstraint(
            "status IN ('SCHEDULED', 'CONFIRMED', 'COMPLETED', 'CANCELLED', 'NO_SHOW')",
            name="chk_interview_status",
        ),
    )
