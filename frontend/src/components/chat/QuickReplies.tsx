import React from 'react';
import { Sparkles } from 'lucide-react';

interface QuickRepliesProps {
  replies: string[];
  onSelect: (reply: string) => void;
  disabled?: boolean;
}

export const QuickReplies: React.FC<QuickRepliesProps> = ({
  replies,
  onSelect,
  disabled,
}) => {
  if (!replies || replies.length === 0) return null;

  return (
    <div className="flex items-center gap-2 overflow-x-auto py-2 px-1 no-scrollbar animate-fade-in">
      <div className="flex items-center gap-1.5 text-xs text-slate-400 font-medium pl-1 flex-shrink-0">
        <Sparkles className="w-3.5 h-3.5 text-campus-400" />
        <span className="hidden sm:inline">Suggestions :</span>
      </div>
      {replies.map((reply, idx) => (
        <button
          key={idx}
          disabled={disabled}
          onClick={() => onSelect(reply)}
          className="flex-shrink-0 px-3 py-1.5 rounded-full text-xs font-medium bg-slate-900/90 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-800 hover:border-campus-500/40 transition shadow-sm active:scale-95 disabled:opacity-50 disabled:pointer-events-none"
        >
          {reply}
        </button>
      ))}
    </div>
  );
};
