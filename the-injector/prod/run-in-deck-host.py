#!/usr/bin/env python3
"""Launch THE INJECTOR under Deck Host (companion-ish / desk)."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

PROD = Path(__file__).resolve().parent
BOX = PROD / "box_sys"
PORT = 42961
URL = f"http://127.0.0.1:{PORT}/"

# Deck Host lives as sibling island
DECK = Path(__file__).resolve().parents[3] / "the-deck-host" / "shell" / "deck_host.py"


def main() -> int:
    server = subprocess.Popen(
        [sys.executable, str(BOX / "server.py")],
        cwd=str(BOX),
    )
    time.sleep(0.6)
    if not DECK.is_file():
        print("Deck Host not found; open browser:", URL)
        print("server pid", server.pid)
        return 0
    # default desk profile — weird product still a window
    cmd = [
        sys.executable,
        str(DECK),
        "--url",
        URL,
        "--title",
        "THE INJECTOR",
        "--profile",
        "desk",
    ]
    try:
        subprocess.call(cmd)
    finally:
        server.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
