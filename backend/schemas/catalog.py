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
