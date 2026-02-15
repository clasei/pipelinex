#!/bin/bash
# pipelinex - start everything in one go

echo "🚀 starting pipelinex..."

# check if we're in the right directory
if [ ! -f "package.json" ] && [ ! -f "requirements.txt" ]; then
    echo "❌ please run this from /Users/clasei/code/pipeline"
    exit 1
fi

# terminal 1: ollama server
echo "📦 checking ollama..."
if ! command -v ollama &> /dev/null; then
    echo "❌ ollama not found. install with: brew install ollama"
    exit 1
fi

echo "✅ ollama found"
echo ""
echo "🔄 starting ollama server on port 11434..."
echo "   (keep this terminal open)"
ollama serve &
OLLAMA_PID=$!

# wait for ollama to start
sleep 3

# terminal 2: backend
echo ""
echo "🔧 starting backend on port 3001..."
(
    cd backend
    if [ ! -d "venv" ]; then
        echo "   creating virtual environment..."
        python3 -m venv venv
    fi
    source venv/bin/activate
    pip install -q -r requirements.txt 2>/dev/null
    python3 -m uvicorn app.main:app --reload --port 3001
) &
BACKEND_PID=$!

# wait for backend to start
sleep 3

# terminal 3: frontend
echo ""
echo "🎨 starting frontend on port 5173..."
(
    cd frontend
    npm install -q 2>/dev/null
    npm run dev
) &
FRONTEND_PID=$!

echo ""
echo "============================================================"
echo "✅ pipelinex is starting!"
echo "============================================================"
echo ""
echo "📊 frontend:  http://localhost:5173"
echo "⚙️  backend:   http://localhost:3001"
echo "📦 ollama:    http://localhost:11434"
echo ""
echo "press ctrl+c to stop all services"
echo ""

# wait for ctrl+c
trap "kill $OLLAMA_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

wait

