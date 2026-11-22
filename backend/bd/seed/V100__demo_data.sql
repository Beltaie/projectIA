-- V100: demo data (SA-18). DEV ONLY: never load this in production.
-- Every row is fake and labelled DEMO.

INSERT INTO institutions (code, name_fr) VALUES
('IIT', 'Institut International de Technologie'),
('ISB', 'École Internationale Supérieure Privée des Affaires de Sfax');

INSERT INTO programs (institution_id, code, name_fr, name_ar, track, duration_years,
                      language_of_instruction, description_fr, career_outcomes_fr)
SELECT i.id, v.code, v.name_fr, v.name_ar, v.track, v.dur, 'FR', v.descr, v.career
FROM institutions i
JOIN (VALUES
  ('IIT','LIC-INFO-FR','Licence en Informatique','إجازة في الإعلامية','LICENCE',3,
   'DEMO: formation en développement et systèmes.','DEMO: développeur, administrateur systèmes.'),
  ('IIT','PREPA-INT-FR','Cycle Préparatoire Intégré','سنة تحضيرية','PREPA',2,
   'DEMO: deux années de tronc commun scientifique.','DEMO: accès au cycle ingénieur.'),
  ('IIT','ING-IA-FR','Cycle Ingénieur Intelligence Artificielle','مهندس ذكاء اصطناعي','INGENIEUR',3,
   'DEMO: formation d''ingénieur orientée IA.','DEMO: ingénieur IA, data engineer.'),
  ('ISB','LIC-GESTION-FR','Licence en Gestion','إجازة في التصرف','LICENCE',3,
   'DEMO: formation en gestion et management.','DEMO: gestionnaire, assistant de direction.')
) AS v(inst, code, name_fr, name_ar, track, dur, descr, career) ON v.inst = i.code;

INSERT INTO program_pathways (from_program_id, to_program_id, conditions_fr)
SELECT a.id, b.id, 'DEMO: passerelle sous conditions de résultats.'
FROM programs a, programs b
WHERE a.code = 'PREPA-INT-FR' AND b.code = 'ING-IA-FR';

INSERT INTO admission_conditions (program_id, academic_year, required_diploma, condition_fr, source)
SELECT id, '2026/2027', 'Baccalauréat', 'DEMO: dossier et moyenne minimale selon la filière.', 'DEMO DATA'
FROM programs WHERE code IN ('LIC-INFO-FR','LIC-GESTION-FR');

INSERT INTO tuition_fees (program_id, academic_year, fee_type, amount, source)
SELECT id, '2026/2027', 'ANNUEL',
       CASE code
         WHEN 'LIC-INFO-FR'    THEN 3500
         WHEN 'PREPA-INT-FR'   THEN 4000
         WHEN 'ING-IA-FR'      THEN 6000
         WHEN 'LIC-GESTION-FR' THEN 3000
       END,
       'DEMO DATA'
FROM programs;

INSERT INTO deadlines (program_id, academic_year, deadline_type, deadline_date, source)
SELECT id, '2026/2027', 'DEPOT_DOSSIER',
       CASE code WHEN 'LIC-INFO-FR' THEN DATE '2027-07-15' ELSE DATE '2027-06-30' END,
       'DEMO DATA'
FROM programs WHERE code IN ('LIC-INFO-FR','ING-IA-FR','LIC-GESTION-FR');

-- One promotion per institution, with different values, to test that case.
INSERT INTO fee_promotions (tuition_fee_id, title, condition_fr, discount_type,
                            discount_value, start_date, end_date, source)
SELECT tf.id,
       'DEMO: paiement annuel anticipé',
       'DEMO: paiement de l''année complète en une seule fois.',
       'PERCENTAGE',
       CASE i.code WHEN 'IIT' THEN 15 ELSE 10 END,
       DATE '2026-09-01', DATE '2027-01-31',
       'DEMO DATA'
FROM tuition_fees tf
JOIN programs p      ON p.id = tf.program_id
JOIN institutions i  ON i.id = p.institution_id
WHERE tf.fee_type = 'ANNUEL' AND p.code IN ('LIC-INFO-FR','LIC-GESTION-FR');