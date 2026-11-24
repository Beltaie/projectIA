from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.errors import AppError
from database import get_db
from models.user import CandidateProfile, User
from schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserOut
from services.auth_service import create_access_token, get_current_user, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
def register_candidate(req: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new student candidate account."""
    existing = db.scalar(select(User).where(User.email == req.email.lower()))
    if existing:
        raise AppError("Un compte avec cet email existe déjà.", status_code=400, code="email_already_exists")

    user = User(
        email=req.email.lower(),
        password_hash=hash_password(req.password),
        role="CANDIDAT",
        first_name=req.first_name,
        last_name=req.last_name,
        phone=req.phone,
        institution_id=None,
    )
    db.add(user)
    db.flush()

    # Initial candidate profile
    profile_data = req.profile.model_dump() if req.profile else {}
    profile = CandidateProfile(
        user_id=user.id,
        bac_type=profile_data.get("bac_type"),
        bac_year=profile_data.get("bac_year"),
        bac_average=profile_data.get("bac_average"),
        current_level=profile_data.get("current_level"),
        target_campus=profile_data.get("target_campus"),
        career_objective=profile_data.get("career_objective"),
        confidence_score=40 if profile_data.get("bac_type") else 10,
    )
    db.add(profile)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id, user.role)
    return TokenResponse(access_token=token, user=user)


@router.post("/login", response_model=TokenResponse)
def login_user(req: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user (Candidate, Responsable, Administrator)."""
    user = db.scalar(select(User).where(User.email == req.email.lower()))
    if not user or not verify_password(req.password, user.password_hash):
        raise AppError("Identifiants incorrects.", status_code=401, code="invalid_credentials")

    if not user.is_active:
        raise AppError("Compte désactivé. Veuillez contacter l'administration.", status_code=403, code="account_disabled")

    token = create_access_token(user.id, user.role)
    return TokenResponse(access_token=token, user=user)


@router.get("/me", response_model=UserOut)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Return profile details of the authenticated user."""
    return current_user
