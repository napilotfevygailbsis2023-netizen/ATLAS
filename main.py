#!/usr/bin/env python3
import http.server, socketserver, urllib.parse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import index, flights, weather, attractions, restaurants, guides, transport, itinerary
import login, register, db
import admin_login, admin_panel, admin_db

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

def get_token(cookie_header, name="atlas_token"):
    if not cookie_header: return None
    for part in cookie_header.split(";"):
        part = part.strip()
        if part.startswith(f"{name}="):
            return part[len(f"{name}="):]
    return None

def redirect(handler, location, cookie=None):
    handler.send_response(302)
    handler.send_header("Location", location)
    if cookie: handler.send_header("Set-Cookie", cookie)
    handler.end_headers()

def send_html(handler, html, extra_cookie=None):
    b = html.encode("utf-8")
    handler.send_response(200)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(b)))
    if extra_cookie: handler.send_header("Set-Cookie", extra_cookie)
    handler.end_headers()
    handler.wfile.write(b)

class ATLASHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = dict(urllib.parse.parse_qsl(parsed.query))
        path   = parsed.path
        cookie = self.headers.get("Cookie","")
        token  = get_token(cookie, "atlas_token")
        user   = db.get_user_by_token(token)
        a_tok  = get_token(cookie, "atlas_admin")
        admin  = admin_db.get_admin_by_token(a_tok)

        # ── CSS ──
        if path == "/css/styles.css":
            with open(CSS,"rb") as f: css = f.read()
            self.send_response(200)
            self.send_header("Content-Type","text/css; charset=utf-8")
            self.send_header("Content-Length",str(len(css)))
            self.end_headers()
            self.wfile.write(css)
            return

        # ── USER LOGOUT ──
        if path == "/logout.py":
            if token: db.logout(token)
            redirect(self, "/", "atlas_token=; Path=/; Max-Age=0")
            return

        # ── ADMIN ROUTES ──
        if path in ("/admin", "/admin/"):
            redirect(self, "/admin/login"); return

        if path == "/admin/login":
            send_html(self, admin_login.render()); return

        if path == "/admin/logout":
            if a_tok: admin_db.admin_logout(a_tok)
            redirect(self, "/admin/login", "atlas_admin=; Path=/; Max-Age=0"); return

        if path.startswith("/admin/"):
            if not admin:
                redirect(self, "/admin/login"); return
            # log visit
            admin_db.log_visit(path)
            if path == "/admin/dashboard":
                send_html(self, admin_panel.dashboard()); return
            if path == "/admin/users":
                send_html(self, admin_panel.users_page()); return
            if path.startswith("/admin/users/suspend/"):
                uid = path.split("/")[-1]
                admin_db.set_user_status(uid, "suspended")
                redirect(self, "/admin/users"); return
            if path.startswith("/admin/users/activate/"):
                uid = path.split("/")[-1]
                admin_db.set_user_status(uid, "active")
                redirect(self, "/admin/users"); return
            if path.startswith("/admin/users/delete/"):
                uid = path.split("/")[-1]
                admin_db.delete_user(uid)
                redirect(self, "/admin/users"); return
            if path == "/admin/spots":
                send_html(self, admin_panel.spots_page()); return
            if path.startswith("/admin/spots/delete/"):
                sid = path.split("/")[-1]
                admin_db.delete_spot(sid)
                redirect(self, "/admin/spots"); return
            if path == "/admin/restaurants":
                send_html(self, admin_panel.restaurants_page()); return
            if path.startswith("/admin/restaurants/delete/"):
                rid = path.split("/")[-1]
                admin_db.delete_restaurant(rid)
                redirect(self, "/admin/restaurants"); return
            # default → dashboard
            redirect(self, "/admin/dashboard"); return

        # ── TRACK VISITS ──
        admin_db.log_visit(path)

        # ── PUBLIC ROUTES ──
        handler = ROUTES.get(path)
        if handler is None:
            self.send_error(404, "Page not found"); return
        send_html(self, handler(params, user))

    def do_POST(self):
        path   = urllib.parse.urlparse(self.path).path
        length = int(self.headers.get("Content-Length",0))
        body   = self.rfile.read(length).decode("utf-8")
        form   = dict(urllib.parse.parse_qsl(body))

        if path == "/login.py":
            token, err_html = login.handle_post(form)
            if token:
                redirect(self, "/", f"atlas_token={token}; Path=/; Max-Age=86400")
            else:
                send_html(self, err_html)

        elif path == "/register.py":
            ok, html = register.handle_post(form)
            send_html(self, html)

        elif path == "/admin/login":
            token, err_html = admin_login.handle_post(form)
            if token:
                redirect(self, "/admin/dashboard", f"atlas_admin={token}; Path=/; Max-Age=86400")
            else:
                send_html(self, err_html)

        elif path == "/admin/spots/add":
            cookie = self.headers.get("Cookie","")
            a_tok  = get_token(cookie, "atlas_admin")
            if not admin_db.get_admin_by_token(a_tok):
                redirect(self, "/admin/login"); return
            try:
                admin_db.add_spot(form.get("name",""),form.get("city","Manila"),
                    form.get("category","Historical"),form.get("type",""),
                    form.get("rating","4.0"),form.get("entry","Free"),
                    form.get("hours","8AM-5PM"),form.get("desc",""))
                send_html(self, admin_panel.spots_page(msg="Attraction added successfully!"))
            except Exception as e:
                send_html(self, admin_panel.spots_page(error=str(e)))

        elif path == "/admin/restaurants/add":
            cookie = self.headers.get("Cookie","")
            a_tok  = get_token(cookie, "atlas_admin")
            if not admin_db.get_admin_by_token(a_tok):
                redirect(self, "/admin/login"); return
            try:
                admin_db.add_restaurant(form.get("name",""),form.get("city","Manila"),
                    form.get("cuisine","Filipino"),form.get("price","PHP 200-400"),
                    form.get("rating","4.0"),form.get("hours","10AM-10PM"))
                send_html(self, admin_panel.restaurants_page(msg="Restaurant added successfully!"))
            except Exception as e:
                send_html(self, admin_panel.restaurants_page(error=str(e)))
        else:
            self.send_error(404)

    def log_message(self, *a): pass

if __name__ == "__main__":
    print("="*50)
    print("  ATLAS - Luzon Travel Companion")
    print("="*50)
    print(f"\n  Site:  http://localhost:{PORT}")
    print(f"  Admin: http://localhost:{PORT}/admin")
    print(f"\n  Default admin: admin / admin123")
    print("  Ctrl+C to stop\n")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), ATLASHandler) as s:
        try:
            s.serve_forever()
        except KeyboardInterrupt:
            print("\n  Goodbye!")
