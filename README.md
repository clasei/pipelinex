# Pipeline.OS Documentation

Complete guides and architecture documentation for the Pipeline.OS project.

## 📋 Documentation Files

### [ARCHITECTURE.md](docs/ARCHITECTURE.md)
Comprehensive monorepo architecture plan including:
- Directory structure
- Technology stack (React frontend + Python/FastAPI backend)
- API contract and routes
- Data models
- Communication flow
- Development setup instructions
- Deployment strategy
- Phase implementation plan

### [TECH_STACK_REVIEW.md](docs/TECH_STACK_REVIEW.md)
Technology stack analysis and best practices:
- Current stack summary
- Best practices assessment
- Production recommendations
- Proposed enhanced dependencies
- Architecture recommendations
- Deployment readiness
- Migration path

### [FRONTEND_SETUP.md](docs/FRONTEND_SETUP.md)
Frontend-specific setup and information:
- Project structure
- Installation steps
- Running the development server

### [PORT_CONFIGURATION.md](docs/PORT_CONFIGURATION.md)
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

For detailed architecture information, see [ARCHITECTURE.md](docs/ARCHITECTURE.md)  
For tech stack analysis, see [TECH_STACK_REVIEW.md](docs/TECH_STACK_REVIEW.md)


