from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from database import get_db
from models.catalog import AdmissionCondition, Deadline, FeePromotion, TuitionFee
from schemas.catalog import AdmissionConditionOut, DeadlineOut, TuitionFeeOut

# Ces routes complètent le routeur catalog (prefix="/api") :

@router.get("/programs/{program_id}/fees", response_model=List[TuitionFeeOut])
def get_program_fees(
    program_id: int,
    year: str = Query("2026/2027", description="Année académique (ex: 2026/2027)"),
    db: Session = Depends(get_db),
):
    """Consultation des frais de scolarité officiels et promotions."""
    fees = db.scalars(
        select(TuitionFee)
        .options(selectinload(TuitionFee.promotions))
        .where(TuitionFee.program_id == program_id, TuitionFee.academic_year == year)
    ).all()
    return fees


@router.get("/programs/{program_id}/admission-conditions", response_model=List[AdmissionConditionOut])
def get_program_admission_conditions(
    program_id: int,
    year: str = Query("2026/2027", description="Année académique (ex: 2026/2027)"),
    db: Session = Depends(get_db),
):
    """Consultation des conditions d'admission et diplômes prérequis."""
    conditions = db.scalars(
        select(AdmissionCondition)
        .where(AdmissionCondition.program_id == program_id, AdmissionCondition.academic_year == year)
    ).all()
    return conditions


@router.get("/programs/{program_id}/deadlines", response_model=List[DeadlineOut])
def get_program_deadlines(
    program_id: int,
    year: str = Query("2026/2027", description="Année académique (ex: 2026/2027)"),
    db: Session = Depends(get_db),
):
    """Consultation des dates limites et calendrier officiel."""
    deadlines = db.scalars(
        select(Deadline)
        .where(Deadline.program_id == program_id, Deadline.academic_year == year)
        .order_by(Deadline.deadline_date)
    ).all()
    return deadlines
