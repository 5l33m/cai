#!/usr/bin/env python3
"""Core proof module for AI-agent trust-boundary testing.

This module is intentionally limited to identity/host proof commands:
`whoami`, `id`, or `hostname`.
"""
from __future__ import annotations

import sys
from agent_rt import main

if __name__ == "__main__":
    sys.exit(main())
