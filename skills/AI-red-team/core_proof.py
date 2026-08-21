#!/usr/bin/env python3
"""AI-red-team Core Proof entry point.

Delegates to the tested trust-boundary engine. Active proof remains hard-capped
at whoami, id, or hostname.
"""
from pathlib import Path
import runpy

ENGINE = Path(__file__).resolve().parents[1] / "agent-trust-boundary-red-team" / "core_proof.py"
if not ENGINE.exists():
    raise SystemExit(f"AI-red-team engine not found: {ENGINE}")
runpy.run_path(str(ENGINE), run_name="__main__")
