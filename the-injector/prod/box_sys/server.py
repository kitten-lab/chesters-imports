#!/usr/bin/env python3
"""THE INJECTOR — Chester's Imports · weird wire UI (static + health)."""

from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

BOX_SYS = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 42961  # Chester crate post — not DATBOX / not sopr


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BOX_SYS), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[injector] {args[0] if args else fmt}")

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in ("/api/health", "/health"):
            raw = json.dumps(
                {
                    "ok": True,
                    "product": "the-injector",
                    "house": "CHESTERS-IMPORTS",
                    "port": PORT,
                    "job": "force outside mail into station inboxes",
                    "mood": "unsettling",
                }
            ).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return
        if path in ("/", ""):
            self.path = "/index.html"
        return super().do_GET()


def main() -> int:
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print("THE INJECTOR · Chester's Imports")
    print(f"  http://{HOST}:{PORT}/")
    print("  Aim FORCE DELIVERY at a running terminal mail inject URL.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\ncrate window closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
