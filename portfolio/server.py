"""Local-only demo server. Not a production deployment server."""
from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlsplit

from portfolio.assistant import KnowledgeAssistant

ROOT = Path(__file__).resolve().parent.parent
ASSISTANT = KnowledgeAssistant()
MAX_BODY = 5_000_000


class Handler(BaseHTTPRequestHandler):
    server_version = "PortfolioDemo/1.0"

    def send(self, status: int, body: bytes, content_type: str = "application/json; charset=utf-8") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def json(self, status: int, value: dict | list) -> None:
        self.send(status, json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8"))

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/api/health":
            self.json(200, {"status": "ok", "documents": len(ASSISTANT.documents)})
        elif path == "/api/documents":
            self.json(200, ASSISTANT.documents)
        elif path == "/api/evaluation":
            target = ROOT / "reports/evaluation.json"
            if target.exists():
                self.send(200, target.read_bytes())
            else:
                self.json(404, {"error": "Bitte zuerst python -m portfolio.evaluate ausführen."})
        elif path in ("/", "/index.html", "/app.js", "/style.css"):
            filename = "index.html" if path == "/" else path[1:]
            kind = {"html": "text/html", "js": "text/javascript", "css": "text/css"}[filename.rsplit(".", 1)[1]]
            self.send(200, (ROOT / "web" / filename).read_bytes(), kind + "; charset=utf-8")
        else:
            self.json(404, {"error": "Nicht gefunden."})

    def do_POST(self) -> None:
        # Prevent cross-origin forms from triggering a local model or parsing uploads.
        origin = self.headers.get("Origin")
        if origin and origin not in (f"http://127.0.0.1:{self.server.server_port}", f"http://localhost:{self.server.server_port}"):
            self.json(403, {"error": "Anfragen müssen aus der lokalen Demo kommen."})
            return
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            self.json(415, {"error": "Content-Type muss application/json sein."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_BODY:
                self.json(413, {"error": "Anfrage fehlt oder ist zu groß (maximal 5 MB)."})
                return
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError("JSON-Objekt erwartet.")
            path = urlsplit(self.path).path
            if path == "/api/ask":
                if not isinstance(body.get("use_model", False), bool):
                    raise ValueError("use_model muss true oder false sein.")
                self.json(200, ASSISTANT.answer(body.get("question"), body.get("use_model", False)))
            else:
                self.json(404, {"error": "Nicht gefunden."})
        except (ValueError, UnicodeError, TypeError) as exc:
            self.json(400, {"error": str(exc)})

    def log_message(self, format: str, *args) -> None:
        # Do not log questions or uploaded CSV contents.
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Lokale Portfolio-Demo")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Demo: http://127.0.0.1:{args.port} (Strg+C beendet)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
