import http.server, socketserver, urllib.parse, os, sys, re, email, hmac, hashlib, secrets
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import index, flights, weather, attractions, restaurants, guides, transport, itinerary, about
import logout, db
import admin_login, admin_panel, admin_db
import guide_portal
import profile as profile_page, guide_db
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_CLIENT_ID     = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
PORT = int(os.environ.get("PORT", 5000))
BASE = os.path.dirname(os.path.abspath(__file__))
CSS  = os.path.join(BASE, "css", "styles.css")

GOOGLE_REDIRECT_URI  = "http://localhost:5000/auth/google/callback"

_CSRF_SECRET = os.environ.get("CSRF_SECRET", os.urandom(32).hex())

def _csrf_token(session_token: str) -> str:
    return hmac.new(_CSRF_SECRET.encode(), session_token.encode(), hashlib.sha256).hexdigest()

def _csrf_input(session_token: str) -> str:
    if not session_token:
        return ""
    return f'<input type="hidden" name="csrf_token" value="{_csrf_token(session_token)}"/>'

def _csrf_ok(form: dict, session_token: str) -> bool:
    if not session_token:
        return True
    submitted = form.get("csrf_token", "")
    return hmac.compare_digest(submitted, _csrf_token(session_token))

ROUTES = {
    "/about.py":       lambda p, u: about.render(u),
    "/":               lambda p, u: index.render(u),
    "/index.py":       lambda p, u: index.render(u),
    "/flights.py":     lambda p, u: flights.render(p, u),
    "/weather.py":     lambda p, u: weather.render(p.get("location","Manila"), u),
    "/attractions.py": lambda p, u: attractions.render(p.get("city","All"), p.get("cat","All"), p.get("kw",""), u),
    "/restaurants.py": lambda p, u: restaurants.render(p.get("city","All"), p.get("kw",""), p.get("type","All"), u),
    "/guides.py":      lambda p, u: guides.render(p.get("city","All"), p.get("lang","All"), u, booked=bool(p.get("booked",""))),
    "/transport.py":   lambda p, u: transport.render(p.get("type","All"), p.get("from","All"), p.get("search",""), u),
    "/itinerary.py":   lambda p, u: itinerary.render(p.get("dest","Manila"), p.get("days",None), u),
    "/profile.py":     lambda p, u: profile_page.render(user=u),
}

def get_token(cookie_header, name="atlas_token"):
    if not cookie_header: return None
    for part in cookie_header.split(";"):
        part = part.strip()
        if part.startswith(f"{name}="):
            return part[len(f"{name}="):]
    return None

def _inject_csrf(html_out, session_token):
    if not session_token or "<head>" not in html_out:
        return html_out
    tok = _csrf_token(session_token)
    return html_out.replace("<head>", f'<head><script>var ATLAS_CSRF="{tok}";</script>', 1)

def redirect(handler, location, cookie=None):
    handler.send_response(302)
    handler.send_header("Location", location)
    if cookie: handler.send_header("Set-Cookie", cookie)
    handler.end_headers()

