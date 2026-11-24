import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
from models.catalog import (
    AdmissionCondition,
    Deadline,
    FeePromotion,
    Institution,
    Program,
    TuitionFee,
)
from models.chat import ChatMessage, ChatSession
from models.user import CandidateProfile, User
from services.auth_service import hash_password

# In-memory SQLite test database for reliable and isolated API testing
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()

    # Seed institutions
    iit = Institution(code="IIT", name_fr="Institut International de Technologie", name_ar="الجامعة الدولية للتكنولوجيا")
    isb = Institution(code="ISB", name_fr="École Internationale Supérieure Privée des Affaires", name_ar="المدرسة العليا الدولية للتصرف")
    db.add_all([iit, isb])
    db.flush()

    # Seed programs
    prog1 = Program(
        institution_id=iit.id,
        code="ING-IA-FR",
        name_fr="Cycle Ingénieur en Intelligence Artificielle",
        name_ar="مهندس ذكاء اصطناعي",
        track="INGENIEUR",
        duration_years=3,
        language_of_instruction="FR",
        description_fr="Formation avancée en IA et vision par ordinateur.",
    )
    prog2 = Program(
        institution_id=iit.id,
        code="PREPA-INT-FR",
        name_fr="Cycle Préparatoire Intégré",
        track="PREPA",
        duration_years=2,
        language_of_instruction="FR",
    )
    prog3 = Program(
        institution_id=isb.id,
        code="LIC-GESTION-FR",
        name_fr="Licence en Gestion",
        track="LICENCE",
        duration_years=3,
        language_of_instruction="FR",
    )
    db.add_all([prog1, prog2, prog3])
    db.flush()

    # Seed fees
    fee1 = TuitionFee(
        program_id=prog1.id,
        academic_year="2026/2027",
        fee_type="ANNUEL",
        amount=6000.0,
        currency="TND",
        source="OFFICIAL CATALOG",
    )
    db.add(fee1)

    # Seed conditions & deadlines
    cond1 = AdmissionCondition(
        program_id=prog1.id,
        academic_year="2026/2027",
        required_diploma="Prépa ou Licence",
        condition_fr="Admission sur dossier et entretien",
        source="OFFICIAL RULES",
    )
    from datetime import date
    dl1 = Deadline(
        program_id=prog1.id,
        academic_year="2026/2027",
        deadline_type="DEPOT_DOSSIER",
        deadline_date=date(2027, 6, 30),
        source="OFFICIAL CALENDAR",
    )
    db.add_all([cond1, dl1])

    # Seed existing user
    user = User(
        email="test.student@smartcampus.tn",
        password_hash=hash_password("password123"),
        role="CANDIDAT",
        first_name="Farah",
        last_name="Bouzid",
        phone="+216 22 333 444",
    )
    db.add(user)
    db.commit()
    db.close()

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    return TestClient(app)


# =========================================================================
# SA-20 & SA-21 Test Suite (Catalogue, Tarifs, Délais)
# =========================================================================

def test_list_institutions(client):
    response = client.get("/api/institutions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    codes = [inst["code"] for inst in data]
    assert "IIT" in codes
    assert "ISB" in codes


def test_list_programs_with_filters(client):
    response = client.get("/api/programs?track=INGENIEUR")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["code"] == "ING-IA-FR"
    assert data[0]["institution_code"] == "IIT"


def test_get_program_detail_and_404(client):
    response = client.get("/api/programs/1")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "ING-IA-FR"
    assert "admission_conditions" in data
    assert "tuition_fees" in data
    assert "deadlines" in data

    # 404 test
    not_found = client.get("/api/programs/9999")
    assert not_found.status_code == 404
    assert not_found.json()["error"]["code"] == "program_not_found"


def test_get_program_fees_and_conditions(client):
    fees = client.get("/api/programs/1/fees?year=2026/2027")
    assert fees.status_code == 200
    fee_data = fees.json()
    assert len(fee_data) >= 1
    assert fee_data[0]["amount"] == 6000.0
    assert fee_data[0]["currency"] == "TND"

    conds = client.get("/api/programs/1/admission-conditions?year=2026/2027")
    assert conds.status_code == 200
    assert len(conds.json()) >= 1

    deadlines = client.get("/api/programs/1/deadlines?year=2026/2027")
    assert deadlines.status_code == 200
    assert len(deadlines.json()) >= 1


# =========================================================================
# SA-28 Test Suite (Authentification & Rôles)
# =========================================================================

def test_register_and_login_candidate(client):
    reg_payload = {
        "email": "new.candidate@gmail.com",
        "password": "mypassword123",
        "first_name": "Sami",
        "last_name": "Gharbi",
        "phone": "+216 99 888 777",
        "profile": {
            "bac_type": "Mathématiques",
            "bac_year": 2025,
            "bac_average": 15.5,
            "target_campus": "IIT"
        }
    }
    reg_res = client.post("/api/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["email"] == "new.candidate@gmail.com"
    assert reg_data["user"]["role"] == "CANDIDAT"

    # Duplicate email
    dup_res = client.post("/api/auth/register", json=reg_payload)
    assert dup_res.status_code == 400
    assert dup_res.json()["error"]["code"] == "email_already_exists"

    # Login
    login_res = client.post("/api/auth/login", json={
        "email": "new.candidate@gmail.com",
        "password": "mypassword123"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    # Profile me
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["first_name"] == "Sami"


# =========================================================================
# SA-29 Test Suite (Liaison d'une conversation invitée à un compte candidat)
# =========================================================================

def test_claim_guest_session_by_candidate(client):
    # 1. Start a guest session
    sess_res = client.post("/api/chat/sessions")
    assert sess_res.status_code == 201
    sess_data = sess_res.json()
    session_id = sess_data["session_id"]
    token = sess_data["session_token"]

    # 2. Guest sends a message
    msg_res = client.post(
        f"/api/chat/sessions/{session_id}/messages",
        headers={"X-Session-Token": token},
        json={"content": "Je veux m'inscrire en génie logiciel IIT"}
    )
    assert msg_res.status_code == 201

    # 3. Candidate logs in
    login_res = client.post("/api/auth/login", json={
        "email": "test.student@smartcampus.tn",
        "password": "password123"
    })
    candidate_jwt = login_res.json()["access_token"]

    # 4. Candidate claims the session
    claim_res = client.post(
        f"/api/chat/sessions/{session_id}/claim",
        headers={
            "Authorization": f"Bearer {candidate_jwt}",
            "X-Session-Token": token
        }
    )
    assert claim_res.status_code == 200
    claim_data = claim_res.json()
    assert claim_data["status"] == "claimed"
    assert claim_data["message_count"] == 1
    assert "claimed_by_user_id" in claim_data

    # 5. Invalid token attempt on another claim
    fake_claim = client.post(
        f"/api/chat/sessions/{session_id}/claim",
        headers={
            "Authorization": f"Bearer {candidate_jwt}",
            "X-Session-Token": "invalid_wrong_token"
        }
    )
    assert fake_claim.status_code == 403
