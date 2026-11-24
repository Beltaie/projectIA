from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import (
    Boolean, CheckConstraint, Date, DateTime, ForeignKey,
    Numeric, SmallInteger, String, Text, UniqueConstraint, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Institution(Base):
    __tablename__ = "institutions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name_fr: Mapped[str] = mapped_column(Text, nullable=False)
    name_ar: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    programs: Mapped[List["Program"]] = relationship("Program", back_populates="institution")

class Program(Base):
    __tablename__ = "programs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    name_fr: Mapped[str] = mapped_column(Text, nullable=False)
    name_ar: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    track: Mapped[str] = mapped_column(String(20), nullable=False)
    duration_years: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    language_of_instruction: Mapped[str] = mapped_column(String(10), nullable=False)
    description_fr: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description_ar: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    career_outcomes_fr: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    career_outcomes_ar: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    institution: Mapped["Institution"] = relationship("Institution", back_populates="programs")
    admission_conditions: Mapped[List["AdmissionCondition"]] = relationship("AdmissionCondition", back_populates="program", cascade="all, delete-orphan")
    tuition_fees: Mapped[List["TuitionFee"]] = relationship("TuitionFee", back_populates="program", cascade="all, delete-orphan")
    deadlines: Mapped[List["Deadline"]] = relationship("Deadline", back_populates="program", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("track IN ('LICENCE','PREPA','INGENIEUR','AUTRE')", name="chk_prog_track"),
        CheckConstraint("language_of_instruction IN ('FR','EN')", name="chk_prog_lang"),
        CheckConstraint("duration_years BETWEEN 1 AND 8", name="chk_prog_duration"),
    )

class ProgramPathway(Base):
    __tablename__ = "program_pathways"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    from_program_id: Mapped[int] = mapped_column(ForeignKey("programs.id", ondelete="CASCADE"), nullable=False, index=True)
    to_program_id: Mapped[int] = mapped_column(ForeignKey("programs.id", ondelete="CASCADE"), nullable=False, index=True)
    conditions_fr: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    conditions_ar: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("from_program_id", "to_program_id", name="uq_program_pathway"),
        CheckConstraint("from_program_id <> to_program_id", name="chk_diff_pathway"),
    )

class AdmissionCondition(Base):
    __tablename__ = "admission_conditions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("programs.id", ondelete="CASCADE"), nullable=False, index=True)
    academic_year: Mapped[str] = mapped_column(String(9), nullable=False, index=True)
    required_diploma: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    condition_fr: Mapped[str] = mapped_column(Text, nullable=False)
    condition_ar: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    program: Mapped["Program"] = relationship("Program", back_populates="admission_conditions")

class TuitionFee(Base):
    __tablename__ = "tuition_fees"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("programs.id", ondelete="CASCADE"), nullable=False, index=True)
    academic_year: Mapped[str] = mapped_column(String(9), nullable=False, index=True)
    fee_type: Mapped[str] = mapped_column(String(30), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="TND", nullable=False)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    program: Mapped["Program"] = relationship("Program", back_populates="tuition_fees")
    promotions: Mapped[List["FeePromotion"]] = relationship("FeePromotion", back_populates="tuition_fee", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("program_id", "academic_year", "fee_type", name="uq_fee_program_year_type"),
        CheckConstraint("fee_type IN ('INSCRIPTION','ANNUEL','SEMESTRIEL','DOSSIER')", name="chk_fee_type"),
        CheckConstraint("amount >= 0", name="chk_fee_amount"),
    )

class Deadline(Base):
    __tablename__ = "deadlines"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("programs.id", ondelete="CASCADE"), nullable=False, index=True)
    academic_year: Mapped[str] = mapped_column(String(9), nullable=False, index=True)
    deadline_type: Mapped[str] = mapped_column(String(30), nullable=False)
    deadline_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    program: Mapped["Program"] = relationship("Program", back_populates="deadlines")

    __table_args__ = (
        UniqueConstraint("program_id", "academic_year", "deadline_type", name="uq_deadline_program_year_type"),
        CheckConstraint("deadline_type IN ('DEPOT_DOSSIER','CONCOURS','ENTRETIEN','RESULTATS','INSCRIPTION')", name="chk_deadline_type"),
    )

class FeePromotion(Base):
    __tablename__ = "fee_promotions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tuition_fee_id: Mapped[int] = mapped_column(ForeignKey("tuition_fees.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    condition_fr: Mapped[str] = mapped_column(Text, nullable=False)
    condition_ar: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    discount_type: Mapped[str] = mapped_column(String(20), nullable=False)
    discount_value: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    tuition_fee: Mapped["TuitionFee"] = relationship("TuitionFee", back_populates="promotions")

    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="chk_promo_dates"),
        CheckConstraint("discount_type IN ('PERCENTAGE','FIXED')", name="chk_promo_type"),
        CheckConstraint("discount_value > 0", name="chk_promo_value"),
    )
