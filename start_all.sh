#!/bin/bash
# Complete startup for pipelinex with Ollama training

echo "🚀 Starting pipelinex - Ollama LLM Trainer"
echo ""
echo "This will start 3 processes:"
echo "  1. Ollama server (port 11434)"
echo "  2. Backend API (port 3001)"
echo "  3. Frontend UI (port 5173)"
echo ""
echo "Press Ctrl+C to stop all processes"
echo ""

# Kill any existing processes on these ports
lsof -ti:11434 | xargs kill -9 2>/dev/null
lsof -ti:3001 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null

# Start Ollama in background
echo "📦 Starting Ollama..."
ollama serve > /tmp/ollama.log 2>&1 &
OLLAMA_PID=$!
sleep 2

# Start backend in background
echo "⚙️  Starting Backend..."
cd backend
source venv/bin/activate 2>/dev/null || (python3.12 -m venv venv && source venv/bin/activate && pip install -r requirements.txt)
python -m uvicorn app.main:app --reload --port 3001 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
cd ..
sleep 3

# Start frontend in foreground
echo "🎨 Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ All services starting!"
echo ""
echo "📊 Frontend:  http://localhost:5173"
echo "⚙️  Backend:   http://localhost:3001"
echo "📦 Ollama:    http://localhost:11434"
echo ""
echo "Logs:"
echo "  Ollama:  tail -f /tmp/ollama.log"
echo "  Backend: tail -f /tmp/backend.log"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait and cleanup on exit
trap "echo ''; echo 'Stopping services...'; kill $OLLAMA_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

wait

