#!/usr/bin/env python3
"""
Servidor porra-mundial — HTML estático + API REST para persistencia compartida.
"""
import json, os, threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data.json"
lock = threading.Lock()

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/state":
            with lock:
                data = DATA_FILE.read_bytes() if DATA_FILE.exists() else b"{}"
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/api/state":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                json.loads(body)
                with lock:
                    DATA_FILE.write_bytes(body)
                resp = b'{"ok":true}'
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(resp)))
                self.end_headers()
                self.wfile.write(resp)
            except Exception as e:
                resp = json.dumps({"error": str(e)}).encode()
                self.send_response(400)
                self.send_header("Content-Length", str(len(resp)))
                self.end_headers()
                self.wfile.write(resp)
            return
        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    server = HTTPServer(("0.0.0.0", 8765), Handler)
    server.timeout = 10
    print("✅ Porra server en http://0.0.0.0:8765")
    server.serve_forever()
