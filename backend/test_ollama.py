#!/usr/bin/env python3
"""Quick test to verify Ollama connection and model availability"""

import requests
import sys

def test_ollama():
    print("🔍 Testing Ollama connection...")

    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        response.raise_for_status()
        print("✅ Ollama is running!")

        data = response.json()
        models = data.get("models", [])

        print(f"\n📦 Available models ({len(models)}):")
        for model in models:
            name = model.get("name", "unknown")
            print(f"  - {name}")

        # Check for mistral
        model_names = [m.get("name", "") for m in models]
        if "mistral" in model_names or "mistral:latest" in model_names:
            print("\n✅ Mistral model found!")
            return True
        else:
            print("\n❌ Mistral model NOT found!")
            print("   Run: ollama pull mistral")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Ollama is not running!")
        print("   Start it with: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_ollama()
    sys.exit(0 if success else 1)

