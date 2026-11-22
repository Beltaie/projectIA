import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, MicOff, Sparkles } from 'lucide-react';
import { detectLanguage } from '../../services/chatService';

interface ChatInputProps {
  onSendMessage: (text: string) => void;
  isLoading: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [text, setText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [detectedLang, setDetectedLang] = useState<'fr' | 'ar_tn' | 'arabizi'>('fr');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (text.trim().length > 2) {
      setDetectedLang(detectLanguage(text));
    }
  }, [text]);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!text.trim() || isLoading) return;

    onSendMessage(text.trim());
    setText('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = `${Math.min(e.target.scrollHeight, 140)}px`;
  };

  // Simulated Voice Input (STT) per Project Specifications (Page 1 & 4)
  const toggleRecording = () => {
    if (isRecording) {
      setIsRecording(false);
    } else {
      setIsRecording(true);
      // Simulate audio transcription in Tunisian/Arabizi
      setTimeout(() => {
        setText('Aslema, ena 3andi bac math w n7eb naamel genie logiciel fel IIT, chneya les conditions?');
        setIsRecording(false);
      }, 2500);
    }
  };

  return (
    <div className="w-full relative">
      {/* Voice Recording Active Banner */}
      {isRecording && (
        <div className="absolute -top-11 left-0 right-0 flex items-center justify-between px-4 py-2 rounded-xl bg-indigo-950/90 border border-indigo-500/30 text-indigo-300 text-xs shadow-lg animate-fade-in backdrop-blur-md">
          <div className="flex items-center gap-2">
            <span className="flex h-2.5 w-2.5 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-red-500"></span>
            </span>
            <span className="font-semibold">Enregistrement audio en cours (Whisper STT)...</span>
          </div>
          <span className="text-[10px] text-indigo-400">Parlez en Français ou Dialecte Tunisien</span>
        </div>
      )}

      {/* Main Input Form */}
      <form
        onSubmit={handleSubmit}
        className="relative flex items-end gap-2 bg-slate-900/90 border border-slate-800 rounded-2xl p-2 sm:p-2.5 focus-within:border-campus-500/60 focus-within:ring-2 focus-within:ring-campus-500/20 shadow-xl transition-all"
      >
        {/* Language Detection Indicator */}
        {text.trim().length > 3 && (
          <div className="hidden sm:flex items-center absolute -top-3.5 right-4 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-800 border border-slate-700 text-slate-300 shadow-sm animate-fade-in">
            Langue détectée :{' '}
            <span className="ml-1 text-campus-400">
              {detectedLang === 'ar_tn' ? 'Tounsi' : detectedLang === 'arabizi' ? 'Arabizi' : 'Français'}
            </span>
          </div>
        )}

        {/* Text Area */}
        <textarea
          ref={textareaRef}
          value={text}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder="Posez votre question en Français, Tunisien ou Arabizi (ex: Chneya l fer9 bin prepa w licence ?)..."
          rows={1}
          disabled={isLoading || isRecording}
          className="flex-1 bg-transparent border-0 resize-none text-slate-100 placeholder-slate-500 text-sm focus:ring-0 focus:outline-none max-h-36 py-2 px-3 leading-relaxed"
        />

        {/* Action Controls */}
        <div className="flex items-center gap-1.5 pb-1">
          {/* Audio Input Button */}
          <button
            type="button"
            onClick={toggleRecording}
            title={isRecording ? 'Arrêter l\'enregistrement' : 'Enregistrer un vocal (Whisper STT)'}
            className={`p-2 rounded-xl transition ${
              isRecording
                ? 'bg-red-500/20 text-red-400 border border-red-500/40 animate-pulse'
                : 'text-slate-400 hover:text-white hover:bg-slate-800'
            }`}
          >
            {isRecording ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
          </button>

          {/* Send Button */}
          <button
            type="submit"
            disabled={!text.trim() || isLoading}
            className="p-2 sm:px-3 sm:py-2 rounded-xl bg-campus-600 hover:bg-campus-500 disabled:opacity-30 disabled:hover:bg-campus-600 text-white font-medium text-xs shadow-md shadow-campus-600/25 transition flex items-center gap-1.5"
          >
            <Send className="w-4 h-4" />
            <span className="hidden sm:inline">Envoyer</span>
          </button>
        </div>
      </form>
    </div>
  );
};
