import React from 'react';
import { Bot, Activity, UserCheck, ShieldCheck, Sparkles, RefreshCw } from 'lucide-react';
import { BackendHealth, CandidateProfile } from '../../types';

interface HeaderProps {
  health: BackendHealth;
  profile: CandidateProfile;
  onRefreshHealth: () => void;
  onToggleProfile: () => void;
  isProfileOpen: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  health,
  profile,
  onRefreshHealth,
  onToggleProfile,
  isProfileOpen,
}) => {
  const completion = profile.confidenceIndex || 20;

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        
        {/* Brand & Institution Logos */}
        <div className="flex items-center gap-3">
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-campus-600 via-indigo-600 to-cyan-500 shadow-lg shadow-campus-600/25 ring-1 ring-white/20">
            <Bot className="w-5 h-5 text-white" />
            <span className="absolute -bottom-0.5 -right-0.5 flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
            </span>
          </div>

          <div>
            <div className="flex items-center gap-2">
              <span className="text-base sm:text-lg font-bold tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
                SmartCampus <span className="text-campus-400">AI</span>
              </span>
              <span className="hidden sm:inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                IIT & ISB Sfax
              </span>
            </div>
            <p className="hidden md:block text-[11px] text-slate-400 font-medium">
              Orientation académique multimodale & agentique
            </p>
          </div>
        </div>

        {/* Status badges & Quick tools */}
        <div className="flex items-center gap-2 sm:gap-3">
          
          {/* Backend Status indicator */}
          <div 
            onClick={onRefreshHealth}
            title={health.status === 'online' ? `Backend FastAPI Connecté (${health.latencyMs}ms)` : `Mode Démo / Agent Local (${health.errorMessage || 'Hors ligne'}) - Cliquer pour tester`}
            className="group flex items-center gap-2 px-2.5 py-1.5 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-slate-700 cursor-pointer transition text-xs"
          >
            <span className="relative flex h-2 w-2">
              <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                health.status === 'online' ? 'bg-emerald-400' : 'bg-amber-400'
              }`}></span>
              <span className={`relative inline-flex rounded-full h-2 w-2 ${
                health.status === 'online' ? 'bg-emerald-500' : 'bg-amber-500'
              }`}></span>
            </span>

            <span className="hidden sm:inline text-slate-300 font-medium">
              {health.status === 'online' ? 'FastAPI 8000' : 'Simulation IA'}
            </span>

            <RefreshCw className="w-3 h-3 text-slate-500 group-hover:text-slate-300 group-hover:rotate-180 transition-transform duration-500" />
          </div>

          {/* Multilingual Support Pill */}
          <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-900/60 border border-slate-800 text-xs text-slate-400">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>FR • Tounsi • Arabizi</span>
          </div>

          {/* Profile Progress Trigger */}
          <button
            onClick={onToggleProfile}
            className={`relative flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition border ${
              isProfileOpen
                ? 'bg-campus-600/20 border-campus-500/50 text-white'
                : 'bg-slate-900/90 border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white'
            }`}
          >
            <UserCheck className="w-3.5 h-3.5 text-campus-400" />
            <span className="hidden sm:inline">Mon Profil</span>
            <span className="px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-campus-500/20 text-campus-300 border border-campus-500/30">
              {completion}%
            </span>
          </button>

          {/* Academic Transparency Badge */}
          <div 
            title="Conforme au cahier des charges SmartCampus AI : Validation humaine systématique avant admission officielle."
            className="hidden xl:flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-emerald-950/30 border border-emerald-500/20 text-[11px] text-emerald-400"
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Contrôle Humain</span>
          </div>

        </div>

      </div>
    </header>
  );
};
