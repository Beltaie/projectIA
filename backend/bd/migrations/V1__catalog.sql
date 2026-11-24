-- V1: academic catalog (SA-12)
--
-- Conventions:
--  * A program taught in two languages is stored as two rows (one per language).
--    The language goes in `code`, e.g. 'GL-FR' and 'GL-EN'. Fees, deadlines and
--    admission conditions point at one program row, so they need no extra structure.
--  * academic_year has the form '2026/2027' (second year = first year + 1).
--  * A promotion is valid when today is between start_date and end_date.
--    There is no on/off flag: to stop a promotion early, change its end_date.
--  

-- Reusable type: 'YYYY/YYYY' where the second year follows the first.
CREATE DOMAIN academic_year AS VARCHAR(9)
  CHECK (
    CASE
      WHEN VALUE ~ '^\d{4}/\d{4}$'
        THEN substr(VALUE, 6, 4)::int = substr(VALUE, 1, 4)::int + 1
      ELSE FALSE
    END
  );

-- Keeps updated_at truthful on every UPDATE.
CREATE FUNCTION set_updated_at() RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE institutions (
  id      SERIAL PRIMARY KEY,
  code    VARCHAR(10) NOT NULL UNIQUE,
  name_fr TEXT NOT NULL,
  name_ar TEXT
);

CREATE TABLE programs (
  id                      SERIAL PRIMARY KEY,
  institution_id          INT          NOT NULL REFERENCES institutions(id),
  code                    VARCHAR(30)  NOT NULL UNIQUE,
  name_fr                 TEXT         NOT NULL,
  name_ar                 TEXT,
  track                   VARCHAR(20)  NOT NULL
                          CHECK (track IN ('LICENCE','PREPA','INGENIEUR','AUTRE')),
  duration_years          SMALLINT     CHECK (duration_years BETWEEN 1 AND 8),
  language_of_instruction VARCHAR(10)  NOT NULL
                          CHECK (language_of_instruction IN ('FR','EN')),
  description_fr          TEXT,
  description_ar          TEXT,
  career_outcomes_fr      TEXT,
  career_outcomes_ar      TEXT,
  is_active               BOOLEAN      NOT NULL DEFAULT TRUE,
  created_at              TIMESTAMPTZ  NOT NULL DEFAULT now(),
  updated_at              TIMESTAMPTZ  NOT NULL DEFAULT now()
  -- Uncomment ONLY if the team agrees every code ends with '-FR' or '-EN':
  -- , CONSTRAINT chk_code_language
  --     CHECK (right(code, 3) = '-' || language_of_instruction)
);

CREATE TRIGGER trg_programs_updated_at
  BEFORE UPDATE ON programs
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE program_pathways (
  id              SERIAL PRIMARY KEY,
  from_program_id INT NOT NULL REFERENCES programs(id) ON DELETE CASCADE,
  to_program_id   INT NOT NULL REFERENCES programs(id) ON DELETE CASCADE,
  conditions_fr   TEXT,
  conditions_ar   TEXT,
  CHECK (from_program_id <> to_program_id),
  UNIQUE (from_program_id, to_program_id)
);

CREATE TABLE admission_conditions (
  id               SERIAL PRIMARY KEY,
  program_id       INT           NOT NULL REFERENCES programs(id) ON DELETE CASCADE,
  academic_year    academic_year NOT NULL,
  required_diploma TEXT,
  condition_fr     TEXT          NOT NULL,
  condition_ar     TEXT,
  source           TEXT          NOT NULL,
  created_at       TIMESTAMPTZ   NOT NULL DEFAULT now()
);

CREATE TABLE tuition_fees (
  id            SERIAL PRIMARY KEY,
  program_id    INT           NOT NULL REFERENCES programs(id) ON DELETE CASCADE,
  academic_year academic_year NOT NULL,
  fee_type      VARCHAR(30)   NOT NULL
                CHECK (fee_type IN ('INSCRIPTION','ANNUEL','SEMESTRIEL','DOSSIER')),
  amount        NUMERIC(10,2) NOT NULL CHECK (amount >= 0),
  currency      CHAR(3)       NOT NULL DEFAULT 'TND',
  source        TEXT          NOT NULL,
  created_at    TIMESTAMPTZ   NOT NULL DEFAULT now(),
  UNIQUE (program_id, academic_year, fee_type)
);

CREATE TABLE deadlines (
  id            SERIAL PRIMARY KEY,
  program_id    INT           NOT NULL REFERENCES programs(id) ON DELETE CASCADE,
  academic_year academic_year NOT NULL,
  deadline_type VARCHAR(30)   NOT NULL
                CHECK (deadline_type IN ('DEPOT_DOSSIER','CONCOURS','ENTRETIEN','RESULTATS','INSCRIPTION')),
  deadline_date DATE          NOT NULL,
  notes         TEXT,
  source        TEXT          NOT NULL,
  created_at    TIMESTAMPTZ   NOT NULL DEFAULT now(),
  UNIQUE (program_id, academic_year, deadline_type)
);

CREATE TABLE fee_promotions (
  id             SERIAL PRIMARY KEY,
  tuition_fee_id INT           NOT NULL REFERENCES tuition_fees(id) ON DELETE CASCADE,
  title          VARCHAR(150)  NOT NULL,
  condition_fr   TEXT          NOT NULL,  -- e.g. paiement de l'annee complete
  condition_ar   TEXT,
  discount_type  VARCHAR(20)   NOT NULL
                 CHECK (discount_type IN ('PERCENTAGE','FIXED')),
  discount_value NUMERIC(10,2) NOT NULL CHECK (discount_value > 0),
  start_date     DATE          NOT NULL,
  end_date       DATE          NOT NULL,
  source         TEXT          NOT NULL,
  created_at     TIMESTAMPTZ   NOT NULL DEFAULT now(),
  CHECK (end_date >= start_date),
  CHECK (discount_type <> 'PERCENTAGE' OR discount_value <= 100)
);

CREATE INDEX idx_programs_institution    ON programs (institution_id);
CREATE INDEX idx_conditions_program_year ON admission_conditions (program_id, academic_year);
CREATE INDEX idx_fees_program_year       ON tuition_fees (program_id, academic_year);
CREATE INDEX idx_deadlines_program_year  ON deadlines (program_id, academic_year);
CREATE INDEX idx_promotions_tuition_fee  ON fee_promotions (tuition_fee_id);