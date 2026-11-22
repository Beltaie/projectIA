import React, { useState } from 'react';
import { X, CheckCircle2, User, Mail, Phone, GraduationCap, ShieldCheck, ArrowRight, HelpCircle } from 'lucide-react';
import { CandidateProfile, ProgramComparison } from '../../types';

interface RegistrationModalProps {
  isOpen: boolean;
  onClose: () => void;
  profile: CandidateProfile;
  selectedProgram?: ProgramComparison | null;
}

export const RegistrationModal: React.FC<RegistrationModalProps> = ({
  isOpen,
  onClose,
  profile,
  selectedProgram,
}) => {
  const [formData, setFormData] = useState({
    fullName: profile.fullName || 'Mohamed Ben Salem',
    email: profile.email || 'mohamed.bensalem@gmail.com',
    phone: profile.phone || '+216 98 123 456',
    education: profile.currentEducation || 'Baccalauréat Mathématiques',
    targetCampus: selectedProgram?.institution || profile.targetCampus || 'IIT',
    program: selectedProgram?.title || 'Cycle Ingénieur Génie Logiciel',
    consent: true,
  });

  const [step, setStep] = useState<'form' | 'qcm' | 'success'>('form');
  const [qcmAnswers, setQcmAnswers] = useState<Record<number, number>>({});

  if (!isOpen) return null;

  // Adaptive QCM Questions based on track (IIT Engineering focus)
  const qcmQuestions = [
    {
      id: 1,
      question: 'En algorithmique, quelle est la complexité temporelle moyenne d\'une recherche binaire dans un tableau trié ?',
      options: ['O(n)', 'O(log n)', 'O(n²)', 'O(1)'],
      correct: 1,
    },
    {
      id: 2,
      question: 'Quelle est la principale différence entre une structure de données Pile (Stack) et File (Queue) ?',
      options: [
        'La pile est FIFO et la file est LIFO',
        'La pile est LIFO (Dernier entré, premier sorti) et la file est FIFO',
        'Il n\'y a aucune différence de principe',
        'La file ne peut contenir que des entiers',
      ],
      correct: 1,
    },
    {
      id: 3,
      question: 'Quelle est votre motivation principale pour intégrer le modèle universitaire nord-américain de l\'IIT ?',
      options: [
        'Approche axée sur les projets réels et stages en entreprise',
        'Accès aux certifications industrielles internationales (AWS, Cisco)',
        'Opportunités de mobilités internationales (Canada, Europe)',
        'Toutes les réponses ci-dessus',
      ],
      correct: 3,
    },
  ];

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in">
      <div className="relative w-full max-w-xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 text-slate-100 overflow-hidden">
        
        {/* Accent top gradient */}
        <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-campus-500 via-indigo-500 to-cyan-400" />

        {/* Header */}
        <div className="flex items-start justify-between mb-5">
          <div>
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-campus-500/15 text-campus-300 border border-campus-500/30">
              Étape {step === 'form' ? '1/3 : Dossier' : step === 'qcm' ? '2/3 : QCM Adaptatif' : '3/3 : Confirmation'}
            </span>
            <h3 className="text-lg font-bold text-white mt-1">
              {step === 'form'
                ? 'Formulaire de Préinscription Rapide'
                : step === 'qcm'
                ? 'Évaluation Initiale & QCM Personnalisé'
                : 'Dossier Enregistré avec Succès !'}
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Step 1: Form */}
        {step === 'form' && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Nom complet</label>
                <div className="relative">
                  <User className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    value={formData.fullName}
                    onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                    className="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-950/70 border border-slate-800 text-xs text-white focus:outline-none focus:border-campus-500"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Email</label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-950/70 border border-slate-800 text-xs text-white focus:outline-none focus:border-campus-500"
                  />
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Téléphone</label>
                <div className="relative">
                  <Phone className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    className="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-950/70 border border-slate-800 text-xs text-white focus:outline-none focus:border-campus-500"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Niveau d'études</label>
                <div className="relative">
                  <GraduationCap className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    value={formData.education}
                    onChange={(e) => setFormData({ ...formData, education: e.target.value })}
                    className="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-950/70 border border-slate-800 text-xs text-white focus:outline-none focus:border-campus-500"
                  />
                </div>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-1">Cursus ciblé</label>
              <input
                type="text"
                value={formData.program}
                onChange={(e) => setFormData({ ...formData, program: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-950/70 border border-slate-800 text-xs text-white focus:outline-none focus:border-campus-500"
              />
            </div>

            <label className="flex items-start gap-2.5 p-3 rounded-xl bg-slate-950/40 border border-slate-800 text-xs text-slate-300 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.consent}
                onChange={(e) => setFormData({ ...formData, consent: e.target.checked })}
                className="mt-0.5 rounded border-slate-700 bg-slate-900 text-campus-600 focus:ring-0"
              />
              <span>J'accepte que mes données soient transmises à l'équipe des admissions IIT/ISB pour la préparation de mon entretien.</span>
            </label>

            <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white"
              >
                Annuler
              </button>
              <button
                type="button"
                onClick={() => setStep('qcm')}
                disabled={!formData.consent}
                className="py-2.5 px-5 rounded-xl font-semibold text-xs tracking-wide bg-gradient-to-r from-campus-600 to-indigo-600 hover:from-campus-500 hover:to-indigo-500 text-white shadow-lg shadow-campus-600/30 transition flex items-center gap-2 disabled:opacity-50"
              >
                <span>Passer au QCM d'évaluation</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Adaptive QCM */}
        {step === 'qcm' && (
          <div className="space-y-4">
            <p className="text-xs text-slate-400">
              Ce test rapide (3 questions) aide les coordinateurs pédagogiques à identifier vos points forts pour l'entretien d'admission.
            </p>

            <div className="space-y-4 max-h-80 overflow-y-auto pr-1">
              {qcmQuestions.map((q, qIdx) => (
                <div key={q.id} className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
                  <h4 className="text-xs font-semibold text-slate-200 mb-2.5">
                    {qIdx + 1}. {q.question}
                  </h4>
                  <div className="space-y-2">
                    {q.options.map((opt, oIdx) => (
                      <label
                        key={oIdx}
                        className={`flex items-center gap-2.5 p-2 rounded-lg text-xs cursor-pointer border transition ${
                          qcmAnswers[q.id] === oIdx
                            ? 'bg-campus-600/20 border-campus-500/60 text-white'
                            : 'bg-slate-900/60 border-slate-800/80 text-slate-300 hover:border-slate-700'
                        }`}
                      >
                        <input
                          type="radio"
                          name={`q-${q.id}`}
                          checked={qcmAnswers[q.id] === oIdx}
                          onChange={() => setQcmAnswers({ ...qcmAnswers, [q.id]: oIdx })}
                          className="text-campus-600 focus:ring-0"
                        />
                        <span>{opt}</span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-between items-center pt-3 border-t border-slate-800">
              <button
                type="button"
                onClick={() => setStep('form')}
                className="px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white"
              >
                Retour
              </button>
              <button
                type="button"
                onClick={() => setStep('success')}
                className="py-2.5 px-5 rounded-xl font-semibold text-xs tracking-wide bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white shadow-lg shadow-emerald-600/30 transition flex items-center gap-2"
              >
                <span>Valider le dossier et le QCM</span>
                <CheckCircle2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Success Confirmation */}
        {step === 'success' && (
          <div className="py-6 text-center space-y-4">
            <div className="w-14 h-14 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center justify-center mx-auto">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <div>
              <h4 className="text-base font-bold text-white">Dossier préinscrit avec succès !</h4>
              <p className="text-xs text-slate-400 max-w-sm mx-auto mt-1">
                Votre candidature pour le <strong className="text-slate-200">{formData.program}</strong> ({formData.targetCampus}) a été transmise aux services des admissions.
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 text-left max-w-sm mx-auto text-xs space-y-1.5">
              <div className="flex justify-between">
                <span className="text-slate-400">Identifiant dossier :</span>
                <span className="font-mono font-bold text-campus-400">SC-2026-0842</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Statut :</span>
                <span className="text-amber-400 font-semibold">En attente d'entretien</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Score QCM :</span>
                <span className="text-emerald-400 font-semibold">100% (3/3 validées)</span>
              </div>
            </div>

            <div className="pt-2">
              <button
                type="button"
                onClick={onClose}
                className="py-2.5 px-6 rounded-xl font-semibold text-xs tracking-wide bg-slate-800 hover:bg-slate-700 text-white transition"
              >
                Fermer et retourner au chat
              </button>
            </div>
          </div>
        )}

      </div>
    </div>
  );
};
