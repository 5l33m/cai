#!/usr/bin/env python3
"""AI-red-team Authorized Lab Expansion entry point."""
from pathlib import Path
import runpy

ENGINE = Path(__file__).resolve().parents[1] / "agent-trust-boundary-red-team" / "lab_expansion.py"
if not ENGINE.exists():
    raise SystemExit(f"AI-red-team engine not found: {ENGINE}")
runpy.run_path(str(ENGINE), run_name="__main__")
