import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class CandidateProfileCreate(BaseModel):
    bac_type: Optional[str] = None
    bac_year: Optional[int] = Field(None, ge=1990, le=2035)
    bac_average: Optional[float] = Field(None, ge=0, le=20)
    current_level: Optional[str] = None
    target_campus: Optional[str] = None
    career_objective: Optional[str] = None

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: Optional[str] = None
    profile: Optional[CandidateProfileCreate] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class CandidateProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    bac_type: Optional[str] = None
    bac_year: Optional[int] = None
    bac_average: Optional[float] = None
    current_level: Optional[str] = None
    target_campus: Optional[str] = None
    career_objective: Optional[str] = None
    confidence_score: int

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    email: str
    role: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    institution_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    profile: Optional[CandidateProfileOut] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
