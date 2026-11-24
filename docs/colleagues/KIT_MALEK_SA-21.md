# 📦 Kit Complet & Code Source pour Malek (MB)

| Tâche Assignée | Intitulé | Sprint |
|---|---|---|
| **SA-21** | Développer les API de consultation des tarifs et des conditions d'admission | Sprint 1 — Socle Technique |

---

## 👋 Salut Malek !
Voici le code source complet prêt à copier-coller dans tes fichiers et les commandes Git pour que ta tâche **SA-21** soit enregistrée et validée à ton nom sur GitHub.

---

# 🚀 TÂCHE SA-21 (API Tarifs, Conditions d'Admission & Délais)

### 1. Fichier : `backend/models/catalog.py`
Ajoute ou vérifie la présence de ces modèles dans `backend/models/catalog.py` :

```python
from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import (
    Boolean, CheckConstraint, Date, DateTime, ForeignKey,
    Numeric, SmallInteger, String, Text, UniqueConstraint, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class AdmissionCondition(Base):
    __tablename__ = "admission_conditions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("programs.id", ondelete="CASCADE"), nullable=False, index=True
    )
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
    program_id: Mapped[int] = mapped_column(
        ForeignKey("programs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    academic_year: Mapped[str] = mapped_column(String(9), nullable=False, index=True)
    fee_type: Mapped[str] = mapped_column(String(30), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="TND", nullable=False)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)

    program: Mapped["Program"] = relationship("Program", back_populates="tuition_fees")
    promotions: Mapped[List["FeePromotion"]] = relationship(
        "FeePromotion", back_populates="tuition_fee", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("program_id", "academic_year", "fee_type", name="uq_fee_program_year_type"),
        CheckConstraint("fee_type IN ('INSCRIPTION','ANNUEL','SEMESTRIEL','DOSSIER')", name="chk_fee_type"),
        CheckConstraint("amount >= 0", name="chk_fee_amount"),
    )


class Deadline(Base):
    __tablename__ = "deadlines"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("programs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    academic_year: Mapped[str] = mapped_column(String(9), nullable=False, index=True)
    deadline_type: Mapped[str] = mapped_column(String(30), nullable=False)
    deadline_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)

    program: Mapped["Program"] = relationship("Program", back_populates="deadlines")

    __table_args__ = (
        UniqueConstraint("program_id", "academic_year", "deadline_type", name="uq_deadline_program_year_type"),
        CheckConstraint(
            "deadline_type IN ('DEPOT_DOSSIER','CONCOURS','ENTRETIEN','RESULTATS','INSCRIPTION')",
            name="chk_deadline_type",
        ),
    )


class FeePromotion(Base):
    __tablename__ = "fee_promotions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tuition_fee_id: Mapped[int] = mapped_column(
        ForeignKey("tuition_fees.id", ondelete="CASCADE"), nullable=False, index=True
    )
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
```

---

### 2. Fichier : `backend/schemas/catalog.py`
Ajoute les schémas de sortie dans `backend/schemas/catalog.py` :

```python
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class FeePromotionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    condition_fr: str
    condition_ar: Optional[str] = None
    discount_type: str
    discount_value: float
    start_date: date
    end_date: date
    source: str

class TuitionFeeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    program_id: int
    academic_year: str
    fee_type: str
    amount: float
    currency: str
    source: str
    promotions: List[FeePromotionOut] = []

class AdmissionConditionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    program_id: int
    academic_year: str
    required_diploma: Optional[str] = None
    condition_fr: str
    condition_ar: Optional[str] = None
    source: str

class DeadlineOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    program_id: int
    academic_year: str
    deadline_type: str
    deadline_date: date
    notes: Optional[str] = None
    source: str
```

---

### 3. Fichier : `backend/api/routes/catalog.py`
Ajoute les routes de consultation dans `backend/api/routes/catalog.py` :

```python
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
```

---

### 4. Commandes Git pour SA-21 :

```bash
git checkout -b feature/SA-21-fees-admission-api
git add backend/models/catalog.py backend/schemas/catalog.py backend/api/routes/catalog.py
git commit -m "SA-21: developper les API de consultation des tarifs, promotions et conditions d'admission"
git push -u origin feature/SA-21-fees-admission-api
```
