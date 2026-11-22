import React, { useState, useEffect, useRef } from 'react';
import { Header } from './components/common/Header';
import { ProfileDrawer } from './components/common/ProfileDrawer';
import { MessageItem } from './components/chat/MessageItem';
import { QuickReplies } from './components/chat/QuickReplies';
import { ChatInput } from './components/chat/ChatInput';
import { CitationModal } from './components/chat/CitationModal';
import { ProgramModal } from './components/chat/ProgramModal';
import { RegistrationModal } from './components/chat/RegistrationModal';
import { checkBackendHealth } from './services/api';
import { sendUserMessage, extractProfileSignals } from './services/chatService';
import {
  ChatMessage,
  CandidateProfile,
  BackendHealth,
  Citation,
  ProgramComparison,
  LanguageMode,
} from './types';
import { Sparkles, Compass, GraduationCap, Building2, CheckCircle2 } from 'lucide-react';

export function App() {
  // Active Language preference ('auto' | 'fr' | 'ar_tn' | 'arabizi')
  const [selectedLanguage, setSelectedLanguage] = useState<LanguageMode | 'auto'>('auto');

  // Backend connectivity state
  const [health, setHealth] = useState<BackendHealth>({
    status: 'checking',
  });

  // Candidate Profile state
  const [profile, setProfile] = useState<CandidateProfile>({
    confidenceIndex: 25,
    preferredSubjects: [],
  });

  // Chat message history
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome-msg',
      role: 'assistant',
      content: `Bienvenue sur **SmartCampus AI**, l'assistant conversationnel intelligent pour l'orientation à l'**IIT** (Institut International de Technologie) et l'**ISB** (International School of Business) !

Je peux vous renseigner en **Français**, **Dialecte Tunisien** ou **Arabizi** :
• Comparer le **Cycle Préparatoire**, les **Licences** et le **Cycle Ingénieur** (Génie Logiciel, Télécom...)
• Explorer les filières de l'**ISB** (Business Intelligence, Finance, Marketing Digital)
• Calculer votre compatibilité de profil et préparer votre préinscription

Pour commencer : **quel est votre diplôme ou niveau actuel** et quel domaine vous intéresse ?`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      language: 'fr',
      citations: [
        {
          id: 'cit-init',
          institution: 'IIT',
          sourceDoc: 'Guide Officiel d\'Orientation 2026-2027',
          section: 'Introduction & Procédure d\'Orientation Intelligente',
          excerpt: 'SmartCampus AI guide les candidats dans le choix de leurs études supérieures et personnalise leur accompagnement.',
          confidence: 0.99,
        },
      ],
      quickReplies: [
        'Différence entre Prépa et Licence IIT',
        'Ingénierie Génie Logiciel IIT',
        'Formations ISB (Business Intelligence)',
        'Aslema, 3andi bac math chneya l options ?',
      ],
    },
  ]);

  const [isLoading, setIsLoading] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [selectedCitation, setSelectedCitation] = useState<Citation | null>(null);
  const [selectedProgram, setSelectedProgram] = useState<ProgramComparison | null>(null);
  const [isRegistrationOpen, setIsRegistrationOpen] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Poll backend health on load and every 20 seconds
  const fetchHealth = async () => {
    const res = await checkBackendHealth();
    setHealth(res);
  };

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 20000);
    return () => clearInterval(interval);
  }, []);

  // Auto-scroll chat to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Handle message sending
  const handleSendMessage = async (text: string, forceLang?: LanguageMode) => {
    if (!text.trim() || isLoading) return;

    const langToUse: LanguageMode | undefined = forceLang || (selectedLanguage !== 'auto' ? selectedLanguage : undefined);

    // 1. Add user message
    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: text,
      language: langToUse,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    // 2. Extract profile signals progressively
    const { updated } = extractProfileSignals(text, profile);
    setProfile(updated);

    try {
      // 3. Get intelligent multimodal AI response
      const assistantMsg = await sendUserMessage(text, [...messages, userMsg], updated, langToUse);
      setMessages((prev) => [...prev, assistantMsg]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          role: 'assistant',
          content: 'Désolé, une erreur est survenue lors du traitement. Veuillez réessayer.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          isError: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // Extract quick replies from latest assistant message
  const latestQuickReplies =
    messages.slice().reverse().find((m) => m.role === 'assistant' && m.quickReplies && m.quickReplies.length > 0)
      ?.quickReplies || [];

  return (
    <div className="flex flex-col h-screen w-full bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Top Navigation */}
      <Header
        health={health}
        profile={profile}
        selectedLanguage={selectedLanguage}
        onSelectLanguage={setSelectedLanguage}
        onRefreshHealth={fetchHealth}
        onToggleProfile={() => setIsProfileOpen(!isProfileOpen)}
        isProfileOpen={isProfileOpen}
      />

      {/* Main Layout Container */}
      <div className="flex-1 flex overflow-hidden max-w-7xl w-full mx-auto px-2 sm:px-6 lg:px-8 py-3 sm:py-4 gap-4">
        
        {/* Left Side: Chat Workspace */}
        <div className="flex-1 flex flex-col h-full bg-slate-900/40 rounded-3xl border border-slate-800/80 shadow-2xl backdrop-blur-xl overflow-hidden">
          
          {/* Top Banner (Campus Highlights) */}
          <div className="px-4 py-2.5 bg-slate-950/60 border-b border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
            <div className="flex items-center gap-2 overflow-x-auto no-scrollbar">
              <span className="flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-campus-500/10 text-campus-300 font-semibold border border-campus-500/20">
                <Building2 className="w-3 h-3 text-campus-400" /> IIT Sfax : Ingénierie & Tech
              </span>
              <span className="flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-teal-500/10 text-teal-300 font-semibold border border-teal-500/20">
                <Building2 className="w-3 h-3 text-teal-400" /> ISB Sfax : Business & Management
              </span>
            </div>
            <span className="hidden md:inline text-[11px] text-slate-500">
              Session d'orientation active
            </span>
          </div>

          {/* Messages Scroll Area */}
          <div className="flex-1 overflow-y-auto px-3 sm:px-6 py-4 space-y-4">
            {messages.map((msg) => (
              <MessageItem
                key={msg.id}
                message={msg}
                onSelectCitation={(cit) => setSelectedCitation(cit)}
                onSelectProgram={(prog) => setSelectedProgram(prog)}
              />
            ))}

            {/* Typing / Thinking Indicator */}
            {isLoading && (
              <div className="flex items-center gap-3 my-4 animate-fade-in">
                <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-campus-600 to-indigo-600 flex items-center justify-center text-white ring-1 ring-white/20">
                  <Sparkles className="w-4 h-4 animate-spin text-cyan-300" />
                </div>
                <div className="px-4 py-3 rounded-2xl rounded-tl-sm bg-slate-900 border border-slate-800 text-xs text-slate-400 flex items-center gap-2 shadow-lg">
                  <span className="flex gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-campus-400 animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-1.5 h-1.5 rounded-full bg-campus-400 animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-1.5 h-1.5 rounded-full bg-campus-400 animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </span>
                  <span>Analyse du corpus RAG et formulation de la recommandation...</span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Bottom Interactive Area */}
          <div className="p-3 sm:p-4 bg-slate-950/80 border-t border-slate-800/80 space-y-2.5">
            {/* Quick Prompt Pills */}
            <QuickReplies
              replies={latestQuickReplies}
              onSelect={handleSendMessage}
              disabled={isLoading}
            />

            {/* Main Chat Input Bar */}
            <ChatInput
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
              selectedLanguage={selectedLanguage}
              onSelectLanguage={setSelectedLanguage}
            />

            <div className="flex items-center justify-between text-[11px] text-slate-500 px-1 pt-1">
              <span>SmartCampus AI • Multimodal Architecture IIT/ISB</span>
              <span className="hidden sm:inline">Entrée pour envoyer, Maj + Entrée pour retour à la ligne</span>
            </div>
          </div>

        </div>

      </div>

      {/* Progressive Profile Drawer */}
      <ProfileDrawer
        isOpen={isProfileOpen}
        onClose={() => setIsProfileOpen(false)}
        profile={profile}
        onStartRegistration={() => setIsRegistrationOpen(true)}
      />

      {/* RAG Citation Inspection Modal */}
      <CitationModal
        citation={selectedCitation}
        onClose={() => setSelectedCitation(null)}
      />

      {/* Course Program Details Modal */}
      <ProgramModal
        program={selectedProgram}
        onClose={() => setSelectedProgram(null)}
        onApply={(prog) => {
          setSelectedProgram(null);
          setIsRegistrationOpen(true);
        }}
      />

      {/* Pre-registration & QCM Modal */}
      <RegistrationModal
        isOpen={isRegistrationOpen}
        onClose={() => setIsRegistrationOpen(false)}
        profile={profile}
        selectedProgram={selectedProgram}
      />
    </div>
  );
}

export default App;
