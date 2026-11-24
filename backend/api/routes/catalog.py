from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from core.errors import AppError
from database import get_db
from models.catalog import AdmissionCondition, Deadline, FeePromotion, Institution, Program, TuitionFee
from models.user import User
from schemas.catalog import (
    AdmissionConditionOut, DeadlineOut, InstitutionOut,
    ProgramCreate, ProgramDetailOut, ProgramOut, TuitionFeeOut
)
from services.auth_service import require_roles

router = APIRouter(prefix="/api", tags=["catalog"])

# SA-20 : Formations et programmes
@router.get("/institutions", response_model=List[InstitutionOut])
def list_institutions(db: Session = Depends(get_db)):
    return db.scalars(select(Institution).order_by(Institution.id)).all()

@router.get("/programs", response_model=List[ProgramOut])
def list_programs(
    institution_id: Optional[int] = Query(None),
    track: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db),
):
    query = select(Program).join(Institution)
    if institution_id: query = query.where(Program.institution_id == institution_id)
    if track: query = query.where(Program.track == track.upper())
    if language: query = query.where(Program.language_of_instruction == language.upper())
    if active_only: query = query.where(Program.is_active.is_(True))

    programs = db.scalars(query.order_by(Program.id)).all()
    result = []
    for p in programs:
        out = ProgramOut.model_validate(p)
        out.institution_code = p.institution.code
        result.append(out)
    return result

@router.get("/programs/{program_id}", response_model=ProgramDetailOut)
def get_program_detail(program_id: int, db: Session = Depends(get_db)):
    program = db.scalar(
        select(Program)
        .options(
            selectinload(Program.institution),
            selectinload(Program.admission_conditions),
            selectinload(Program.tuition_fees).selectinload(TuitionFee.promotions),
            selectinload(Program.deadlines),
        )
        .where(Program.id == program_id)
    )
    if not program:
        raise AppError("Programme introuvable", status_code=404, code="program_not_found")
    out = ProgramDetailOut.model_validate(program)
    out.institution_code = program.institution.code
    return out

@router.post("/programs", status_code=status.HTTP_201_CREATED, response_model=ProgramOut)
def create_program(
    req: ProgramCreate,
    current_user: User = Depends(require_roles(["RESPONSABLE", "ADMINISTRATEUR"])),
    db: Session = Depends(get_db),
):
    if current_user.role == "RESPONSABLE" and current_user.institution_id != req.institution_id:
        raise AppError("Accès refusé. Vous ne pouvez gérer que votre propre institution.", status_code=403, code="forbidden_institution")

    existing = db.scalar(select(Program).where(Program.code == req.code))
    if existing:
        raise AppError("Un programme avec ce code existe déjà.", status_code=400, code="program_code_exists")

    prog = Program(**req.model_dump())
    db.add(prog)
    db.commit()
    db.refresh(prog)
    out = ProgramOut.model_validate(prog)
    out.institution_code = prog.institution.code if prog.institution else None
    return out

@router.get("/programs/{program_id}/fees", response_model=List[TuitionFeeOut])
def get_program_fees(program_id: int, year: str = Query("2026/2027"), db: Session = Depends(get_db)):
    return db.scalars(
        select(TuitionFee).options(selectinload(TuitionFee.promotions))
        .where(TuitionFee.program_id == program_id, TuitionFee.academic_year == year)
    ).all()

@router.get("/programs/{program_id}/admission-conditions", response_model=List[AdmissionConditionOut])
def get_program_admission_conditions(program_id: int, year: str = Query("2026/2027"), db: Session = Depends(get_db)):
    return db.scalars(select(AdmissionCondition).where(AdmissionCondition.program_id == program_id, AdmissionCondition.academic_year == year)).all()

@router.get("/programs/{program_id}/deadlines", response_model=List[DeadlineOut])
def get_program_deadlines(program_id: int, year: str = Query("2026/2027"), db: Session = Depends(get_db)):
    return db.scalars(select(Deadline).where(Deadline.program_id == program_id, Deadline.academic_year == year).order_by(Deadline.deadline_date)).all()
