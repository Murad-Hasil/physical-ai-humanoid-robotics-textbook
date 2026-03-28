# Physical AI & Humanoid Robotics Textbook

An AI-native interactive textbook for teaching Physical AI and Humanoid Robotics — built with Docusaurus, FastAPI, Qdrant, and Neon Postgres.

**Live Book:** https://Murad-Hasil.github.io/physical-ai-humanoid-robotics-textbook/
**Backend API:** https://mb-murad-physical-ai-backend.hf.space/docs

---

## What's Inside

### 13-Week Curriculum

| Module | Weeks | Topics |
|--------|-------|--------|
| Foundation | 1–2 | Physical AI principles, humanoid landscape, sensor systems |
| ROS 2 | 3–5 | Nodes, topics, services, actions, Python packages |
| Gazebo | 6–7 | Physics simulation, URDF/SDF, sensor simulation |
| NVIDIA Isaac | 8–10 | Isaac Sim, Isaac ROS, reinforcement learning, sim-to-real |
| Humanoid + ConvAI | 11–13 | Kinematics, locomotion, Voice-to-Action, Autonomous Humanoid capstone |

### AI Features

- **RAG Chatbot** — Ask questions about any chapter. Powered by Qdrant Cloud (vector search) + Groq LLaMA 3.3 70B
- **Selected Text → Ask AI** — Highlight any text in the book and instantly ask the chatbot about it
- **Hardware-Aware Personalization** — Content adapts based on your hardware (Sim Rig with RTX GPU / Jetson Edge Kit / Unitree G1)
- **Roman Urdu Translation** — Translate any chapter to Roman Urdu with one click

### Platform Features

- JWT authentication with 3-step hardware onboarding at signup
- Admin dashboard — health monitoring, curriculum ingestion, Qdrant reindex
- 180 vectors indexed in Qdrant Cloud across all 13 weeks

---

## Tech Stack

**Frontend**
- Docusaurus v3 (React, TypeScript)
- Tailwind CSS — cyber/dark theme
- Deployed to GitHub Pages via GitHub Actions

**Backend**
- FastAPI (Python)
- Neon Serverless Postgres — 12 tables
- Qdrant Cloud — vector database (384-dim, BAAI/bge-small-en-v1.5)
- Groq API (LLaMA 3.3 70B) — LLM for RAG + personalization + translation
- Deployed on Hugging Face Spaces (Docker)

---

## Project Structure

```
├── docusaurus-textbook/     # Frontend — Docusaurus book
│   ├── docs/                # 13 weeks of content
│   │   ├── foundation/      # Weeks 1–2
│   │   ├── 01-ros-2/        # Weeks 3–5
│   │   ├── 02-gazebo/       # Weeks 6–7
│   │   ├── 03-nvidia-isaac/ # Weeks 8–10
│   │   └── 04-humanoid/     # Weeks 11–13
│   └── src/
│       ├── components/      # ChatWidget, Roadmap, Admin
│       ├── context/         # PersonalizationContext, HardwareContext
│       └── theme/           # Custom Navbar, DocItem (translation/personalization buttons)
│
├── backend/                 # FastAPI backend
│   ├── api/                 # Auth, chat, admin, user profiles
│   ├── services/            # RAG pipeline, personalization, translation
│   ├── retrieval/           # Qdrant vector service
│   ├── llm/                 # Groq client + prompts
│   └── models/              # SQLAlchemy models
│
└── .github/workflows/       # GitHub Actions — auto deploy to GitHub Pages
```

---

## Local Development

### Frontend
```bash
cd docusaurus-textbook
npm install
npm start
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your keys
uvicorn main:app --reload
```

### Environment Variables (backend)
```
DATABASE_URL=postgresql://...     # Neon Serverless Postgres
GROQ_API_KEY=gsk_...              # Groq API
QDRANT_URL=https://...qdrant.io   # Qdrant Cloud
QDRANT_API_KEY=...
SECRET_KEY=...
JWT_SECRET_KEY=...
CORS_ORIGINS=http://localhost:3000
```

---

## Built With

- [Claude Code](https://www.claude.com/product/claude-code) — AI-assisted development
- [Spec-Kit Plus](https://github.com/panaversity/spec-kit-plus/) — Spec-driven workflow
- [Docusaurus](https://docusaurus.io/) — Static site framework
- [Qdrant](https://qdrant.tech/) — Vector database
- [Neon](https://neon.tech/) — Serverless Postgres
- [Groq](https://groq.com/) — LLM inference
