#!/usr/bin/env python3
"""
Servidor porra-mundial — sirve el HTML estático y una mini API REST
para persistir el estado en data.json (compartido entre todos los navegadores).
"""
import json, os, threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data.json"
lock = threading.Lock()

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # silenciar logs de acceso

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/state":
            with lock:
                if DATA_FILE.exists():
                    data = DATA_FILE.read_bytes()
                else:
                    data = b"{}"
            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(data)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/state":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                json.loads(body)  # validar JSON
                with lock:
                    DATA_FILE.write_bytes(body)
                self.send_response(200)
                self._cors()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            except Exception as e:
                self.send_response(400)
                self._cors()
                self.end_headers()
                self.wfile.write(f'{{"error":"{e}"}}'.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    port = 8765
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"✅ Porra server corriendo en http://0.0.0.0:{port}")
    server.serve_forever()
