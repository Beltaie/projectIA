import { ChatMessage, CandidateProfile, LanguageMode, ProgramComparison, Citation } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Detect language of the input query
export function detectLanguage(text: string): LanguageMode {
  const lower = text.toLowerCase();
  const arabiziPatterns = [
    /\b(3aslema|aslema|chneya|chnawa|chkoun|n7eb|nhebb|behi|kifech|fama|feha|ta9ra|fl|fard|wa9t|brabi|mta3|m3a)\b/i,
    /[235789]/, // Arabizi numbers like 3, 7, 9
  ];
  const tunisianPatterns = [
    /[\u0600-\u06FF]/, // Arabic script
  ];

  if (tunisianPatterns.some((pattern) => pattern.test(lower))) {
    return 'ar_tn';
  }
  if (arabiziPatterns.some((pattern) => pattern.test(lower))) {
    return 'arabizi';
  }
  return 'fr';
}

// Extract progressive profile information from message content
export function extractProfileSignals(
  text: string,
  current: CandidateProfile
): { updated: CandidateProfile; hasNewSignals: boolean } {
  const lower = text.toLowerCase();
  const next = { ...current };
  let hasNewSignals = false;

  // Education level
  if (lower.includes('bac math') || lower.includes('bac sciences') || lower.includes('bac info') || lower.includes('bac technique') || lower.includes('bac eco') || lower.includes('terminale')) {
    if (lower.includes('bac math')) next.currentEducation = 'Baccalauréat Mathématiques';
    else if (lower.includes('bac info')) next.currentEducation = 'Baccalauréat Informatique';
    else if (lower.includes('bac sciences')) next.currentEducation = 'Baccalauréat Sciences Expérimentales';
    else if (lower.includes('bac technique')) next.currentEducation = 'Baccalauréat Technique';
    else if (lower.includes('bac eco')) next.currentEducation = 'Baccalauréat Économie & Gestion';
    else next.currentEducation = 'Lycéen (Terminale)';
    hasNewSignals = true;
  } else if (lower.includes('licence') || lower.includes('bac+3') || lower.includes('l3')) {
    next.currentEducation = 'Licence (Bac+3 en cours ou validée)';
    hasNewSignals = true;
  }

  // Interests
  const subjects: string[] = [...(next.preferredSubjects || [])];
  if ((lower.includes('info') || lower.includes('code') || lower.includes('prog') || lower.includes('logiciel')) && !subjects.includes('Informatique & Dev')) {
    subjects.push('Informatique & Dev');
    hasNewSignals = true;
  }
  if ((lower.includes('math') || lower.includes('calcul') || lower.includes('algorithme')) && !subjects.includes('Mathématiques')) {
    subjects.push('Mathématiques');
    hasNewSignals = true;
  }
  if ((lower.includes('ai') || lower.includes('ia') || lower.includes('intelligence artificielle') || lower.includes('data')) && !subjects.includes('IA & Data Science')) {
    subjects.push('IA & Data Science');
    hasNewSignals = true;
  }
  if ((lower.includes('gestion') || lower.includes('business') || lower.includes('marketing') || lower.includes('finance')) && !subjects.includes('Management & Business')) {
    subjects.push('Management & Business');
    hasNewSignals = true;
  }
  next.preferredSubjects = subjects;

  // Target Campus
  if (lower.includes('iit') && !lower.includes('isb')) {
    next.targetCampus = 'IIT';
    hasNewSignals = true;
  } else if (lower.includes('isb') && !lower.includes('iit')) {
    next.targetCampus = 'ISB';
    hasNewSignals = true;
  }

  // Target Level
  if (lower.includes('prepa') || lower.includes('prépa')) {
    next.targetLevel = 'Cycle Préparatoire';
    hasNewSignals = true;
  } else if (lower.includes('ingenieur') || lower.includes('ingénieur') || lower.includes('genie')) {
    next.targetLevel = 'Cycle Ingénieur';
    hasNewSignals = true;
  } else if (lower.includes('licence')) {
    next.targetLevel = 'Licence';
    hasNewSignals = true;
  }

  // Calculate confidence / completion rate
  let score = 20; // baseline conversation started
  if (next.currentEducation) score += 25;
  if (next.preferredSubjects && next.preferredSubjects.length > 0) score += 25;
  if (next.targetLevel || next.targetCampus) score += 20;
  if (next.careerObjective) score += 10;
  next.confidenceIndex = Math.min(100, score);

  if (next.confidenceIndex >= 70) {
    next.isReadyForRegistration = true;
  }

  return { updated: next, hasNewSignals };
}

