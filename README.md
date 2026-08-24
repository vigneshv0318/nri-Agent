# 👵 Ammachi – AI-Powered Native Language Learning Platform for NRI Children

<div align="center">

![Ammachi Logo](frontend/public/pwa-192x192.png)

**Your Personal AI Native Language Companion & Cultural Storyteller**

[![PWA Ready](https://img.shields.io/badge/PWA-Installable-orange?style=for-the-badge&logo=pwa)](https://web.dev/progressive-web-apps/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/React-Vite%20PWA-61DAFB?style=for-the-badge&logo=react)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Psycopg3-336791?style=for-the-badge&logo=postgresql)](https://www.postgresql.org)
[![PaddleOCR](https://img.shields.io/badge/PaddleOCR-PP--OCRv5-FF6F00?style=for-the-badge)](https://github.com/PaddlePaddle/PaddleOCR)
[![Gemini AI](https://img.shields.io/badge/Google%20Gemini-Multimodal-4285F4?style=for-the-badge&logo=google)](https://deepmind.google/technologies/gemini/)

</div>

---

## 📖 Overview

**Ammachi ("Grandmother's Class")** is a production-ready, installable **Progressive Web App (PWA)** designed to help NRI (Non-Resident Indian) children learn, retain, and celebrate Indian native languages (**Tamil, Telugu, Hindi, Malayalam, and Kannada**). 

The platform combines warm, motherly AI mentorship with cutting-edge vision, speech, and agentic workflows across three core modules:

1. ✍️ **AI Handwritten Tutor (PaddleOCR PP-OCRv5 + Gemini Vision)**: Write in a real notebook, snap a photo or use live camera capture, and receive instant stroke, curve, and pulli/dot analysis from Ammachi.
2. 🎤 **AI Voice Agent (Deepgram STT + Patience Denoising Agent + ElevenLabs TTS)**: Practice speaking and conversational fluency with an adaptive, stutter-tolerant grandmother persona that recasts mistakes gently.
3. 🪔 **Cultural Discovery & Gamification (LangGraph Agent + RAG + Digital Passport)**: Explore Indian festivals (Pongal, Diwali, Ugadi, Onam, Karthigai Deepam), folktales, solve quiz challenges, and collect digital Cultural Stamps.

---

## 🛠️ Upgraded Architecture & Tech Stack

```
                               ┌────────────────────────────────┐
                               │  Ammachi React 18 Vite PWA     │
                               │  (Tailwind CSS + WebApp Shell) │
                               └───────────────┬────────────────┘
                                               │ HTTP / REST / JWT
                                               ▼
                               ┌────────────────────────────────┐
                               │        FastAPI Backend         │
                               └───────┬───────────────┬────────┘
                                       │               │
            ┌──────────────────────────┼───────────────┼──────────────────────────┐
            ▼                          ▼               ▼                          ▼
 ┌──────────────────────┐   ┌────────────────────┐   ┌────────────────────┐   ┌──────────────────────────┐
 │    Module 1: Vision  │   │  Module 2: Voice   │   │ Module 3: Culture  │   │  Database & Persistence  │
 │  PaddleOCR PP-OCRv5  │   │  Deepgram Nova-2   │   │  LangGraph State   │   │  PostgreSQL (Psycopg 3)  │
 │  Gemini Multimodal   │   │  Patience Agent    │   │  Festival Story RAG│   │  SQLAlchemy 2.0 ORM      │
 │  Stroke Evaluation   │   │  ElevenLabs TTS    │   │  Gamified Badges   │   │  (SQLite local fallback) │
 └──────────────────────┘   └────────────────────┘   └────────────────────┘   └──────────────────────────┘
```

### Technology Highlights
- **Frontend PWA**: React 18, Vite 5, Tailwind CSS, `vite-plugin-pwa` (Service Worker, Workbox static asset caching, Web App Manifest, Install prompts), Lucide Icons, Canvas Confetti.
- **Backend API**: FastAPI, Pydantic v2, Python 3.11+, JWT security, CORS middleware.
- **AI / Agent Layer**: Google Gemini (`gemini-1.5-flash` / `gemini-2.0-flash`), LangChain, LangGraph orchestrator, Groq Cloud fallback.
- **Vision / OCR**: PaddleOCR (PP-OCRv5 multilingual Indian script support) + OpenCV preprocessing (CLAHE, bilateral filtering).
- **Speech**: Deepgram STT (`nova-2`), ElevenLabs emotive Grandmother TTS (`eleven_multilingual_v2`), gTTS regional fallback.
- **Database**: PostgreSQL with SQLAlchemy 2.0 and Psycopg 3 driver (with automatic zero-config SQLite development fallback).

---

## 📁 Repository Structure

```
AI-Native-Language-Tutor-main/
│
├── backend/
│   ├── api/
│   │   ├── auth.py              # Authentication (JWT, signup, login, Google OAuth, /me)
│   │   ├── vision.py            # Module 1: Handwriting analysis & letters API
│   │   ├── voice.py             # Module 2: STT, Patience Agent, & ElevenLabs TTS
│   │   ├── culture.py           # Module 3: Cultural discovery & LangGraph chat
│   │   └── user.py              # User progress, stats, and passport stamps
│   │
│   ├── database/
│   │   ├── connection.py         # SQLAlchemy engine, Psycopg 3, & SQLite fallback
│   │   ├── models.py             # User, LearningProgress, CulturalStamp, Session
│   │   └── crud.py               # Data access layer & streak/progress metrics
│   │
│   ├── services/
│   │   ├── paddleocr_service.py  # Multilingual PP-OCRv5 character recognition
│   │   ├── gemini_service.py     # Gemini Multimodal Vision & LLM completion
│   │   ├── voice_service.py      # Deepgram STT & ElevenLabs/gTTS streaming
│   │   └── culture_service.py    # Cultural dataset, festivals RAG & media search
│   │
│   ├── agents/
│   │   ├── patience_agent.py     # Speech denoiser & subtle recasting assistant
│   │   └── langgraph_culture.py  # LangGraph state workflow for cultural mentoring
│   │
│   ├── schemas/                  # Pydantic v2 schemas for all APIs
│   ├── main.py                  # FastAPI application entry point
│   └── requirements.txt         # Upgraded Python dependencies
│
├── frontend/
│   ├── public/                  # App icons, favicon, PWA manifest icons
│   ├── src/
│   │   ├── components/          # Mascots, Speech bubbles, Navbars, Audio players
│   │   ├── pages/               # Auth, Dashboard, Writing, Speaking, Culture, Progress, Profile
│   │   ├── context/             # AuthContext (JWT) & LanguageContext (Tamil/Telugu/Hindi)
│   │   ├── services/            # Axios API clients
│   │   ├── App.jsx              # React Router setup
│   │   ├── main.jsx             # React entry point & PWA service worker registration
│   │   └── index.css            # Tailwind design system with warm child-friendly theme
│   ├── package.json
│   └── vite.config.js           # Vite PWA configuration
│
├── .env.example                 # Environment configuration template
├── .gitignore                   # Production Git ignore rules
└── README.md
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.10+** (Python 3.11 recommended)
- **Node.js 18+** & **npm**
- **Git**
- *(Optional)* **PostgreSQL** (if omitted, backend runs seamlessly with local SQLite)

---

### 1. Environment Setup

Copy `.env.example` to create your `.env` file in the `backend/` directory:

```bash
cp .env.example backend/.env
```

Configure your API keys in `backend/.env`:
```ini
# PostgreSQL (Optional - falls back to SQLite if omitted)
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/ammachi_db

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# Groq Cloud (Fast fallback)
GROQ_API_KEY=your_groq_api_key_here

# Deepgram Speech-to-Text
DEEPGRAM_API_KEY=your_deepgram_api_key_here

# ElevenLabs Voice
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=ThT5KcBeYPX3keUQqHPh

# JWT Security
JWT_SECRET=your_jwt_secret_key_here

# Frontend URL
FRONTEND_URL=http://localhost:5173
PORT=8000
```

---

### 2. Backend Setup & Run

Navigate to `backend/` and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Start the FastAPI backend server:

```bash
uvicorn main:app --reload --port 8000
```

The API will be live at:
- **API Root**: `http://localhost:8000`
- **Interactive OpenAPI Docs (Swagger)**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

---

### 3. Frontend Setup & Run

Open a new terminal window, navigate to `frontend/`, and install dependencies:

```bash
cd frontend
npm install
```

Start the Vite development server:

```bash
npm run dev
```

Open your browser at:
👉 `http://localhost:5173`

---

## 📱 Testing Progressive Web App (PWA) Features

### 1. Desktop Installation (Chrome / Edge)
1. Open `http://localhost:5173` in Google Chrome or Microsoft Edge.
2. Click the **Install App** icon in the address bar (or Menu > "Install Ammachi's Class").
3. Launch the standalone desktop app window.

### 2. Mobile Installation (iOS / Android)
- **Android (Chrome)**: Tap the 3-dots menu > **"Add to Home screen"** / **"Install app"**.
- **iOS (Safari)**: Tap the Share button > **"Add to Home Screen"**.

### 3. Offline Shell Test
1. In Chrome DevTools, open the **Application** tab.
2. Check **Service Workers** to verify `sw.js` is active.
3. Check the **Offline** checkbox in DevTools Network tab.
4. Refresh the page: the application shell, fonts, cached lessons, and navigation continue to function offline with an amber offline status banner!

---

## 🧪 Testing the 3 Core Modules

### ✍️ Module 1: AI Handwritten Tutor
1. Navigate to `/writing`.
2. Choose your language (Tamil / Telugu) and select a character (e.g. `அ` or `అ`).
3. Write the character in your physical notebook.
4. Click **"Open Camera"** to take a snapshot, or click **"Upload File"** to pick a picture.
5. Click **"Analyze with Ammachi"**:
   - PaddleOCR extracts the text.
   - Google Gemini evaluates your stroke shape and pulli/dots.
   - Ammachi speaks her motherly feedback aloud with audio!

### 🎤 Module 2: AI Voice Agent
1. Navigate to `/speaking`.
2. Tap **"Tap to Speak 🎙️"** and grant microphone permission when prompted.
3. Say words or sentences (e.g., *"Vazhaipazham"* or *"Vanakkam Ammachi"*).
4. Tap **"Stop Recording"**:
   - Deepgram transcribes your speech.
   - The Patience Agent denoises any pauses or repetitions.
   - Ammachi replies in a warm voice (ElevenLabs / gTTS) and awards fluency points.

### 🪔 Module 3: Cultural Discovery & Gamification
1. Navigate to `/culture`.
2. Select any festival (e.g., **Pongal**, **Diwali**, **Ugadi**, or **Onam**).
3. The LangGraph agent retrieves cultural folklore, shows colorful celebration snapshots, and asks a quiz challenge.
4. Type your answer to earn points and unlock digital stamps in your **Cultural Passport** with celebratory confetti animations!

---

## 🔒 Security & Best Practices
- **No Hardcoded Secrets**: All API keys, database credentials, and JWT secrets are managed via environment variables.
- **Secure Password Hashing**: Passwords are hashed using salted cryptographic hashing (PBKDF2-SHA256).
- **Protected Endpoints**: JWT validation middleware ensures user privacy and progress integrity.
- **Strict CORS**: Origins are strictly controlled via `FRONTEND_URL` / `CORS_ORIGINS`.
