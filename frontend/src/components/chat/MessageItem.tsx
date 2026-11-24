import React from 'react';
import { Bot, User, FileText, ChevronRight, Copy, Check, Sparkles, BookMarked } from 'lucide-react';
import { ChatMessage, Citation, ProgramComparison } from '../../types';

interface MessageItemProps {
  message: ChatMessage;
  onSelectCitation: (citation: Citation) => void;
  onSelectProgram: (program: ProgramComparison) => void;
}

export const MessageItem: React.FC<MessageItemProps> = ({
  message,
  onSelectCitation,
  onSelectProgram,
}) => {
  const isUser = message.role === 'user';
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Helper to format basic markdown-like paragraphs and bold text
  const renderFormattedContent = (content: string) => {
    const lines = content.split('\n');
    return lines.map((line, index) => {
      if (!line.trim()) {
        return <div key={index} className="h-2" />;
      }

      // Format bold text (**text**)
      const parts = line.split(/(\*\*.*?\*\*)/g);
      const formattedLine = parts.map((part, pIdx) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          return (
            <strong key={pIdx} className="font-bold text-white">
              {part.slice(2, -2)}
            </strong>
          );
        }
        return part;
      });

      // Bullet points
      if (line.trim().startsWith('•') || line.trim().startsWith('-')) {
        return (
          <div key={index} className="flex items-start gap-2 ml-1 my-1">
            <span className="text-campus-400 mt-1 flex-shrink-0">•</span>
            <span className="text-slate-200">{formattedLine}</span>
          </div>
        );
      }

      // Numbered lists
      if (/^\d+\./.test(line.trim())) {
        return (
          <div key={index} className="flex items-start gap-2 ml-1 my-1.5">
            <span className="text-campus-400 font-semibold flex-shrink-0">
              {line.trim().match(/^\d+\./)?.[0]}
            </span>
            <span className="text-slate-200">{formattedLine}</span>
          </div>
        );
      }

      return (
        <p key={index} className="leading-relaxed text-slate-200 my-1">
          {formattedLine}
        </p>
      );
    });
  };

  return (
    <div
      className={`group flex items-start gap-3 sm:gap-4 my-4 animate-slide-up ${
        isUser ? 'flex-row-reverse' : 'flex-row'
      }`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 sm:w-9 sm:h-9 rounded-xl flex items-center justify-center shadow-md ${
          isUser
            ? 'bg-slate-800 text-slate-300 ring-1 ring-slate-700'
            : 'bg-gradient-to-tr from-campus-600 to-indigo-600 text-white ring-1 ring-white/20'
        }`}
      >
        {isUser ? <User className="w-4 h-4 sm:w-5 sm:h-5" /> : <Bot className="w-4 h-4 sm:w-5 sm:h-5" />}
      </div>

      {/* Message Box */}
      <div
        className={`relative max-w-[85%] sm:max-w-[78%] rounded-2xl p-4 sm:p-5 transition-all shadow-lg ${
          isUser
            ? 'bg-gradient-to-br from-campus-900/60 to-slate-900 border border-campus-700/40 text-slate-100 rounded-tr-sm'
            : 'bg-slate-900/80 border border-slate-800/90 text-slate-200 rounded-tl-sm backdrop-blur-md'
        }`}
      >
        {/* Meta Header */}
        <div className="flex items-center justify-between gap-2 mb-2 text-[11px] text-slate-400">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-slate-300">
              {isUser ? 'Vous' : 'SmartCampus AI'}
            </span>
            {message.language && (
              <span className="px-1.5 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider bg-slate-800 text-slate-400 border border-slate-700">
                {message.language === 'ar_tn'
                  ? 'Tounsi'
                  : message.language === 'arabizi'
                  ? 'Arabizi'
                  : 'Français'}
              </span>
            )}
          </div>
          <div className="flex items-center gap-2">
            <span>{message.timestamp}</span>
            <button
              onClick={handleCopy}
              title="Copier le message"
              className="opacity-0 group-hover:opacity-100 text-slate-400 hover:text-white transition p-1"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="text-sm text-slate-200 space-y-1">
          {renderFormattedContent(message.content)}
        </div>

        {/* Embedded RAG Citations */}
        {message.citations && message.citations.length > 0 && (
          <div className="mt-4 pt-3 border-t border-slate-800/80">
            <div className="flex items-center gap-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2">
              <BookMarked className="w-3.5 h-3.5 text-campus-400" />
              <span>Sources officielles vérifiées (RAG)</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {message.citations.map((cit) => (
                <button
                  key={cit.id}
                  onClick={() => onSelectCitation(cit)}
                  className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-950/80 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-xs text-slate-300 transition group/btn"
                >
                  <FileText className="w-3.5 h-3.5 text-campus-400 group-hover/btn:text-cyan-400" />
                  <span className="truncate max-w-[200px]">{cit.sourceDoc}</span>
                  <span className="text-[10px] text-emerald-400 font-bold">
                    {Math.round(cit.confidence * 100)}%
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Embedded Course Recommendations */}
        {message.recommendations && message.recommendations.length > 0 && (
          <div className="mt-4 pt-3 border-t border-slate-800/80 space-y-3">
            <div className="flex items-center gap-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
              <span>Parcours recommandés selon votre profil</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {message.recommendations.map((prog) => (
                <div
                  key={prog.id}
                  onClick={() => onSelectProgram(prog)}
                  className="cursor-pointer p-3.5 rounded-xl bg-slate-950/70 hover:bg-slate-800/90 border border-slate-800 hover:border-campus-500/50 transition-all flex flex-col justify-between group/card shadow-sm"
                >
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-campus-500/15 text-campus-300 border border-campus-500/20">
                        {prog.institution} • {prog.level}
                      </span>
                      <span className="text-xs font-bold text-emerald-400">
                        {prog.matchScore}%
                      </span>
                    </div>
                    <h4 className="text-xs font-semibold text-white group-hover/card:text-campus-300 transition-colors line-clamp-2">
                      {prog.title}
                    </h4>
                  </div>

                  <div className="mt-3 flex items-center justify-between pt-2 border-t border-slate-800/60 text-[11px] text-slate-400 group-hover/card:text-white transition">
                    <span>{prog.durationYears} ans d'études</span>
                    <span className="flex items-center gap-0.5 text-campus-400 group-hover/card:translate-x-0.5 transition-transform">
                      Détails <ChevronRight className="w-3.5 h-3.5" />
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
