#!/usr/bin/env python3
import http.server, socketserver, urllib.parse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import index, flights, weather, attractions, restaurants, guides, transport, itinerary, login, register, db

PORT = int(os.environ.get("PORT", 5000))
BASE = os.path.dirname(os.path.abspath(__file__))
CSS  = os.path.join(BASE, "css", "styles.css")

ROUTES = {
    "/":               lambda p, u: index.render(u),
    "/index.py":       lambda p, u: index.render(u),
    "/flights.py":     lambda p, u: flights.render(p, u),
    "/weather.py":     lambda p, u: weather.render(p.get("location","Manila"), u),
    "/attractions.py": lambda p, u: attractions.render(p.get("city","All"), p.get("cat","All"), p.get("kw",""), u),
    "/restaurants.py": lambda p, u: restaurants.render(p.get("city","All"), p.get("kw",""), u),
    "/guides.py":      lambda p, u: guides.render(p.get("city","All"), p.get("lang","All"), u),
    "/transport.py":   lambda p, u: transport.render(p.get("type","All"), p.get("from","All"), u),
    "/itinerary.py":   lambda p, u: itinerary.render(p.get("dest","Manila"), u),
    "/login.py":       lambda p, u: login.render(),
    "/register.py":    lambda p, u: register.render(),
}

def get_token(cookie_header):
    if not cookie_header:
        return None
    for part in cookie_header.split(";"):
        part = part.strip()
        if part.startswith("atlas_token="):
            return part[len("atlas_token="):]
    return None

class ATLASHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = dict(urllib.parse.parse_qsl(parsed.query))
        path   = parsed.path
        token  = get_token(self.headers.get("Cookie",""))
        user   = db.get_user_by_token(token)

        # Serve CSS
        if path == "/css/styles.css":
            with open(CSS,"rb") as f: css = f.read()
            self.send_response(200)
            self.send_header("Content-Type","text/css; charset=utf-8")
            self.send_header("Content-Length",str(len(css)))
            self.end_headers()
            self.wfile.write(css)
            return

        # Logout
        if path == "/logout.py":
            if token:
                db.logout(token)
            self.send_response(302)
            self.send_header("Location","/")
            self.send_header("Set-Cookie","atlas_token=; Path=/; Max-Age=0")
            self.end_headers()
            return

        handler = ROUTES.get(path)
        if handler is None:
            self.send_error(404, "Page not found")
            return

        html = handler(params, user).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type","text/html; charset=utf-8")
        self.send_header("Content-Length",str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        length = int(self.headers.get("Content-Length",0))
        body = self.rfile.read(length).decode("utf-8")
        form = dict(urllib.parse.parse_qsl(body))

        if path == "/login.py":
            token, error_html = login.handle_post(form)
            if token:
                self.send_response(302)
                self.send_header("Location","/")
                self.send_header("Set-Cookie",f"atlas_token={token}; Path=/; Max-Age=86400")
                self.end_headers()
            else:
                html = error_html.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type","text/html; charset=utf-8")
                self.send_header("Content-Length",str(len(html)))
                self.end_headers()
                self.wfile.write(html)

        elif path == "/register.py":
            ok, html_response = register.handle_post(form)
            html = html_response.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type","text/html; charset=utf-8")
            self.send_header("Content-Length",str(len(html)))
            self.end_headers()
            self.wfile.write(html)
        else:
            self.send_error(404)

    def log_message(self, *a): pass

if __name__ == "__main__":
    print("="*50)
    print("  ATLAS - Luzon Travel Companion")
    print("="*50)
    print(f"\n  Running at http://localhost:{PORT}")
    print("  Ctrl+C to stop\n")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), ATLASHandler) as s:
        try:
            s.serve_forever()
        except KeyboardInterrupt:
            print("\n  Goodbye!")
