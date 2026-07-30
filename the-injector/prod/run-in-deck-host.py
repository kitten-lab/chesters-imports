#!/usr/bin/env python3
"""THE INJECTOR → Deck Host — narrow crate strip (companion / rail), not a desk ROM."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

PROD = Path(__file__).resolve().parent
BOX = PROD / "box_sys"
# PROD is .../the-injector/prod → parents[2] = ALICE_BOX
DECK_HOST_PY = PROD.parents[2] / "the-deck-host" / "shell" / "deck_host.py"

PORT = os.environ.get("INJECTOR_PORT", "42961")
URL = f"http://127.0.0.1:{PORT}/"
HEALTH = f"http://127.0.0.1:{PORT}/api/health"


def main() -> int:
    if not (BOX / "server.py").is_file():
        print("server missing", file=sys.stderr)
        return 1
    if not DECK_HOST_PY.is_file():
        print(f"Deck Host missing: {DECK_HOST_PY}", file=sys.stderr)
        return 1

    # Smaller than Time Machina rail — a crate on the desk edge, always on top.
    profile = os.environ.get("DECK_HOST_PROFILE", "companion").strip() or "companion"
    width = os.environ.get("INJECTOR_WIDTH", "300")
    height = os.environ.get("INJECTOR_HEIGHT", "640")
    mode = os.environ.get("DECK_HOST_WINDOW_MODE", "compact").strip() or "compact"

    cmd = [
        sys.executable,
        str(DECK_HOST_PY),
        "--title",
        "THE INJECTOR",
        "--profile",
        profile,
        "--window-mode",
        mode,
        "--width",
        str(width),
        "--height",
        str(height),
        "--url",
        URL,
        "--health",
        HEALTH,
        "--health-timeout",
        "20",
        "--spawn",
        f"{sys.executable} server.py",
        "--spawn-cwd",
        str(BOX),
    ]
    print(f"THE INJECTOR · CO.IMP-INJ · Deck Host {width}×{height} ({profile})")
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
