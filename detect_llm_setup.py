#!/usr/bin/env python3
"""
Detect which LLM setup you have on your mac
Run this to find your models
"""

import os
import json
from pathlib import Path

def check_ollama():
    """Check if ollama is installed and list models"""
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            return {
                'installed': True,
                'output': result.stdout
            }
    except:
        pass
    return {'installed': False}

def check_lm_studio():
    """Check if LM Studio models exist"""
    path = Path.home() / "Library/Application Support/LM Studio/models"
    if path.exists():
        models = list(path.glob("*"))
        return {
            'installed': True,
            'path': str(path),
            'models': [m.name for m in models]
        }
    return {'installed': False}

def check_huggingface():
    """Check if HuggingFace models exist"""
    path = Path.home() / ".cache/huggingface/hub"
    if path.exists():
        models = list(path.glob("models--*"))
        return {
            'installed': True,
            'path': str(path),
            'count': len(models),
            'models': [m.name for m in models[:5]]  # first 5
        }
    return {'installed': False}

def check_gguf_files():
    """Search for GGUF files"""
    home = Path.home()
    gguf_files = []

    # search common locations
    common_paths = [
        home / ".cache/lm-studio",
        home / "llm",
        home / "models",
        home / "Downloads",
    ]

    for search_path in common_paths:
        if search_path.exists():
            gguf_files.extend(search_path.glob("**/*.gguf"))

    return {
        'found': len(gguf_files) > 0,
        'files': [str(f) for f in gguf_files[:10]]
    }

def main():
    print("🔍 detecting llm setup on your mac...\n")

    print("=" * 60)
    print("OLLAMA")
    print("=" * 60)
    ollama = check_ollama()
    if ollama['installed']:
        print("✅ ollama installed!")
        print(ollama['output'])
    else:
        print("❌ ollama not installed")

    print("\n" + "=" * 60)
    print("LM STUDIO")
    print("=" * 60)
    lm_studio = check_lm_studio()
    if lm_studio['installed']:
        print(f"✅ lm studio models found at: {lm_studio['path']}")
        print(f"models: {', '.join(lm_studio['models'][:5])}")
    else:
        print("❌ lm studio models not found")

    print("\n" + "=" * 60)
    print("HUGGINGFACE")
    print("=" * 60)
    hf = check_huggingface()
    if hf['installed']:
        print(f"✅ huggingface models found at: {hf['path']}")
        print(f"count: {hf['count']} models")
        print(f"sample: {', '.join(hf['models'][:3])}")
    else:
        print("❌ huggingface models not found")

    print("\n" + "=" * 60)
    print("GGUF FILES (llama.cpp)")
    print("=" * 60)
    gguf = check_gguf_files()
    if gguf['found']:
        print(f"✅ found {len(gguf['files'])} gguf files:")
        for f in gguf['files'][:5]:
            print(f"   - {f}")
    else:
        print("❌ no gguf files found")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    has_setup = any([
        ollama['installed'],
        lm_studio['installed'],
        hf['installed'],
        gguf['found']
    ])

    if has_setup:
        print("✅ you have models! tell me which setup above and i'll connect it")
    else:
        print("❌ no models found")
        print("\ndo this to get started:")
        print("  brew install ollama")
        print("  ollama pull mistral")

if __name__ == "__main__":
    main()

