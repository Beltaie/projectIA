-- V101: Demo Data for Users, Candidate Profiles, and Applications (SA-17)
-- Assignee: EK (Erij Kacem)
-- DEV ONLY: Demo data for local testing and end-to-end integration

-- Fixed UUIDs for predictable testing
-- Admin: 11111111-1111-1111-1111-111111111111
-- Responsable IIT: 22222222-2222-2222-2222-222222222222
-- Responsable ISB: 33333333-3333-3333-3333-333333333333
-- Candidate Mohamed Ben Salem: 44444444-4444-4444-4444-444444444444
-- Candidate Erij Kacem: 55555555-5555-5555-5555-555555555555

INSERT INTO users (id, email, password_hash, role, first_name, last_name, phone, institution_id)
SELECT '11111111-1111-1111-1111-111111111111'::uuid, 'admin@smartcampus.tn',
       'pbkdf2:sha256:600000$dummyhash$adminsecret', 'ADMINISTRATEUR', 'Super', 'Admin', '+216 74 000 000', NULL
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, email, password_hash, role, first_name, last_name, phone, institution_id)
SELECT '22222222-2222-2222-2222-222222222222'::uuid, 'responsable.iit@smartcampus.tn',
       'pbkdf2:sha256:600000$dummyhash$iitsecret', 'RESPONSABLE', 'Karim', 'Trabelsi', '+216 74 111 222', i.id
FROM institutions i WHERE i.code = 'IIT'
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, email, password_hash, role, first_name, last_name, phone, institution_id)
SELECT '33333333-3333-3333-3333-333333333333'::uuid, 'responsable.isb@smartcampus.tn',
       'pbkdf2:sha256:600000$dummyhash$isbsecret', 'RESPONSABLE', 'Sonia', 'Mezghani', '+216 74 333 444', i.id
FROM institutions i WHERE i.code = 'ISB'
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, email, password_hash, role, first_name, last_name, phone, institution_id)
VALUES
('44444444-4444-4444-4444-444444444444'::uuid, 'mohamed.bensalem@gmail.com',
 'pbkdf2:sha256:600000$dummyhash$candidate1', 'CANDIDAT', 'Mohamed', 'Ben Salem', '+216 98 123 456', NULL),
('55555555-5555-5555-5555-555555555555'::uuid, 'erij.kacem@gmail.com',
 'pbkdf2:sha256:600000$dummyhash$candidate2', 'CANDIDAT', 'Erij', 'Kacem', '+216 55 987 654', NULL)
ON CONFLICT (email) DO NOTHING;

-- Candidate Profiles
INSERT INTO candidate_profiles (user_id, bac_type, bac_year, bac_average, current_level, target_campus, career_objective, confidence_score)
VALUES
('44444444-4444-4444-4444-444444444444'::uuid, 'Sciences de l''Informatique', 2024, 15.75, 'Bac+2 / Prépa', 'IIT', 'Devenir ingénieur en intelligence artificielle et vision par ordinateur', 85),
('55555555-5555-5555-5555-555555555555'::uuid, 'Mathématiques', 2025, 16.20, 'Terminale / Bac', 'IIT', 'Poursuivre un cursus intégré en Génie Logiciel avec double diplomation nord-américaine', 95)
ON CONFLICT (user_id) DO NOTHING;

-- Applications (Dossiers)
INSERT INTO applications (application_number, candidate_id, program_id, academic_year, status, motivation_text, qcm_score, qcm_completed_at, submitted_at)
SELECT 'APP-2026-IIT-0001', '44444444-4444-4444-4444-444444444444'::uuid, p.id, '2026/2027',
       'UNDER_REVIEW', 'Passionné d''IA et désireux de rejoindre le cycle ingénieur IIT après ma prépa.', 92.50, now() - INTERVAL '2 days', now() - INTERVAL '2 days'
FROM programs p WHERE p.code = 'ING-IA-FR'
ON CONFLICT (application_number) DO NOTHING;

INSERT INTO applications (application_number, candidate_id, program_id, academic_year, status, motivation_text, qcm_score, qcm_completed_at, submitted_at)
SELECT 'APP-2026-IIT-0002', '55555555-5555-5555-5555-555555555555'::uuid, p.id, '2026/2027',
       'ACCEPTED', 'Très attirée par le modèle pédagogique par projets de l''IIT et les partenariats canadiens.', 98.00, now() - INTERVAL '5 days', now() - INTERVAL '5 days'
FROM programs p WHERE p.code = 'PREPA-INT-FR'
ON CONFLICT (application_number) DO NOTHING;

-- Application Review for Erij Kacem's accepted application
INSERT INTO application_reviews (application_id, reviewer_id, decision, comments, score)
SELECT a.id, '22222222-2222-2222-2222-222222222222'::uuid, 'ACCEPTED',
       'Excellent dossier scolaire en mathématiques, score QCM remarquable (98%). Avis très favorable pour la prépa intégrée.', 18.50
FROM applications a WHERE a.application_number = 'APP-2026-IIT-0002'
ON CONFLICT DO NOTHING;

-- Interview Slot for Mohamed Ben Salem
INSERT INTO interview_slots (application_id, interviewer_id, scheduled_at, duration_minutes, modality, location_or_link, status, interview_notes)
SELECT a.id, '22222222-2222-2222-2222-222222222222'::uuid, now() + INTERVAL '3 days', 30, 'ONLINE',
       'https://meet.google.com/iit-admission-interview', 'SCHEDULED', 'Entretien technique et validation du projet professionnel en IA.'
FROM applications a WHERE a.application_number = 'APP-2026-IIT-0001'
ON CONFLICT DO NOTHING;
