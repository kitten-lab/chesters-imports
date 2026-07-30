#!/usr/bin/env python3
"""THE INJECTOR — Chester's Imports · crate post (static + health + mail proxy)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

BOX_SYS = Path(__file__).resolve().parent
HOST = "127.0.0.1"
# Launcher recipe must match this (was wrongly 43100 in launches.json).
PORT = int(os.environ.get("INJECTOR_PORT", "42961"))
# Terminal network mail inject — browser never talks to this directly (CORS / pywebview).
DEFAULT_WIRE = os.environ.get(
    "INJECTOR_WIRE",
    "http://127.0.0.1:43101/api/mail/inject",
)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BOX_SYS), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[injector] {args[0] if args else fmt}")

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, code: int, obj: dict) -> None:
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers", "Content-Type, X-Mail-Token"
        )
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in ("/api/health", "/health"):
            self._json(
                200,
                {
                    "ok": True,
                    "product": "the-injector",
                    "sku": "CO.IMP-INJ",
                    "house": "CHESTERS-IMPORTS",
                    "port": PORT,
                    "wire": DEFAULT_WIRE,
                    "job": "force outside mail into station inboxes",
                    "mood": "unsettling",
                },
            )
            return
        if path in ("/", ""):
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path != "/api/inject":
            self.send_error(404, "not a crate door")
            return

        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n > 0 else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._json(400, {"ok": False, "error": "crate is not JSON"})
            return

        if not isinstance(payload, dict):
            self._json(400, {"ok": False, "error": "crate is not an object"})
            return

        # Optional override wire (advanced UI); default terminal inject URL
        wire = str(payload.pop("wire", "") or "").strip() or DEFAULT_WIRE
        if not wire.startswith("http://127.0.0.1") and not wire.startswith(
            "http://localhost"
        ):
            self._json(
                400,
                {
                    "ok": False,
                    "error": "wire must stay on localhost (this desk only)",
                },
            )
            return

        token = str(payload.get("token") or "")
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            wire,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "X-Mail-Token": token,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = resp.read()
                code = resp.status
        except urllib.error.HTTPError as e:
            data = e.read() if e.fp else b""
            code = e.code
        except urllib.error.URLError as e:
            self._json(
                502,
                {
                    "ok": False,
                    "error": f"wall silent — is TERMINALS (sdk-import) up? ({e.reason})",
                    "wire": wire,
                },
            )
            return
        except TimeoutError:
            self._json(
                504,
                {"ok": False, "error": "wire timed out", "wire": wire},
            )
            return

        try:
            out = json.loads(data.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            out = {
                "ok": False,
                "error": f"station returned non-JSON (HTTP {code})",
                "raw": data.decode("utf-8", errors="replace")[:400],
            }
            code = 502

        if not isinstance(out, dict):
            out = {"ok": False, "error": "station returned a non-object"}

        # Pass through station status when sensible
        if code >= 400 and out.get("ok") is not False:
            out.setdefault("ok", False)
            out.setdefault("error", f"HTTP {code}")
        self._json(code if 200 <= code < 600 else 502, out)


def main() -> int:
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print("THE INJECTOR · Chester's Imports · CO.IMP-INJ")
    print(f"  http://{HOST}:{PORT}/")
    print(f"  proxy → {DEFAULT_WIRE}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\ncrate window closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
