#!/usr/bin/env python3
"""
Servidor porra-mundial - HTML estatico.
"""
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    server = HTTPServer(("0.0.0.0", 8765), Handler)
    server.timeout = 10
    print("Porra server en http://0.0.0.0:8765")
    server.serve_forever()
