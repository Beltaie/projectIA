import uuid
from datetime import datetime
from models.user import User, CandidateProfile
from models.application import Application, ApplicationReview, InterviewSlot
from models.chat import ChatSession


def test_user_instantiation():
    user = User(
        id=uuid.uuid4(),
        email="test.candidate@smartcampus.tn",
        password_hash="hashed_pw_123",
        role="CANDIDAT",
        first_name="Ahmed",
        last_name="Mansour",
        phone="+216 20 111 222",
        is_active=True,
    )
    assert user.email == "test.candidate@smartcampus.tn"
    assert user.role == "CANDIDAT"
    assert user.institution_id is None


def test_candidate_profile_instantiation():
    user_id = uuid.uuid4()
    profile = CandidateProfile(
        user_id=user_id,
        bac_type="Mathématiques",
        bac_year=2025,
        bac_average=16.85,
        current_level="Terminale / Bac",
        target_campus="IIT",
        career_objective="Cycle Ingénieur en Génie Logiciel",
        confidence_score=90,
    )
    assert profile.bac_type == "Mathématiques"
    assert profile.bac_average == 16.85
    assert profile.confidence_score == 90
    assert profile.target_campus == "IIT"


def test_application_instantiation():
    app = Application(
        application_number="APP-2026-IIT-0099",
        candidate_id=uuid.uuid4(),
        program_id=3,
        academic_year="2026/2027",
        status="SUBMITTED",
        motivation_text="Motivation pour le cycle ingénieur IIT",
        qcm_score=95.0,
    )
    assert app.application_number == "APP-2026-IIT-0099"
    assert app.status == "SUBMITTED"
    assert app.qcm_score == 95.0


def test_review_and_interview_instantiation():
    rev = ApplicationReview(
        application_id=1,
        reviewer_id=uuid.uuid4(),
        decision="ACCEPTED",
        comments="Candidat excellent",
        score=19.0,
    )
    assert rev.decision == "ACCEPTED"
    assert rev.score == 19.0

    slot = InterviewSlot(
        application_id=1,
        interviewer_id=rev.reviewer_id,
        scheduled_at=datetime.now(),
        duration_minutes=30,
        modality="ONLINE",
        status="CONFIRMED",
    )
    assert slot.duration_minutes == 30
    assert slot.modality == "ONLINE"
    assert slot.status == "CONFIRMED"


def test_chat_session_guest_to_candidate_bridge():
    session = ChatSession(
        token_hash="a" * 64,
        expires_at=datetime.now(),
        user_id=None,
        claimed_at=None,
    )
    assert session.user_id is None
    # Simulate claiming by candidate
    candidate_id = uuid.uuid4()
    session.user_id = candidate_id
    session.claimed_at = datetime.now()
    assert session.user_id == candidate_id
    assert session.claimed_at is not None