def send_html(handler, html, cookie=None):
    b = html.encode("utf-8")
    handler.send_response(200)
    handler.send_header("Content-Type","text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(b)))
    if cookie: handler.send_header("Set-Cookie", cookie)
    handler.end_headers()
    try:
        handler.wfile.write(b)
    except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
        pass

class ATLASHandler(http.server.SimpleHTTPRequestHandler):
    def handle_error(self, request, client_address):
        import sys
        exc = sys.exc_info()[1]
        if isinstance(exc, (ConnectionAbortedError, ConnectionResetError, BrokenPipeError)):
            return
        super().handle_error(request, client_address)

    def get_admin(self):
        a_tok = get_token(self.headers.get("Cookie",""), "atlas_admin")
        return admin_db.get_admin_by_token(a_tok), a_tok

    def require_admin(self):
        admin, tok = self.get_admin()
        if not admin:
            redirect(self, "/admin/login")
            return None, None
        return admin, tok

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = dict(urllib.parse.parse_qsl(parsed.query))
        path   = parsed.path
        cookie = self.headers.get("Cookie","")
        token  = get_token(cookie, "atlas_token")
        user   = db.get_user_by_token(token)

        if path == "/css/styles.css":
            with open(CSS,"rb") as f: css = f.read()
            self.send_response(200)
            self.send_header("Content-Type","text/css; charset=utf-8")
            self.send_header("Content-Length", str(len(css)))
            self.end_headers()
            self.wfile.write(css)
            return

        if path == "/ATLAS_LOGO.jpg":
            logo_path = os.path.join(BASE, "ATLAS_LOGO.jpg")
            if os.path.isfile(logo_path):
                with open(logo_path,"rb") as f: img = f.read()
                self.send_response(200)
                self.send_header("Content-Type","image/jpeg")
                self.send_header("Content-Length", str(len(img)))
                self.end_headers()
                self.wfile.write(img)
            else:
                self.send_error(404)
            return

        if path.startswith("/uploads/"):
            fname = path[len("/uploads/"):]
            fpath = os.path.join(BASE, "uploads", fname)
            if os.path.isfile(fpath):
                ext = os.path.splitext(fname)[-1].lower().lstrip(".")
                mime = {"jpg":"image/jpeg","jpeg":"image/jpeg","png":"image/png","gif":"image/gif","webp":"image/webp"}.get(ext,"application/octet-stream")
                with open(fpath,"rb") as f: data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_error(404)
            return

        # ── Google OAuth: Step 1 — redirect user to Google ──
        if path == "/auth/google":
            if not GOOGLE_CLIENT_ID:
                send_html(self, "<h2>Google OAuth not configured. Set GOOGLE_CLIENT_ID in .env</h2>")
                return
            import urllib.parse as _up
            scope = "openid email profile"
            # Pass 'next' via the OAuth 'state' param so it survives the round-trip to Google
            next_val   = params.get("next", "")
            login_hint = params.get("login_hint", "")
            oauth_params = {
                "client_id":     GOOGLE_CLIENT_ID,
                "redirect_uri":  GOOGLE_REDIRECT_URI,
                "response_type": "code",
                "scope":         scope,
                "access_type":   "offline",
                "prompt":        "select_account consent",
                "state":         next_val,
            }
            if login_hint:
                oauth_params["login_hint"] = login_hint
            auth_url = (
                "https://accounts.google.com/o/oauth2/v2/auth?"
                + _up.urlencode(oauth_params)
            )
            redirect(self, auth_url)
            return

        # ── Google OAuth: Step 2 — handle callback from Google ──
        if path == "/auth/google/callback":
            import urllib.parse as _up, urllib.request as _ur, json as _json
            code  = params.get("code", "")
            error = params.get("error", "")
            if error or not code:
                redirect(self, "/")
                return
            if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
                redirect(self, "/")
                return
            # Exchange code for tokens
            try:
                token_data = _up.urlencode({
                    "code":          code,
                    "client_id":     GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "redirect_uri":  GOOGLE_REDIRECT_URI,
                    "grant_type":    "authorization_code",
                }).encode()
                req = _ur.Request("https://oauth2.googleapis.com/token", data=token_data,
                                  headers={"Content-Type": "application/x-www-form-urlencoded"})
                with _ur.urlopen(req, timeout=8) as r:
                    token_resp = _json.loads(r.read())
            except Exception as ex:
                redirect(self, "/")
                return

            access_token = token_resp.get("access_token", "")
            if not access_token:
                redirect(self, "/")
                return

            # Fetch user info from Google
            try:
                req2 = _ur.Request("https://www.googleapis.com/oauth2/v3/userinfo",
                                   headers={"Authorization": f"Bearer {access_token}"})
                with _ur.urlopen(req2, timeout=8) as r:
                    guser = _json.loads(r.read())
            except Exception as ex:
                redirect(self, "/")
                return

            g_email = guser.get("email", "").lower().strip()
            g_fname = guser.get("given_name", guser.get("name", "User"))
            g_lname = guser.get("family_name", "")
            g_photo = guser.get("picture", "")

            if not g_email:
                redirect(self, "/")
                return

            # 'state' carries the 'next' value we set in Step 1
            next_page = params.get("state", "")

            if next_page == "guide":
                import urllib.parse as _enc
                guide = guide_db.get_guide_by_email(g_email)
                if not guide:
                    # Auto-create a guide account from Google profile
                    ok, msg2 = guide_db.register_guide(
                        g_fname, g_lname, g_email, secrets.token_hex(16),
                        "", "Manila"
                    )
                    guide = guide_db.get_guide_by_email(g_email) if ok else None
                if not guide:
                    msg = _enc.quote("Could not create guide account. Please try registering manually.")
                    redirect(self, "/guide?error_msg=" + msg)
                    return
                if guide.get("status") == "suspended":
                    msg = _enc.quote("Your guide account has been suspended. Contact support.")
                    redirect(self, "/guide?error_msg=" + msg)
                    return
                is_new = guide.get("status") == "pending"
                g_sess_token = guide_db.create_guide_session(guide["id"])
                if g_sess_token:
                    dest = "/guide/dashboard?welcome=1" if is_new else "/guide/dashboard"
                    redirect(self, dest,
                             f"atlas_guide={g_sess_token}; Path=/; Max-Age=86400")
                else:
                    msg = _enc.quote("Session error. Please try again.")
                    redirect(self, "/guide?error_msg=" + msg)
            else:
                # Regular tourist login
                sess_token = db.login_or_create_google_user(g_email, g_fname, g_lname, g_photo)
                if sess_token:
                    redirect(self, "/", f"atlas_token={sess_token}; Path=/; Max-Age=86400")
                else:
                    redirect(self, "/")
            return

        if path == "/logout.py":
            if token:
                db.logout(token)
            redirect(self, "/", "atlas_token=; Path=/; Max-Age=0")
            return

        # ── Admin routes ──
        if path in ("/admin", "/admin/"):
            redirect(self, "/admin/login"); return
        if path == "/admin/login":
            send_html(self, admin_login.render()); return
        if path.startswith("/admin"):
            admin, tok = self.get_admin()
            if not admin:
                redirect(self, "/admin/login"); return
            section = path.replace("/admin/","").replace("/admin","") or "dashboard"
            html_out = {
                "dashboard": lambda: admin_panel.dashboard(admin),
                "tourists":  lambda: admin_panel.tourists_page(admin),
                "spots":     lambda: admin_panel.spots_page(admin, page=int(params.get("page",1))),
                "restaurants": lambda: admin_panel.restaurants_page(admin, page=int(params.get("page",1))),
                "guides":    lambda: admin_panel.guides_page(admin, page=int(params.get("page",1))),
                "transport": lambda: admin_panel.transport_page(admin, page=int(params.get("page",1))),
                "flights":   lambda: admin_panel.flights_page(admin),
                "profile":   lambda: admin_panel.profile_page(admin),
            }.get(section, lambda: admin_panel.dashboard(admin))()
            send_html(self, html_out); return

        # ── Guide portal routes ──
        if path == "/guide/check-email":
            import json as _json
            email = params.get("email","").strip().lower()
            exists = guide_db.get_guide_by_email(email) is not None
            resp = _json.dumps({"exists": exists}).encode()
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.send_header("Content-Length", str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
            return

        if path in ("/guide", "/guide/"):
            send_html(self, guide_portal.render_login(
                error=params.get("error_msg", ""),
                success=params.get("success", "")
            )); return
        if path == "/guide/logout":
            g_tok = get_token(cookie, "atlas_guide")
            if g_tok:
                guide_db.logout_guide(g_tok)
            redirect(self, "/guide", "atlas_guide=; Path=/; Max-Age=0"); return
        if path == "/guide/verify":
            email = params.get("email","")
            send_html(self, guide_portal.render_verify_guide(email)); return
        if path.startswith("/guide/"):
            g_tok = get_token(cookie, "atlas_guide")
            guide = guide_db.get_guide_by_token(g_tok)
            if not guide:
                redirect(self, "/guide"); return
            section = path.replace("/guide/","").replace("/guide","") or "dashboard"
            html_out = {
                "dashboard":    lambda: guide_portal.render_dashboard(guide),
                "packages":     lambda: guide_portal.render_packages(guide),
                "bookings":     lambda: guide_portal.render_bookings(guide, params.get("status","all")),
                "availability": lambda: guide_portal.render_availability(guide),
                "ratings":      lambda: guide_portal.render_ratings(guide),
                "profile":      lambda: guide_portal.render_profile(guide),
            }.get(section, lambda: guide_portal.render_dashboard(guide))()
            send_html(self, html_out); return

        handler = ROUTES.get(path)
        if handler is None:
            self.send_error(404, "Page not found"); return
        page_csrf = _csrf_token(token) if token else ""
        html_out = handler(params, user)
        if page_csrf and "<head>" in html_out:
            html_out = html_out.replace(
                "<head>",
                f'<head><script>var ATLAS_CSRF="{page_csrf}";</script>',
                1
            )
        send_html(self, html_out)

    def do_POST(self):
        path   = urllib.parse.urlparse(self.path).path
        cookie = self.headers.get("Cookie","")
        token  = get_token(cookie, "atlas_token")
        user   = db.get_user_by_token(token)
        content_type = self.headers.get("Content-Type","")
        length = int(self.headers.get("Content-Length",0))

        body = self.rfile.read(length).decode("utf-8")
        form = dict(urllib.parse.parse_qsl(body))

        _sess_tok = (get_token(cookie, "atlas_token") or
                     get_token(cookie, "atlas_admin") or
                     get_token(cookie, "atlas_guide") or "")
        _csrf_exempt = {"/login.py", "/verify", "/admin/login", "/guide/login"}

        if path not in _csrf_exempt and not _csrf_ok(form, _sess_tok):
            self.send_error(403, "Invalid or missing CSRF token"); return

        if path == "/login.py":
            email    = form.get("email","").strip().lower()
            password = form.get("password","").strip()
            if not email or not password:
                redirect(self, "/"); return
            result, token, user = db.login_user(email, password)
            if not result or result == "suspended":
                redirect(self, "/"); return
            redirect(self, "/", f"atlas_token={token}; Path=/; Max-Age=86400")

        # ── Admin POST ──
        elif path == "/admin/login":
            result = admin_login.handle_post(form)
            if result.get("token"):
                redirect(self, "/admin/dashboard", f"atlas_admin={result['token']}; Path=/; Max-Age=86400")
            else:
                send_html(self, admin_login.render(error=result.get("error","")))

        # ── Guide POST ──
        elif path == "/guide/login":
            result = guide_portal.handle_login(form) if hasattr(guide_portal, 'handle_login') else {}
            if result.get("token"):
                dest = "/guide/dashboard?welcome=1" if result.get("new") else "/guide/dashboard"
                redirect(self, dest, f"atlas_guide={result['token']}; Path=/; Max-Age=86400")
            else:
                send_html(self, guide_portal.render_login(error=result.get("error","")))

        elif path.startswith("/guide/"):
            g_tok = get_token(cookie, "atlas_guide")
            guide = guide_db.get_guide_by_token(g_tok)
            if not guide:
                redirect(self, "/guide"); return
            section = path.replace("/guide/","")
            if section == "dashboard":
                send_html(self, guide_portal.render_dashboard(guide))
            elif section == "packages":
                send_html(self, guide_portal.render_packages(guide))
            elif section == "bookings":
                send_html(self, guide_portal.render_bookings(guide))
            elif section == "availability":
                send_html(self, guide_portal.render_availability(guide))
            elif section == "profile":
                action = form.get("action","")
                if action == "update_profile":
                    guide_db.update_guide_profile(guide["id"], {
                        "phone":        form.get("phone","").strip(),
                        "city":         form.get("city","Manila").strip(),
                        "languages":    form.get("languages","EN, FIL").strip(),
                        "speciality":   form.get("speciality","").strip(),
                        "bio":          form.get("bio","").strip(),
                        "rate":         form.get("rate","P1,500/day").strip(),
                        "availability": form.get("availability","Mon-Sun").strip(),
                    })
                    guide = guide_db.get_guide_by_token(g_tok)
                    send_html(self, guide_portal.render_profile(guide, msg="Profile updated successfully!"))
                elif action == "change_password":
                    new_pw  = form.get("new_pw","").strip()
                    new_pw2 = form.get("new_pw2","").strip()
                    if not new_pw or len(new_pw) < 6:
                        send_html(self, guide_portal.render_profile(guide, err="Password must be at least 6 characters."))
                    elif new_pw != new_pw2:
                        send_html(self, guide_portal.render_profile(guide, err="Passwords do not match."))
                    else:
                        guide_db.change_guide_password(guide["id"], new_pw)
                        send_html(self, guide_portal.render_profile(guide, msg="Password changed successfully!"))
                else:
                    send_html(self, guide_portal.render_profile(guide))
            else:
                self.send_error(404)

        # ── Tourist books a guide ──
        elif path == "/book-guide":
            if not user:
                redirect(self, "/guides.py"); return
            guide_id = int(form.get("guide_id", 0) or 0)
            if not guide_id:
                redirect(self, "/guides.py"); return
            guide_db.add_booking({
                "guide_id":      guide_id,
                "tourist_name":  form.get("tourist_name",  "").strip(),
                "tourist_email": user.get("email", ""),
                "tourist_phone": form.get("tourist_phone", "").strip(),
                "package_id":    0,
                "package_title": form.get("package_title", "Custom Tour").strip(),
                "tour_date":     form.get("tour_date",     "").strip(),
                "pax":           int(form.get("pax", 1) or 1),
                "notes":         form.get("notes",         "").strip(),
            })
            redirect(self, "/guides.py?booked=1"); return

        elif path.startswith("/admin/"):
            admin, tok = self.get_admin()
            if not admin:
                redirect(self, "/admin/login"); return
            self.send_error(404)

        else:
            self.send_error(404)

    def log_message(self, *a): pass

if __name__ == "__main__":
    print("="*50)
    print("  ATLAS - Luzon Travel Companion")
    print("="*50)
    print(f"\n  Site:  http://localhost:{PORT}")
    print(f"  Admin: http://localhost:{PORT}/admin")
    print(f"  Guide: http://localhost:{PORT}/guide")
    _admin_pw = os.environ.get("ATLAS_ADMIN_PASSWORD", "admin123")
    print(f"\n  Admin login: admin / {_admin_pw}")
    print("  Ctrl+C to stop\n")

    try:
        db.purge_expired_sessions()
        guide_db.purge_expired_guide_sessions()
    except Exception:
        pass

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), ATLASHandler) as s:
        try: s.serve_forever()
        except KeyboardInterrupt: print("\n  Goodbye!")