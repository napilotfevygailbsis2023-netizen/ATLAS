#!/usr/bin/env python3
"""
ATLAS — Luzon Travel Companion
================================
HOW TO RUN LOCALLY:
    python main.py
    Open: http://localhost:5000

DEPLOYED ON RAILWAY:
    Automatically runs on the assigned PORT
"""

import http.server, socketserver, urllib.parse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))))

import index, flights, weather, attractions, restaurants, guides, transport, itinerary, login, register

PORT = int(os.environ.get("PORT", 5000))

ROUTES = {
    "/":               lambda p: index.render(),
    "/index.py":       lambda p: index.render(),
    "/flights.py":     lambda p: flights.render(p),
    "/weather.py":     lambda p: weather.render(p.get("location","Manila")),
    "/attractions.py": lambda p: attractions.render(p.get("city","All"), p.get("cat","All"), p.get("kw","")),
    "/restaurants.py": lambda p: restaurants.render(p.get("city","All"), p.get("kw","")),
    "/guides.py":      lambda p: guides.render(p.get("city","All"), p.get("lang","All")),
    "/transport.py":   lambda p: transport.render(p.get("type","All"), p.get("from","All")),
    "/itinerary.py":   lambda p: itinerary.render(p.get("dest","Manila")),
    "/login.py":       lambda p: login.render(),
    "/register.py":    lambda p: register.render(),
}

CSS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "css", "styles.css")

class ATLASHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = dict(urllib.parse.parse_qsl(parsed.query))
        path   = parsed.path

        if path == "/css/styles.css":
            with open(CSS_PATH, "rb") as f:
                css = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.send_header("Content-Length", str(len(css)))
            self.end_headers()
            self.wfile.write(css)
            return

        handler = ROUTES.get(path)
        if handler is None:
            self.send_error(404, "Page not found")
            return

        html = handler(params).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    print("=" * 50)
    print("  ATLAS — Luzon Travel Companion")
    print("=" * 50)
    print(f"\n  Running at http://localhost:{PORT}")
    print(f"  Ctrl+C to stop\n")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), ATLASHandler) as s:
        try:
            s.serve_forever()
        except KeyboardInterrupt:
            print("\n  Goodbye!")
