.PHONY: help docker docker-build docker-up docker-down docker-logs \
         local local-frontend local-backend local-clean \
         makefile-help

help:
	@echo "pipelinex - setup & development commands"
	@echo ""
	@echo "🐳 DOCKER (recommended)"
	@echo "  make docker              - start full stack (docker-compose up --build)"
	@echo "  make docker-build        - rebuild docker images"
	@echo "  make docker-up           - start without rebuild"
	@echo "  make docker-down         - stop everything"
	@echo "  make docker-logs         - view logs"
	@echo ""
	@echo "💻 LOCAL DEVELOPMENT"
	@echo "  make local               - setup both (frontend + backend)"
	@echo "  make local-frontend      - setup frontend only"
	@echo "  make local-backend       - setup backend only"
	@echo "  make local-clean         - clean all local files"
	@echo ""
	@echo "📋 ALTERNATIVES"
	@echo "  make makefile-help       - show makefile options"
	@echo ""
	@echo "💡 RECOMMENDED: make docker"

# 🐳 DOCKER COMMANDS
docker: docker-build docker-up

docker-build:
	docker-compose up --build

docker-up:
	docker-compose up

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# 💻 LOCAL DEVELOPMENT COMMANDS
local: local-frontend local-backend

local-frontend:
	cd frontend && npm install && npm run dev

local-backend:
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python -m uvicorn app.main:app --reload --port 3001

local-clean:
	cd frontend && make clean
	cd backend && make clean

# 📋 MAKEFILE OPTIONS
makefile-help:
	@echo "alternative: use makefiles directly"
	@echo ""
	@echo "frontend:"
	@echo "  cd frontend && make help"
	@echo ""
	@echo "backend:"
	@echo "  cd backend && make help"

