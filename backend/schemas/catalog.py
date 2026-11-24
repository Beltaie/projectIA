from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class InstitutionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name_fr: str
    name_ar: Optional[str] = None


class ProgramBase(BaseModel):
    code: str
    name_fr: str
    name_ar: Optional[str] = None
    track: str
    duration_years: Optional[int] = None
    language_of_instruction: str
    description_fr: Optional[str] = None
    description_ar: Optional[str] = None
    career_outcomes_fr: Optional[str] = None
    career_outcomes_ar: Optional[str] = None
    is_active: bool = True


class ProgramCreate(ProgramBase):
    institution_id: int


class ProgramOut(ProgramBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution_id: int
    institution_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime


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


class ProgramDetailOut(ProgramOut):
    admission_conditions: List[AdmissionConditionOut] = []
    tuition_fees: List[TuitionFeeOut] = []
    deadlines: List[DeadlineOut] = []
