export type MessageRole = 'user' | 'assistant' | 'system';

export type LanguageMode = 'fr' | 'ar_tn' | 'arabizi';

export type Campus = 'IIT' | 'ISB' | 'ALL';

export type StudyLevel = 'Licence' | 'Cycle Préparatoire' | 'Cycle Ingénieur' | 'Master';

export interface Citation {
  id: string;
  sourceDoc: string;
  section: string;
  institution: 'IIT' | 'ISB';
  excerpt: string;
  confidence: number;
}

export interface ProgramComparison {
  id: string;
  title: string;
  institution: 'IIT' | 'ISB';
  level: StudyLevel;
  durationYears: number;
  matchScore: number;
  badge?: string;
  careerOutcomes: string[];
  prerequisites: string[];
  strengths: string[];
}

export interface CandidateProfile {
  fullName?: string;
  email?: string;
  phone?: string;
  currentEducation?: string;
  preferredSubjects?: string[];
  careerObjective?: string;
  targetCampus?: Campus;
  targetLevel?: StudyLevel;
  confidenceIndex?: number; // 0 to 100
  isReadyForRegistration?: boolean;
}

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: string;
  language?: LanguageMode;
  citations?: Citation[];
  recommendations?: ProgramComparison[];
  quickReplies?: string[];
  isStreaming?: boolean;
  isError?: boolean;
}

export interface BackendHealth {
  status: 'online' | 'offline' | 'checking';
  serviceName?: string;
  version?: string;
  environment?: string;
  latencyMs?: number;
  lastChecked?: string;
  errorMessage?: string;
}
