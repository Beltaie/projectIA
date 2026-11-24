from datetime import datetime
import uuid
from typing import Optional, List

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Numeric, SmallInteger, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    institution_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("institutions.id", ondelete="SET NULL"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    profile: Mapped[Optional["CandidateProfile"]] = relationship(
        "CandidateProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    applications: Mapped[List["Application"]] = relationship(
        "Application", back_populates="candidate", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "role IN ('CANDIDAT', 'RESPONSABLE', 'ADMINISTRATEUR')",
            name="chk_user_role",
        ),
        CheckConstraint(
            "(role = 'RESPONSABLE' AND institution_id IS NOT NULL) OR (role <> 'RESPONSABLE')",
            name="chk_responsable_institution",
        ),
    )


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    bac_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    bac_year: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    bac_average: Mapped[Optional[float]] = mapped_column(Numeric(4, 2), nullable=True)
    current_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    target_campus: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    career_objective: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence_score: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="profile")

    __table_args__ = (
        CheckConstraint("bac_year BETWEEN 1990 AND 2035", name="chk_profile_bac_year"),
        CheckConstraint("bac_average >= 0 AND bac_average <= 20", name="chk_profile_bac_avg"),
        CheckConstraint("confidence_score BETWEEN 0 AND 100", name="chk_profile_confidence"),
        CheckConstraint(
            "target_campus IS NULL OR target_campus IN ('IIT', 'ISB', 'ALL')",
            name="chk_profile_campus",
        ),
    )
