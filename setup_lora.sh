#!/bin/bash
# Setup LoRA training environment

echo "🎓 Setting up LoRA training environment..."
echo ""

cd "$(dirname "$0")/backend"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.12 -m venv venv
fi

# Activate venv
source venv/bin/activate

echo "📦 Installing LoRA training dependencies..."
echo "This will take 10-15 minutes and download ~5-10 GB..."
echo ""

# Install base requirements first
pip install --upgrade pip
pip install -r requirements.txt

# Install training requirements
pip install -r requirements-training.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "🧪 Testing setup..."

# Test import
python -c "
from app.services.lora_trainer import LoRATrainer
import torch
print('✅ LoRA trainer ready!')
print(f'🔧 Device: CUDA={torch.cuda.is_available()}, MPS={torch.backends.mps.is_available()}')
"

echo ""
echo "🎉 All set! You can now:"
echo "   1. Start backend: python -m uvicorn app.main:app --reload --port 3001"
echo "   2. Start LoRA training via API: POST /api/lora/train/start"
echo ""
echo "📚 See LORA_TRAINING_GUIDE.md for full instructions"

