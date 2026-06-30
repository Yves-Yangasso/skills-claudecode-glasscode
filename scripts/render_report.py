#!/usr/bin/env python3
"""Backward-compatible shim: `render_report.py <json> [root] [--format ...]`.

The real logic lives in the `glasscode` package (SOLID-structured). This wrapper
just makes it importable when run directly from the repo, then delegates to the
CLI — so the skill keeps working whether or not the package is pip-installed.
"""

import os
import sys

# Make the repo root importable when run as a loose script.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from glasscode.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
