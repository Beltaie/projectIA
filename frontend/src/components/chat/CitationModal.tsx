import React from 'react';
import { X, FileText, CheckCircle, ExternalLink, ShieldCheck } from 'lucide-react';
import { Citation } from '../../types';

interface CitationModalProps {
  citation: Citation | null;
  onClose: () => void;
}

export const CitationModal: React.FC<CitationModalProps> = ({ citation, onClose }) => {
  if (!citation) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in">
      <div className="relative w-full max-w-lg bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 text-slate-100 overflow-hidden">
        
        {/* Accent top gradient */}
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-campus-500 via-indigo-500 to-cyan-400" />

        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-campus-500/10 text-campus-400 border border-campus-500/20">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-slate-800 text-campus-300 border border-slate-700">
                Source Documentaire Officielle • {citation.institution}
              </span>
              <h3 className="text-base font-semibold text-white mt-1">
                {citation.sourceDoc}
              </h3>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Section info & Confidence */}
        <div className="flex items-center justify-between text-xs py-2 px-3 rounded-lg bg-slate-950/60 border border-slate-800/80 mb-4">
          <span className="text-slate-400 font-medium">{citation.section}</span>
          <span className="flex items-center gap-1 font-semibold text-emerald-400">
            <ShieldCheck className="w-3.5 h-3.5" />
            Indice de pertinence : {Math.round(citation.confidence * 100)}%
          </span>
        </div>

        {/* Excerpt text */}
        <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-slate-300 text-sm leading-relaxed mb-5 font-sans italic">
          "{citation.excerpt}"
        </div>

        <div className="flex items-center justify-between text-xs text-slate-500">
          <span>Indexé par le moteur RAG SmartCampus AI</span>
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium transition"
          >
            Fermer
          </button>
        </div>

      </div>
    </div>
  );
};
