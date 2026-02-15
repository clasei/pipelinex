#!/bin/bash
# pipelinex startup script

set -e

echo "🚀 starting pipelinex..."
echo ""

# check if ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ ollama not running"
    echo "start it in a separate terminal: ollama serve"
    exit 1
fi

echo "✅ ollama running"

# check training data
if [ ! -f "backend/training_data.jsonl" ]; then
    echo "❌ training data not found at backend/training_data.jsonl"
    exit 1
fi

echo "✅ training data found"

# start backend
echo ""
echo "starting backend on port 3001..."
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 3001

