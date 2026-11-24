-- V2: Users, Candidate Profiles, Applications, and Reviews (SA-17)
-- Assignee: EK (Erij Kacem)
-- Dependent on V1__catalog.sql (institutions, programs, academic_year domain, set_updated_at function)

-- Ensure pgcrypto or gen_random_uuid is available
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Central Users Table (Admins, Responsables IIT/ISB, Candidates)
CREATE TABLE users (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email           VARCHAR(255) NOT NULL UNIQUE,
  password_hash   VARCHAR(255) NOT NULL,
  role            VARCHAR(20)  NOT NULL
                  CHECK (role IN ('CANDIDAT', 'RESPONSABLE', 'ADMINISTRATEUR')),
  first_name      VARCHAR(100) NOT NULL,
  last_name       VARCHAR(100) NOT NULL,
  phone           VARCHAR(30),
  institution_id  INT          REFERENCES institutions(id) ON DELETE SET NULL,
  is_active       BOOLEAN      NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
  -- A Responsable must be tied to an institution; Candidates and Admins should not have one.
  CONSTRAINT chk_responsable_institution
    CHECK (
      (role = 'RESPONSABLE' AND institution_id IS NOT NULL) OR
      (role <> 'RESPONSABLE')
    )
);

CREATE TRIGGER trg_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- 2. Candidate Profiles (Progressive profiling data gathered via Chatbot or Form)
CREATE TABLE candidate_profiles (
  id                SERIAL PRIMARY KEY,
  user_id           UUID         NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  bac_type          VARCHAR(50),
  bac_year          SMALLINT     CHECK (bac_year BETWEEN 1990 AND 2035),
  bac_average       NUMERIC(4,2) CHECK (bac_average >= 0 AND bac_average <= 20),
  current_level     VARCHAR(50),
  target_campus     VARCHAR(10)  CHECK (target_campus IN ('IIT', 'ISB', 'ALL')),
  career_objective  TEXT,
  confidence_score  SMALLINT     DEFAULT 0 CHECK (confidence_score BETWEEN 0 AND 100),
  created_at        TIMESTAMPTZ  NOT NULL DEFAULT now(),
  updated_at        TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE TRIGGER trg_candidate_profiles_updated_at
  BEFORE UPDATE ON candidate_profiles
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- 3. Applications (Dossiers de Candidature & Préinscriptions)
CREATE TABLE applications (
  id                 SERIAL PRIMARY KEY,
  application_number VARCHAR(32)   NOT NULL UNIQUE,
  candidate_id       UUID          NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  program_id         INT           NOT NULL REFERENCES programs(id) ON DELETE RESTRICT,
  academic_year      academic_year NOT NULL,
  status             VARCHAR(35)   NOT NULL DEFAULT 'DRAFT'
                     CHECK (status IN (
                       'DRAFT',
                       'SUBMITTED',
                       'UNDER_REVIEW',
                       'INTERVIEW_REQUIRED',
                       'ACCEPTED',
                       'REJECTED',
                       'WAITLISTED',
                       'CANCELLED'
                     )),
  motivation_text    TEXT,
  qcm_score          NUMERIC(5,2)  CHECK (qcm_score >= 0 AND qcm_score <= 100),
  qcm_completed_at   TIMESTAMPTZ,
  submitted_at       TIMESTAMPTZ,
  created_at         TIMESTAMPTZ   NOT NULL DEFAULT now(),
  updated_at         TIMESTAMPTZ   NOT NULL DEFAULT now(),
  UNIQUE (candidate_id, program_id, academic_year)
);

CREATE TRIGGER trg_applications_updated_at
  BEFORE UPDATE ON applications
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- 4. Application Human Evaluations and Decisions
CREATE TABLE application_reviews (
  id             SERIAL PRIMARY KEY,
  application_id INT          NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  reviewer_id    UUID         NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  decision       VARCHAR(30)  NOT NULL
                 CHECK (decision IN ('ACCEPTED', 'REJECTED', 'INTERVIEW_REQUIRED', 'WAITLISTED')),
  comments       TEXT,
  score          NUMERIC(4,2) CHECK (score >= 0 AND score <= 20),
  decided_at     TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- 5. Admission Interview Slots
CREATE TABLE interview_slots (
  id               SERIAL PRIMARY KEY,
  application_id   INT         REFERENCES applications(id) ON DELETE SET NULL,
  interviewer_id   UUID        NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  scheduled_at     TIMESTAMPTZ NOT NULL,
  duration_minutes SMALLINT    NOT NULL DEFAULT 30 CHECK (duration_minutes BETWEEN 10 AND 180),
  modality         VARCHAR(20) NOT NULL DEFAULT 'ONLINE'
                   CHECK (modality IN ('ONLINE', 'PRESENTIAL')),
  location_or_link TEXT,
  status           VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED'
                   CHECK (status IN ('SCHEDULED', 'CONFIRMED', 'COMPLETED', 'CANCELLED', 'NO_SHOW')),
  interview_notes  TEXT,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 6. Link Anonymous Guest Chat Sessions to Registered Candidates (Bridge for SA-29)
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'chat_sessions') THEN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'chat_sessions' AND column_name = 'user_id') THEN
      ALTER TABLE chat_sessions
        ADD COLUMN user_id UUID REFERENCES users(id) ON DELETE SET NULL,
        ADD COLUMN claimed_at TIMESTAMPTZ;
    END IF;
  END IF;
END $$;

-- Performance Indexes
CREATE INDEX idx_users_email               ON users (email);
CREATE INDEX idx_users_role_inst           ON users (role, institution_id);
CREATE INDEX idx_candidate_profiles_user   ON candidate_profiles (user_id);
CREATE INDEX idx_applications_candidate    ON applications (candidate_id);
CREATE INDEX idx_applications_prog_status  ON applications (program_id, status);
CREATE INDEX idx_applications_year         ON applications (academic_year);
CREATE INDEX idx_reviews_application       ON application_reviews (application_id);
CREATE INDEX idx_interviews_application    ON interview_slots (application_id);
CREATE INDEX idx_interviews_scheduled      ON interview_slots (scheduled_at);