// Smart multimodal response generator (serves as high-fidelity Sprint 1 mock & future fallback)
export async function sendUserMessage(
  prompt: string,
  history: ChatMessage[],
  profile: CandidateProfile,
  forceLanguage?: LanguageMode
): Promise<ChatMessage> {
  const lang = forceLanguage || detectLanguage(prompt);
  const lower = prompt.toLowerCase();

  // 1. Try sending to actual backend if implemented
  try {
    const res = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: prompt,
        language: lang,
        profile,
        history: history.slice(-6).map((h) => ({ role: h.role, content: h.content })),
      }),
    });
    if (res.ok) {
      const data = await res.json();
      return {
        id: `msg-${Date.now()}`,
        role: 'assistant',
        content: data.response || data.message,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        language: lang,
        citations: data.citations || [],
        recommendations: data.recommendations || [],
        quickReplies: data.quickReplies || [],
      };
    }
  } catch {
    // Graceful fallback to agent simulation
  }

  // 2. Intelligent Agent Simulation (IIT & ISB Multimodal Knowledge Base)
  await new Promise((r) => setTimeout(r, 650)); // Realistic latency

  let content = '';
  let citations: Citation[] = [];
  let recommendations: ProgramComparison[] = [];
  let quickReplies: string[] = [];

  // Scenarios:
  // A. Difference between Prépa and Licence at IIT
  if (lower.includes('prepa') && (lower.includes('licence') || lower.includes('fer9') || lower.includes('difference') || lower.includes('far9'))) {
    if (lang === 'arabizi') {
      content = `Ahla bik! El fer9 el asesi bin **Cycle Préparatoire Intégré** w **Licence** fel IIT houwa:

1. **Cycle Préparatoire (2 ans)**: Orienté barcha sciences appliquées w maths/physique avancé. Ywaslek direct lel **Cycle Ingénieur IIT** (Génie Logiciel, Systèmes Embarqués, etc.) bla concours national, ama b contrôle continu rigoureux.
2. **Licence Informatique / Business (3 ans)**: Parcours LMD plus progressif, axé pratique et professionnalisation dès la première année. Possibilité d'intégrer le cycle ingénieur sur dossier (concours spécifique IIT) ou continuer en Master.

Chkoun menhom t7es rou7ek 9riblou akthar? T7eb parcours direct ingénieur wala licence pratique d'abord?`;
    } else {
      content = `Excellente question ! Voici la distinction majeure à l'**IIT (Institut International de Technologie)** :

• **Cycle Préparatoire Intégré (2 ans)** : Idéal pour les bacheliers scientifiques (Maths, Sciences, Info). Formation intensive pluridisciplinaire ouvrant un accès direct aux spécialités d'ingénieurs (Génie Logiciel, Télécom, Génie Industriel) via contrôle continu et projets.
• **Licence (3 ans)** : Parcours LMD appliqué combinant théorie et stages dès la L2/L3. Permet soit une insertion professionnelle rapide, soit une passerelle sur dossier vers le cycle d'ingénieur IIT.

Quel est votre type de Baccalauréat actuel pour vous orienter au mieux ?`;
    }

    citations = [
      {
        id: 'cit-1',
        institution: 'IIT',
        sourceDoc: 'Brochure Officielle IIT 2026-2027',
        section: 'Parcours Préparatoire & Conditions d\'Accès (p. 8)',
        excerpt: 'Le cycle préparatoire intégré de l\'IIT prépare sur 2 ans aux études d\'ingénieurs avec passerelle interne directe.',
        confidence: 0.96,
      },
      {
        id: 'cit-2',
        institution: 'IIT',
        sourceDoc: 'Règlement des Études Supérieures Privées',
        section: 'Passerelles Licence vers Cycle Ingénieur (Art. 14)',
        excerpt: 'Les diplômés de Licence Informatique accréditée peuvent postuler sur dossier en 1ère année Cycle Ingénieur.',
        confidence: 0.91,
      },
    ];

    recommendations = [
      {
        id: 'rec-prepa-iit',
        title: 'Cycle Préparatoire Intégré (Technologies & Ingénierie)',
        institution: 'IIT',
        level: 'Cycle Préparatoire',
        durationYears: 2,
        matchScore: 92,
        badge: 'Voie Royale Ingénieur',
        prerequisites: ['Bac Maths', 'Bac Sciences', 'Bac Info', 'Bac Technique'],
        careerOutcomes: ['Accès automatique au cycle Ingénieur IIT', 'Génie Logiciel', 'Systèmes Électroniques'],
        strengths: ['Pas de concours national stressant', 'Projets d\'ingénierie dès la P1', 'Encadrement par enseignants chevronnés'],
      },
      {
        id: 'rec-licence-iit',
        title: 'Licence en Sciences Informatiques (Développement & Systèmes)',
        institution: 'IIT',
        level: 'Licence',
        durationYears: 3,
        matchScore: 85,
        badge: 'Pratique & Polyvalente',
        prerequisites: ['Bac toute série avec prédisposition scientifique'],
        careerOutcomes: ['Développeur Full-Stack', 'Administrateur Systèmes', 'Poursuite en Cycle Ingénieur'],
        strengths: ['Stages obligatoires en entreprise', 'Certifications professionnelles incluses', 'Validation progressive'],
      },
    ];

    quickReplies = [
      'Je prépare un Bac Math/Sciences',
      'Je veux devenir Ingénieur Logiciel',
      'Quels sont les frais et bourses ?',
    ];
  }
  // B. ISB Formations (Business, Finance, Digital Marketing, BI)
  else if (lower.includes('isb') || lower.includes('business') || lower.includes('gestion') || lower.includes('finance') || lower.includes('marketing')) {
    if (lang === 'arabizi') {
      content = `Marhba! L'**ISB (International School of Business)** propose des formations accréditées b modern standards internationaux:

• **Licences Fondamentales & Appliquées**:
  - Business Administration & Management
  - Business Intelligence & Data Analytics (b collaboration ma3 IIT)
  - Finance, Banque & Fintech
  - Marketing Digital & E-Commerce
• **Masters Professionnels**: MBA, Finance Internationale, Supply Chain.

Ena tanshek b **Business Intelligence** idha t7eb tkhallat bin Business w Informatique. Chnawa rayek?`;
    } else {
      content = `À l'**ISB (International School of Business)**, les programmes sont conçus en synergie avec le monde de l'entreprise :

1. **Licence Business Intelligence & Big Data** : Double compétence rare très recherchée alliant gestion de projet et outils d'analyse de données (en partenariat technique avec l'IIT).
2. **Licence Management & Marketing Digital** : Stratégie d'entreprise, communication numérique et entrepreneuriat.
3. **Licence Finance & Comptabilité Internationale** : Audit, marchés financiers et gestion des risques.

Avez-vous une préférence pour l'analyse technologique ou la finance pure ?`;
    }

    citations = [
      {
        id: 'cit-3',
        institution: 'ISB',
        sourceDoc: 'Guide d\'Orientation ISB 2026',
        section: 'Département Systèmes d\'Information et Décisionnel (p. 12)',
        excerpt: 'La filière Business Intelligence combine les modules de gestion ISB aux cours de base de données avancées IIT.',
        confidence: 0.94,
      },
    ];

    recommendations = [
      {
        id: 'rec-isb-bi',
        title: 'Licence Business Intelligence & Analytics',
        institution: 'ISB',
        level: 'Licence',
        durationYears: 3,
        matchScore: 90,
        badge: 'Hybride Tech & Management',
        prerequisites: ['Bac Éco-Gestion', 'Bac Maths', 'Bac Sciences', 'Bac Info'],
        careerOutcomes: ['Data Analyst', 'Consultant ERP', 'Product Owner Junior'],
        strengths: ['Partenariat avec l\'IIT pour les compétences data', 'Stages à l\'étranger possibles', 'Immersion corporate'],
      },
    ];

    quickReplies = [
      'Détails sur la Licence Business Intelligence',
      'Conditions d\'admission ISB',
      'Je préfère le côté 100% technique IIT',
    ];
  }
  // C. Génie Logiciel / Computer Engineering at IIT
  else if (lower.includes('logiciel') || lower.includes('dev') || lower.includes('code') || lower.includes('informatique') || lower.includes('software')) {
    content = `Le **Cycle Ingénieur en Génie Logiciel de l'IIT** est l'un des programmes phares de notre campus nord-américain :

• **Durée** : 3 ans (après prépa, licence ou DUT admissible).
• **Piliers pédagogiques** : Architecture logicielle moderne, Cloud Computing, DevOps, Intelligence Artificielle & Big Data, Sécurité applicative.
• **Partenariats & Certifications** : Accès direct aux certifications AWS, Cisco, Microsoft, et réseau d'alumni dans des multinationales.
• **Alternance & Projets** : Projet de fin d'études (PFE) souvent rémunéré en Tunisie ou en Europe / Amérique du Nord.

Aimeriez-vous que je vérifie votre éligibilité pour ce parcours ou souhaitez-vous planifier une préinscription préliminaire ?`;

    citations = [
      {
        id: 'cit-4',
        institution: 'IIT',
        sourceDoc: 'Référentiel des Compétences Ingénieur IIT',
        section: 'Génie Logiciel & Systèmes d\'Information (Section 3.2)',
        excerpt: 'Formation certifiée conforme aux exigences EUR-ACE et inspirée des modèles universitaires nord-américains.',
        confidence: 0.98,
      },
    ];

    recommendations = [
      {
        id: 'rec-gl-iit',
        title: 'Diplôme National d\'Ingénieur en Génie Logiciel',
        institution: 'IIT',
        level: 'Cycle Ingénieur',
        durationYears: 3,
        matchScore: 97,
        badge: 'Top Taux d\'Insertion (98%)',
        prerequisites: ['Cycle Préparatoire validé', 'Licence Info/Maths/Sc. (Mention B/TB)', 'Passage test d\'orientation'],
        careerOutcomes: ['Ingénieur Full-Stack Cloud', 'Architecte Logiciel', 'Tech Lead', 'Data Engineer'],
        strengths: ['Double diplomation possible avec partenaires canadiens/français', 'FabLab & laboratoires haute technologie', 'Hackathons semestriels'],
      },
    ];

    quickReplies = [
      'Lancer ma préinscription pour le Génie Logiciel',
      'Quels sont les prérequis d\'admission ?',
      'Passer le QCM d\'évaluation préliminaire',
    ];
  }
  // D. General Greeting / Arabizi Welcome
  else if (lower.includes('aslema') || lower.includes('3aslema') || lower.includes('bonjour') || lower.includes('salut') || lower.includes('hello')) {
    if (lang === 'arabizi') {
      content = `Ahla w sahla bik f **SmartCampus AI** ! Ena l'assistant mte3ek bech n3awnek tekhtar a7sen parcours f **IIT** (Institut International de Technologie) wala f **ISB** (International School of Business).

Tnajem tes2alni b tounsi, arabizi wala français.
9olli : Chnouwa l'bac mte3ek (wala el diplôme li 3andek tawwa) w chnouwa l domaine li t7eb tekhem fih f l'musta9bal?`;
    } else {
      content = `Bienvenue sur **SmartCampus AI**, la plateforme conversationnelle d'orientation intelligente pour l'**IIT** et l'**ISB** !

Je suis là pour vous conseiller avec précision, comparer nos cursus (Licence, Prépa, Ingénierie, Master) et vous accompagner pas à pas jusqu'à la préinscription.

Pour débuter : **quel est votre parcours actuel** (série de bac, spécialité) et **quels domaines vous passionnent** le plus ?`;
    }

    quickReplies = [
      'Différence entre Prépa et Licence IIT',
      'Découvrir le Cycle Ingénieur Génie Logiciel',
      'Formations de l\'ISB (Business & Data)',
      'Comment se déroule l\'admission ?',
    ];
  }
  // E. Default responsive answer with adaptive intelligence
  else {
    content = `J'ai bien pris note de votre message. À l'**IIT** et l'**ISB**, nous offrons des cursus reconnus à l'échelle internationale avec un accompagnement pédagogique sur mesure.

Pour vous offrir une orientation parfaitement adaptée :
1. **Diplôme actuel** : Quel diplôme préparez-vous ou avez-vous obtenu ?
2. **Objectif** : Visez-vous une carrière technique (génie logiciel, électronique, mécatronique) ou management/business (finance, marketing, data business) ?`;

    citations = [
      {
        id: 'cit-gen',
        institution: 'IIT',
        sourceDoc: 'Portail des Admissions 2026-2027',
        section: 'Orientation & Entretiens Personnalisés',
        excerpt: 'Chaque candidature fait l\'objet d\'un bilan de compétences et d\'un entretien individuel d\'orientation.',
        confidence: 0.89,
      },
    ];

    quickReplies = [
      'Je veux une carrière en informatique',
      'Je cherche un diplôme en management/commerce',
      'Je veux faire une prépa intégrée',
    ];
  }

  return {
    id: `msg-${Date.now()}`,
    role: 'assistant',
    content,
    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    language: lang,
    citations,
    recommendations,
    quickReplies,
  };
}
