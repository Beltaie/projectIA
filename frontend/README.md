# SmartCampus AI — Frontend (Sprint 1)

Modern, responsive, agentic conversational frontend for **SmartCampus AI** (IIT & ISB Sfax).

## Architecture & Features

- **Multi-lingual Support**: French, Tunisian Arabic, and Arabizi input recognition with live code-switching support.
- **Progressive Profiling**: Automatically extracts candidate signals (Baccalauréat series, academic interests, career goals) and updates an interactive profile completion gauge.
- **RAG Citations & Grounding**: Visual badges with instant document modal inspection (source document, section, excerpt, confidence score).
- **Program Recommendation & Comparison**: Interactive cards comparing IIT & ISB curricula (Licence, Prépa Intégrée, Cycle Ingénieur Génie Logiciel, Business Intelligence) with match scores and prerequisites.
- **Multimodal (Voice STT / Text)**: Simulated Whisper voice recording trigger with real-time waveform states.
- **Pre-Registration & Adaptive QCM Preview**: Pre-filled registration flow and 3-question adaptive evaluation test.
- **FastAPI Backend Integration**:
  - Automatically queries `http://localhost:8000/health` (pre-configured for port 5173 CORS in `backend/config/settings.py`).
  - Seamless fallback to intelligent local simulation if backend is offline or undergoing maintenance.
  - Aligned with backend standardized error schema (`{"error": {"code": "...", "message": "..."}}`).

## Tech Stack

- **Framework**: React 19 + TypeScript + Vite
- **Styling**: Tailwind CSS + Custom Glassmorphism Theme (IIT & ISB brand colors)
- **Icons**: Lucide React

## Setup & Run

### 1. Development Mode
```powershell
cd frontend
npm install
npm run dev
```
Runs locally at: `http://localhost:5173`

### 2. Production Build
```powershell
npm run build
npm run preview
```
