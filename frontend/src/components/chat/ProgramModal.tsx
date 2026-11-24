import React from 'react';
import { X, Award, Clock, CheckCircle2, Briefcase, GraduationCap, ArrowRight } from 'lucide-react';
import { ProgramComparison } from '../../types';

interface ProgramModalProps {
  program: ProgramComparison | null;
  onClose: () => void;
  onApply: (program: ProgramComparison) => void;
}

export const ProgramModal: React.FC<ProgramModalProps> = ({
  program,
  onClose,
  onApply,
}) => {
  if (!program) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-950/75 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in">
      <div className="relative w-full max-w-xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 text-slate-100 overflow-hidden">
        
        {/* Accent top gradient */}
        <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-campus-500 via-indigo-500 to-emerald-400" />

        {/* Modal Header */}
        <div className="flex items-start justify-between mb-5">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="px-2.5 py-0.5 rounded text-[10px] font-bold tracking-wide uppercase bg-campus-500/15 text-campus-300 border border-campus-500/30">
                {program.institution} • {program.level}
              </span>
              {program.badge && (
                <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                  {program.badge}
                </span>
              )}
            </div>
            <h3 className="text-lg font-bold text-white tracking-tight">
              {program.title}
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Quick Highlights / Metrics */}
        <div className="grid grid-cols-2 gap-3 mb-5">
          <div className="p-3 rounded-xl bg-slate-950/50 border border-slate-800">
            <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-0.5">
              <Clock className="w-3.5 h-3.5 text-indigo-400" />
              <span>Durée des études</span>
            </div>
            <div className="text-sm font-semibold text-white">
              {program.durationYears} ans ({program.level === 'Cycle Préparatoire' ? '4 semestres' : `${program.durationYears * 2} semestres`})
            </div>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/50 border border-slate-800">
            <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-0.5">
              <Award className="w-3.5 h-3.5 text-emerald-400" />
              <span>Indice d'adéquation profil</span>
            </div>
            <div className="text-sm font-bold text-emerald-400">
              {program.matchScore}% de compatibilité
            </div>
          </div>
        </div>

        {/* Strengths / Points Forts */}
        <div className="mb-4">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
            <span>Points forts du programme</span>
          </h4>
          <ul className="space-y-1.5">
            {program.strengths.map((str, idx) => (
              <li key={idx} className="text-xs text-slate-300 flex items-start gap-2">
                <span className="text-campus-400 mt-0.5">•</span>
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Prerequisites */}
        <div className="mb-4">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
            <GraduationCap className="w-3.5 h-3.5 text-indigo-400" />
            <span>Conditions d'admission & Prérequis</span>
          </h4>
          <div className="flex flex-wrap gap-1.5">
            {program.prerequisites.map((req, idx) => (
              <span
                key={idx}
                className="px-2.5 py-1 rounded-md text-xs bg-slate-800/80 text-slate-300 border border-slate-700/80"
              >
                {req}
              </span>
            ))}
          </div>
        </div>

        {/* Career Outcomes */}
        <div className="mb-6">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
            <Briefcase className="w-3.5 h-3.5 text-amber-400" />
            <span>Métiers & Débouchés</span>
          </h4>
          <div className="flex flex-wrap gap-1.5">
            {program.careerOutcomes.map((career, idx) => (
              <span
                key={idx}
                className="px-2.5 py-1 rounded-md text-xs bg-indigo-950/40 text-indigo-300 border border-indigo-500/20"
              >
                {career}
              </span>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between gap-3 pt-3 border-t border-slate-800">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition"
          >
            Fermer
          </button>
          <button
            onClick={() => onApply(program)}
            className="py-2.5 px-5 rounded-xl font-semibold text-xs tracking-wide bg-gradient-to-r from-campus-600 to-indigo-600 hover:from-campus-500 hover:to-indigo-500 text-white shadow-lg shadow-campus-600/30 transition flex items-center gap-2 group"
          >
            <span>Choisir pour Préinscription</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>

      </div>
    </div>
  );
};
