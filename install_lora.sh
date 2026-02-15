#!/bin/bash
# LoRA Training Installation Script
# Run this to install all LoRA training dependencies

set -e

echo "🎓 LoRA Training Installation"
echo "================================"
echo ""

# Navigate to backend
cd "$(dirname "$0")/backend"

# Activate venv
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating venv..."
    python3.12 -m venv venv
fi

source venv/bin/activate

echo "📦 Installing LoRA training dependencies..."
echo "This will take 10-15 minutes and download ~5-10 GB"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install PyTorch (largest download)
echo ""
echo "📥 Installing PyTorch (this is the big one, ~2-3 GB)..."
pip install torch torchvision torchaudio

# Install Transformers and core libraries
echo ""
echo "📥 Installing Transformers and PEFT..."
pip install transformers>=4.36.0
pip install peft>=0.7.0
pip install accelerate>=0.25.0

# Install dataset tools
echo ""
echo "📥 Installing dataset tools..."
pip install datasets>=2.14.0

# Install training utilities
echo ""
echo "📥 Installing training utilities..."
pip install trl>=0.7.0
pip install scipy>=1.11.0
pip install scikit-learn>=1.3.0

# Install quantization (optional, may not work on all systems)
echo ""
echo "📥 Installing BitsAndBytes (optional)..."
pip install bitsandbytes || echo "⚠️  BitsAndBytes install failed (this is optional)"

# Install tokenizers
echo ""
echo "📥 Installing tokenizers..."
pip install tokenizers>=0.15.0
pip install sentencepiece>=0.1.99

echo ""
echo "================================"
echo "✅ Installation Complete!"
echo "================================"
echo ""

# Test installation
echo "🧪 Testing installation..."
python << 'EOF'
import sys

print("\n🔍 Checking installed packages:\n")

# Check PyTorch
try:
    import torch
    print(f"✅ PyTorch: {torch.__version__}")
    print(f"   MPS (Apple Silicon GPU) available: {torch.backends.mps.is_available()}")
    print(f"   MPS built: {torch.backends.mps.is_built()}")
    if torch.backends.mps.is_available():
        print("   🍎 Your Mac M3 GPU will be used for training!")
except ImportError as e:
    print(f"❌ PyTorch: FAILED - {e}")
    sys.exit(1)

# Check Transformers
try:
    import transformers
    print(f"✅ Transformers: {transformers.__version__}")
except ImportError as e:
    print(f"❌ Transformers: FAILED - {e}")
    sys.exit(1)

# Check PEFT (LoRA)
try:
    import peft
    print(f"✅ PEFT (LoRA): {peft.__version__}")
except ImportError as e:
    print(f"❌ PEFT: FAILED - {e}")
    sys.exit(1)

# Check Accelerate
try:
    import accelerate
    print(f"✅ Accelerate: {accelerate.__version__}")
except ImportError as e:
    print(f"❌ Accelerate: FAILED - {e}")
    sys.exit(1)

# Check Datasets
try:
    import datasets
    print(f"✅ Datasets: {datasets.__version__}")
except ImportError as e:
    print(f"❌ Datasets: FAILED - {e}")
    sys.exit(1)

# Check BitsAndBytes (optional)
try:
    import bitsandbytes
    print(f"✅ BitsAndBytes: Installed")
except ImportError:
    print(f"⚠️  BitsAndBytes: Not installed (optional, you can still train)")

# Test LoRA trainer import
try:
    from app.services.lora_trainer import LoRATrainer, LoRATrainingConfig
    print(f"✅ LoRATrainer: Ready to use!")
except ImportError as e:
    print(f"❌ LoRATrainer: FAILED - {e}")
    sys.exit(1)

print("\n🎉 All checks passed! LoRA training is ready!")
print("\n📚 Next steps:")
print("   1. Restart your backend: python -m uvicorn app.main:app --reload --port 3001")
print("   2. Start LoRA training: POST /api/lora/train/start")
print("   3. See LORA_TRAINING_GUIDE.md for full instructions")
EOF

echo ""
echo "🎉 Setup complete! You're ready for real LoRA training!"

