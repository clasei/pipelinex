#!/usr/bin/env python3
"""quick test to see if server can import properly"""

import sys
sys.path.insert(0, '/Users/clasei/code/pipeline/backend')

print("testing imports...")

try:
    print("importing fastapi...")
    from fastapi import FastAPI
    print("✅ fastapi ok")

    print("importing config...")
    from app.config import settings
    print(f"✅ config ok - port: {settings.API_PORT}")

    print("importing routes...")
    from app.routes import training
    print("✅ routes ok")

    print("importing main app...")
    from app.main import app
    print(f"✅ app ok - {app.title}")

    print("\n🎉 all imports successful!")
    print("\nnow run:")
    print("cd /Users/clasei/code/pipeline/backend")
    print("source venv/bin/activate")
    print("python -m uvicorn app.main:app --reload --port 3001")

except Exception as e:
    print(f"\n❌ error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

