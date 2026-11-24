import logging
import os
import hashlib
from datetime import date
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config.settings import settings

logger = logging.getLogger("smartcampus.database")


class Base(DeclarativeBase):
    pass


def _simple_hash(password: str) -> str:
    salt = os.urandom(16).hex()
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return f"pbkdf2:sha256:100000${salt}${dk.hex()}"


def _init_sqlite_demo_data(target_engine):
    """Seed demo data in SQLite so local development works immediately without Docker."""
    from models.catalog import (
        AdmissionCondition,
        Deadline,
        FeePromotion,
        Institution,
        Program,
        TuitionFee,
    )
    from models.user import User

    Base.metadata.create_all(bind=target_engine)
    Session = sessionmaker(bind=target_engine)
    with Session() as db:
        if db.scalar(select(Institution).limit(1)) is not None:
            return

        iit = Institution(
            code="IIT",
            name_fr="Institut International de Technologie",
            name_ar="الجامعة الدولية للتكنولوجيا",
        )
        isb = Institution(
            code="ISB",
            name_fr="École Internationale Supérieure Privée des Affaires de Sfax",
            name_ar="المدرسة العليا الدولية للتصرف",
        )
        db.add_all([iit, isb])
        db.flush()

        p1 = Program(
            institution_id=iit.id,
            code="LIC-INFO-FR",
            name_fr="Licence en Informatique",
            name_ar="إجازة في الإعلامية",
            track="LICENCE",
            duration_years=3,
            language_of_instruction="FR",
            description_fr="Formation en développement logiciel, systèmes et réseaux.",
            career_outcomes_fr="Développeur web/mobile, administrateur systèmes.",
        )
        p2 = Program(
            institution_id=iit.id,
            code="PREPA-INT-FR",
            name_fr="Cycle Préparatoire Intégré",
            name_ar="سنة تحضيرية",
            track="PREPA",
            duration_years=2,
            language_of_instruction="FR",
            description_fr="Deux années de tronc commun scientifique pour accès direct au cycle ingénieur.",
            career_outcomes_fr="Accès direct au cycle ingénieur.",
        )
        p3 = Program(
            institution_id=iit.id,
            code="ING-IA-FR",
            name_fr="Cycle Ingénieur Intelligence Artificielle",
            name_ar="مهندس ذكاء اصطناci",
            track="INGENIEUR",
            duration_years=3,
            language_of_instruction="FR",
            description_fr="Formation d'ingénieur d'élite orientée IA, machine learning et vision.",
            career_outcomes_fr="Ingénieur IA, Data Scientist, MLOps.",
        )
        p4 = Program(
            institution_id=isb.id,
            code="LIC-GESTION-FR",
            name_fr="Licence en Gestion",
            name_ar="إجازة في التصرف",
            track="LICENCE",
            duration_years=3,
            language_of_instruction="FR",
            description_fr="Formation en management, finance et marketing digital.",
            career_outcomes_fr="Gestionnaire, consultant d'affaires.",
        )
        db.add_all([p1, p2, p3, p4])
        db.flush()

        db.add_all([
            TuitionFee(program_id=p1.id, academic_year="2026/2027", fee_type="ANNUEL", amount=3500.0, currency="TND", source="OFFICIAL CATALOG"),
            TuitionFee(program_id=p2.id, academic_year="2026/2027", fee_type="ANNUEL", amount=4000.0, currency="TND", source="OFFICIAL CATALOG"),
            TuitionFee(program_id=p3.id, academic_year="2026/2027", fee_type="ANNUEL", amount=6000.0, currency="TND", source="OFFICIAL CATALOG"),
            TuitionFee(program_id=p4.id, academic_year="2026/2027", fee_type="ANNUEL", amount=3000.0, currency="TND", source="OFFICIAL CATALOG"),
        ])
        db.flush()

        db.add_all([
            AdmissionCondition(program_id=p1.id, academic_year="2026/2027", required_diploma="Baccalauréat", condition_fr="Dossier scolaire et moyenne minimale.", source="OFFICIAL RULES"),
            AdmissionCondition(program_id=p3.id, academic_year="2026/2027", required_diploma="Prépa ou Licence", condition_fr="Admissibilité sur concours ou dossier + entretien.", source="OFFICIAL RULES"),
            Deadline(program_id=p1.id, academic_year="2026/2027", deadline_type="DEPOT_DOSSIER", deadline_date=date(2027, 7, 15), source="OFFICIAL CALENDAR"),
            Deadline(program_id=p3.id, academic_year="2026/2027", deadline_type="DEPOT_DOSSIER", deadline_date=date(2027, 6, 30), source="OFFICIAL CALENDAR"),
        ])

        db.add_all([
            User(email="admin@smartcampus.tn", password_hash=_simple_hash("adminsecret"), role="ADMINISTRATEUR", first_name="Super", last_name="Admin"),
            User(email="responsable.iit@smartcampus.tn", password_hash=_simple_hash("iitsecret"), role="RESPONSABLE", first_name="Karim", last_name="Trabelsi", institution_id=iit.id),
        ])
        db.commit()


def _get_engine():
    target_url = settings.database_url
    try:
        eng = create_engine(target_url, pool_pre_ping=True, connect_args={"connect_timeout": 1} if "postgresql" in target_url else {})
        with eng.connect() as conn:
            pass
        return eng
    except Exception:
        sqlite_path = os.path.join(os.path.dirname(__file__), "smartcampus_local.db")
        sqlite_url = f"sqlite:///{sqlite_path}"
        eng = create_engine(sqlite_url, connect_args={"check_same_thread": False})
        _init_sqlite_demo_data(eng)
        return eng


engine = _get_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db():
    """One DB session per request, always closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
