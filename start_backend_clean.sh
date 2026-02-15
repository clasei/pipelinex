#!/bin/bash
# Quick start script for pipelinex backend

cd "$(dirname "$0")/backend"

echo "🚀 Starting pipelinex backend..."
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3.12 -m venv venv
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✅ Ready to start!"
echo ""
echo "Starting uvicorn server on http://localhost:3001..."
echo ""

# Start server
python -m uvicorn app.main:app --reload --port 3001

