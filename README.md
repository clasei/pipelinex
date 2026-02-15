# pipelinex → local llm training dashboard

minimal, cyan-styled ui for training your local llm with your data.

## stack

- **frontend**: react + typescript + vite + tailwind (port 5173)
- **backend**: fastapi + python 3.12 (port 3001)
- **llm**: ollama + mistral (port 11434)

## quick start

you need **3 terminals**:

### terminal 1: ollama
```bash
ollama serve
```

### terminal 2: backend
```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 3001
```

or use the script:
```bash
./start_backend.sh
```

### terminal 3: frontend
```bash
cd frontend
npm run dev
```

then open: **http://localhost:5173**

## setup (first time only)

### 1. install ollama
```bash
# already done - you have mistral installed
ollama list
```

### 2. setup backend
```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. setup frontend
```bash
cd frontend
npm install
```

### 4. add training data
place your conversations in `backend/training_data.jsonl` (already done)

## training data format

```json
{"prompt": "your question", "completion": "your answer style"}
```

## api endpoints

- `GET /api/health` → health check
- `POST /api/training/start` → start training
- `POST /api/training/stop` → stop training
- `GET /api/training/status` → get status
- `WS /api/training/stream` → real-time metrics

## project structure

```
pipeline/
├── frontend/          # react ui
│   ├── App.tsx
│   ├── components/
│   └── package.json
├── backend/           # fastapi server
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routes/
│   │   └── services/
│   ├── venv/
│   ├── requirements.txt
│   └── training_data.jsonl
└── README.md
```

## colors

- background: `#020408` (almost black)
- primary: `#00d9ff` (cyan - subtle)
- text: `#e8e8e8` (whiteish grey)
- accent: `#4a5568` (grey)

## dev notes

- python interpreter: `/Users/clasei/code/pipeline/backend/venv/bin/python`
- all text: lowercase
- style: minimal, clean, no clutter
- font: system fonts for readability

## troubleshooting

**port already in use?**
```bash
lsof -ti:3001 | xargs kill -9  # backend
lsof -ti:5173 | xargs kill -9  # frontend
```

**ollama not responding?**
```bash
pkill ollama
ollama serve
```

**python imports failing?**
```bash
cd backend
source venv/bin/activate
python test_server.py
```

## next steps

1. ✅ ui cleanup
2. ✅ connect ollama  
3. ⏳ test training loop
4. ⏳ add real-time metrics
5. ⏳ docker setup

---

built with focus. no fluff.

## 📋 detailed docs

see `/docs` folder for architecture, setup guides, and technical details.


## 📋 Documentation Files

### [ARCHITECTURE.md](.docs/ARCHITECTURE.md)
Comprehensive monorepo architecture plan including:
- Directory structure
- Technology stack (React frontend + Python/FastAPI backend)
- API contract and routes
- Data models
- Communication flow
- Development setup instructions
- Deployment strategy
- Phase implementation plan

### [TECH_STACK_REVIEW.md](.docs/TECH_STACK_REVIEW.md)
Technology stack analysis and best practices:
- Current stack summary
- Best practices assessment
- Production recommendations
- Proposed enhanced dependencies
- Architecture recommendations
- Deployment readiness
- Migration path

### [FRONTEND_SETUP.md](.docs/FRONTEND_SETUP.md)
Frontend-specific setup and information:
- Project structure
- Installation steps
- Running the development server

### [PORT_CONFIGURATION.md](.docs/PORT_CONFIGURATION.md)
Port configuration and troubleshooting:
- Frontend port (3000) explanation
- Backend port (3001) explanation
- Why Vite defaults to 5173
- How to prevent port conflicts
- Docker Compose port mapping

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- Python 3.11+
- Docker & Docker Compose (optional)

### Development Setup

**Option 1: Local Installation**

```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend (in another terminal)
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 3001
```

**Option 2: Docker Compose**

```bash
docker-compose up --build
```

### Access the Application
- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://localhost:3001
- **API Documentation:** http://localhost:3001/docs
- **PostgreSQL (Docker only):** localhost:5432

## 📁 Directory Structure

```
pipeline/
├── frontend/                    # React/TypeScript dashboard
│   ├── src/
│   ├── components/
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── backend/                     # Python/FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── db/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md
│   ├── TECH_STACK_REVIEW.md
│   ├── FRONTEND_SETUP.md
│   └── README.md
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔧 Configuration

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Configuration options:
- `VITE_API_URL` - Backend API endpoint (frontend)
- `API_HOST` - Backend host (backend)
- `API_PORT` - Backend port (backend)
- `DATABASE_URL` - Database connection string
- `DEBUG` - Debug mode toggle
- `GEMINI_API_KEY` - Optional AI integration

## 📚 API Routes

### Training Endpoints
- `GET /api/training` - List all trainings
- `POST /api/training` - Start new training
- `GET /api/training/{id}` - Get training details
- `PATCH /api/training/{id}` - Update training

### Checkpoints
- `GET /api/checkpoints` - List checkpoints
- `POST /api/training/{id}/checkpoint` - Save checkpoint

### WebSocket
- `WS /ws/training/{id}` - Real-time updates

### Health
- `GET /api/health` - Health check

## 🎯 Project Goals

Pipeline.OS is a **local LLM training dashboard** that:
- Monitors real-time training progress
- Displays live logs, loss metrics, and throughput
- Allows hyperparameter tuning during training
- Manages model checkpoints
- Provides a chat interface for training insights

## 🛠️ Tech Stack Summary

| Component | Technology | Version |
|-----------|-----------|---------|
| Frontend | React | 19.2.4 |
| Language | TypeScript | 5.8.2 |
| Build Tool | Vite | 6.2.0 |
| Styling | Tailwind CSS | CDN |
| Backend Framework | FastAPI | 0.104.1 |
| Backend Language | Python | 3.11+ |
| Database | SQLite / PostgreSQL | - |
| Containerization | Docker | - |

## 📖 Next Steps

1. **Setup**: Follow the Quick Start section above
2. **Development**: Modify components in `frontend/` and routes in `backend/`
3. **Testing**: Use http://localhost:3001/docs for API testing
4. **Deployment**: See ARCHITECTURE.md for deployment strategies

## 🤝 Contributing

When adding features:
1. Update relevant .md files in `docs/`
2. Follow the architecture patterns in ARCHITECTURE.md
3. Ensure database migrations are included
4. Test both frontend and backend changes

## 📝 Notes

- Frontend uses CDN-loaded Tailwind (can be migrated to npm build)
- Backend uses SQLite by default (PostgreSQL in docker-compose)
- WebSocket connections handle real-time training updates
- Training simulation is built-in for development/testing

---

For detailed architecture information, see [ARCHITECTURE.md](.docs/ARCHITECTURE.md)  
For tech stack analysis, see [TECH_STACK_REVIEW.md](.docs/TECH_STACK_REVIEW.md)


