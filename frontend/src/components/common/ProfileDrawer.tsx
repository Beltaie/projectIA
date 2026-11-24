import React from 'react';
import { X, GraduationCap, Compass, BookOpen, Target, Sparkles, CheckCircle2, AlertCircle, ArrowRight } from 'lucide-react';
import { CandidateProfile } from '../../types';

interface ProfileDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  profile: CandidateProfile;
  onStartRegistration?: () => void;
}

export const ProfileDrawer: React.FC<ProfileDrawerProps> = ({
  isOpen,
  onClose,
  profile,
  onStartRegistration,
}) => {
  if (!isOpen) return null;

  const score = profile.confidenceIndex || 20;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-slate-950/60 backdrop-blur-sm animate-fade-in">
      <div className="absolute inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-slate-900 border-l border-slate-800 shadow-2xl flex flex-col">
          
          {/* Drawer Header */}
          <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/50">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-lg bg-campus-500/10 text-campus-400 border border-campus-500/20">
                <Compass className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-semibold text-white">Profil d'Orientation</h3>
                <p className="text-xs text-slate-400">Construction continue par l'agent IA</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Drawer Body */}
          <div className="flex-1 overflow-y-auto p-5 space-y-6">
            
            {/* Completion Gauge Card */}
            <div className="p-4 rounded-xl bg-gradient-to-br from-slate-800/60 to-slate-900/60 border border-slate-700/50">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Complétude du profil
                </span>
                <span className="text-sm font-bold text-campus-400">{score}%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-campus-500 to-cyan-400 transition-all duration-700 rounded-full"
                  style={{ width: `${score}%` }}
                />
              </div>
              <p className="mt-2 text-xs text-slate-400 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-cyan-400 flex-shrink-0" />
                <span>
                  {score < 50
                    ? 'Continuez à échanger pour affiner la recommandation.'
                    : score < 80
                    ? 'Profil bien ciblé ! Vous pouvez préciser vos ambitions.'
                    : 'Profil optimal pour lancer la préinscription.'}
                </span>
              </p>
            </div>

            {/* Profile Attributes */}
            <div className="space-y-4">
              
              {/* Niveau / Formation Actuelle */}
              <div className="p-3.5 rounded-xl bg-slate-950/40 border border-slate-800/80">
                <div className="flex items-center gap-2 text-xs font-medium text-slate-400 mb-1.5">
                  <GraduationCap className="w-4 h-4 text-indigo-400" />
                  <span>Niveau scolaire / Diplôme actuel</span>
                </div>
                <div className="text-sm font-semibold text-white">
                  {profile.currentEducation || (
                    <span className="text-slate-500 italic font-normal">
                      En attente de précision (ex: Bac Math, L3...)
                    </span>
                  )}
                </div>
              </div>

              {/* Centres d'intérêt & Matières */}
              <div className="p-3.5 rounded-xl bg-slate-950/40 border border-slate-800/80">
                <div className="flex items-center gap-2 text-xs font-medium text-slate-400 mb-2">
                  <BookOpen className="w-4 h-4 text-cyan-400" />
                  <span>Centres d'intérêt & Compétences clés</span>
                </div>
                {profile.preferredSubjects && profile.preferredSubjects.length > 0 ? (
                  <div className="flex flex-wrap gap-1.5">
                    {profile.preferredSubjects.map((sub, i) => (
                      <span
                        key={i}
                        className="px-2 py-0.5 rounded-md text-xs font-medium bg-campus-500/15 text-campus-300 border border-campus-500/20"
                      >
                        {sub}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-slate-500 italic">
                    Aucune matière déclarée (parlez de ce que vous aimez étudier)
                  </p>
                )}
              </div>

              {/* Campus & Niveau Visé */}
              <div className="p-3.5 rounded-xl bg-slate-950/40 border border-slate-800/80">
                <div className="flex items-center gap-2 text-xs font-medium text-slate-400 mb-1.5">
                  <Target className="w-4 h-4 text-emerald-400" />
                  <span>Cursus & Établissement cibles</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-slate-800 text-slate-200 border border-slate-700">
                    {profile.targetCampus || 'IIT / ISB'}
                  </span>
                  <span className="text-xs text-slate-400">•</span>
                  <span className="text-xs font-medium text-slate-300">
                    {profile.targetLevel || 'Licence, Prépa ou Ingénieur'}
                  </span>
                </div>
              </div>

            </div>

            {/* Human in the loop Notice */}
            <div className="p-3.5 rounded-xl bg-amber-950/20 border border-amber-500/20 text-xs text-amber-300/90 space-y-1">
              <div className="flex items-center gap-1.5 font-semibold text-amber-300">
                <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0" />
                <span>Garantie Académique & Déontologie</span>
              </div>
              <p className="text-[11px] leading-relaxed text-amber-200/70">
                Les suggestions fournies par SmartCampus AI sont strictement indicatives. La décision d'admission finale est prononcée par la commission pédagogique IIT/ISB après entretien.
              </p>
            </div>

          </div>

          {/* Drawer Footer CTA */}
          <div className="p-5 border-t border-slate-800 bg-slate-950/60">
            <button
              onClick={() => {
                onClose();
                if (onStartRegistration) onStartRegistration();
              }}
              className="w-full py-2.5 px-4 rounded-xl font-semibold text-xs tracking-wide bg-gradient-to-r from-campus-600 to-indigo-600 hover:from-campus-500 hover:to-indigo-500 text-white shadow-lg shadow-campus-600/30 transition flex items-center justify-center gap-2 group"
            >
              <span>Continuer vers la Préinscription</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>
          </div>

        </div>
      </div>
    </div>
  );
};
