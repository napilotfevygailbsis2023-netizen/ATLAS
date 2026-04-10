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
    "/profile.py":     lambda p, u: profile_page.render(user=u, msg=p.get("msg",""), err=p.get("err","")),
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

            # Compute section ONCE at the top so Python 3.14 doesn't treat it
            # as unbound when re.match() references it below.
            _sec = path.replace("/admin/","").replace("/admin","") or "dashboard"

            # ── Action routes (delete / approve / reject) ──
            import re as _re

            m = _re.match(r"^guides/delete/(\d+)$", _sec)
            if m:
                admin_db.delete_guide(int(m.group(1)))
                redirect(self, "/admin/guides?msg=Guide+deleted"); return

            m = _re.match(r"^guides/doc-approve/(\d+)$", _sec)
            if m:
                guide_db.set_doc_status(int(m.group(1)), "approved")
                redirect(self, "/admin/guides?tab=docs&msg=Approved"); return

            m = _re.match(r"^guides/doc-reject/(\d+)$", _sec)
            if m:
                guide_db.set_doc_status(int(m.group(1)), "rejected")
                redirect(self, "/admin/guides?tab=docs&msg=Rejected"); return

            m = _re.match(r"^tourists/delete/(\d+)$", _sec)
            if m:
                admin_db.delete_tourist(int(m.group(1)))
                redirect(self, "/admin/tourists?msg=Tourist+deleted"); return

            m = _re.match(r"^tourists/suspend/(\d+)$", _sec)
            if m:
                admin_db.set_tourist_status(int(m.group(1)), "suspended")
                redirect(self, "/admin/tourists"); return

            m = _re.match(r"^tourists/activate/(\d+)$", _sec)
            if m:
                admin_db.set_tourist_status(int(m.group(1)), "active")
                redirect(self, "/admin/tourists"); return

            m = _re.match(r"^tourists/archive/(\d+)$", _sec)
            if m:
                admin_db.set_tourist_status(int(m.group(1)), "archived")
                redirect(self, "/admin/tourists"); return

            m = _re.match(r"^spots/delete/(\d+)$", _sec)
            if m:
                admin_db.delete_spot(int(m.group(1)))
                redirect(self, "/admin/spots"); return

            m = _re.match(r"^restaurants/delete/(\d+)$", _sec)
            if m:
                admin_db.delete_restaurant(int(m.group(1)))
                redirect(self, "/admin/restaurants"); return

            m = _re.match(r"^flights/delete/(\d+)$", _sec)
            if m:
                admin_db.delete_flight(int(m.group(1)))
                redirect(self, "/admin/flights"); return

            m = _re.match(r"^transport/delete/(\d+)$", _sec)
            if m:
                admin_db.delete_transport(int(m.group(1)))
                redirect(self, "/admin/transport"); return

            # ── Page renders ──
            tab = params.get("tab", "registered")
            html_out = {
                "dashboard":   lambda: admin_panel.dashboard(admin),
                "tourists":    lambda: admin_panel.tourists_page(admin, msg=params.get("msg","")),
                "spots":       lambda: admin_panel.spots_page(admin, page=int(params.get("page",1))),
                "restaurants": lambda: admin_panel.restaurants_page(admin, page=int(params.get("page",1))),
                "guides":      lambda: admin_panel.guides_page(admin, page=int(params.get("page",1)), tab=tab, msg=params.get("msg","")),
                "transport":   lambda: admin_panel.transport_page(admin, page=int(params.get("page",1))),
                "flights":     lambda: admin_panel.flights_page(admin),
                "profile":     lambda: admin_panel.profile_page(admin),
            }.get(_sec, lambda: admin_panel.dashboard(admin))()
            send_html(self, html_out); return

        # ── Login / Signup GET routes ─────────────────────────────────────────
        if path == "/login.py":
            import login as login_page
            send_html(self, login_page.render(
                error=params.get("error",""),
                success=params.get("success","")
            )); return
        if path == "/login/password":
            import login as login_page
            email = params.get("email","").strip().lower()
            if not email:
                redirect(self, "/login.py"); return
            send_html(self, login_page.render_login_password(email,
                error=params.get("error",""))); return
        if path == "/signup/password":
            import login as login_page
            email = params.get("email","").strip().lower()
            if not email:
                redirect(self, "/login.py"); return
            send_html(self, login_page.render_signup_password(email,
                error=params.get("error",""))); return
        if path == "/signup/verify":
            import login as login_page
            email = params.get("email","").strip().lower()
            if not email:
                redirect(self, "/login.py"); return
            send_html(self, login_page.render_verify_email(email,
                error=params.get("error",""))); return

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

        # Read raw bytes — keep for multipart; decode for urlencoded
        raw_body = self.rfile.read(length)
        if "multipart/form-data" in content_type:
            body = raw_body.decode("latin-1")  # preserve bytes via latin-1
            form = {}  # will be parsed per-route via cgi.FieldStorage
        else:
            body = raw_body.decode("utf-8", errors="replace")
            form = dict(urllib.parse.parse_qsl(body))

        _sess_tok = (get_token(cookie, "atlas_token") or
                     get_token(cookie, "atlas_admin") or
                     get_token(cookie, "atlas_guide") or "")
        _csrf_exempt = {"/login.py", "/login/email", "/login/2fa",
                        "/signup/password", "/signup/verify", "/signup/resend",
                        "/verify", "/admin/login", "/guide/login",
                        "/profile/photo", "/auth/google/complete"}

        if path not in _csrf_exempt and not _csrf_ok(form, _sess_tok):
            self.send_error(403, "Invalid or missing CSRF token"); return

        if path == "/login.py":
            import login as login_page, urllib.parse as _up
            email    = form.get("email","").strip().lower()
            password = form.get("password","").strip()
            if not email or not password:
                redirect(self, "/login.py"); return
            result, tok, usr = db.login_user(email, password)
            if result == "suspended":
                redirect(self, "/login/password?email=" + _up.quote(email) +
                         "&error=Your+account+has+been+suspended"); return
            if not result:
                redirect(self, "/login/password?email=" + _up.quote(email) +
                         "&error=Incorrect+password.+Please+try+again."); return
            # 2FA check
            if usr.get("totp_enabled") and usr.get("totp_secret"):
                import login as login_page
                send_html(self, login_page.render_2fa(email)); return
            redirect(self, "/", f"atlas_token={tok}; Path=/; Max-Age=86400")

        # ── New signup flow POST routes ───────────────────────────────────────
        elif path == "/login/email":
            import urllib.parse as _up
            email = form.get("email","").strip().lower()
            if not email or "@" not in email:
                redirect(self, "/login.py?error=Please+enter+a+valid+email+address"); return
            existing = db.get_user_by_email(email)
            if existing:
                redirect(self, "/login/password?email=" + _up.quote(email)); return
            else:
                redirect(self, "/signup/password?email=" + _up.quote(email)); return

        elif path == "/signup/password":
            import login as login_page, urllib.parse as _up
            email = form.get("email","").strip().lower()
            pw    = form.get("password","").strip()
            if not email:
                redirect(self, "/login.py"); return
            # Server-side password validation (mirrors client-side rules)
            if (len(pw) < 12
                    or not any(c.isupper() for c in pw)
                    or not any(c.isdigit() for c in pw)):
                redirect(self, "/signup/password?email=" + _up.quote(email) +
                         "&error=Password+must+be+12%2B+chars+with+uppercase+and+a+number"); return
            # Store pending and send code
            code = db.store_signup_pending(email, pw)
            # ── Replace the print below with your email-sending call ──────────
            print(f"[ATLAS SIGNUP CODE] {email} → {code}")
            # ─────────────────────────────────────────────────────────────────
            redirect(self, "/signup/verify?email=" + _up.quote(email)); return

        elif path == "/signup/verify":
            import urllib.parse as _up
            email = form.get("email","").strip().lower()
            code  = form.get("code","").strip()
            ok, tok, msg = db.activate_signup(email, code)
            if ok:
                redirect(self, "/profile.py",
                         f"atlas_token={tok}; Path=/; Max-Age=86400"); return
            redirect(self, "/signup/verify?email=" + _up.quote(email) +
                     "&error=" + _up.quote(msg)); return

        elif path == "/signup/resend":
            import random, urllib.parse as _up
            email = form.get("email","").strip().lower()
            conn_r = db.get_conn(); cur_r = conn_r.cursor(dictionary=True)
            cur_r.execute("SELECT password FROM pending_users WHERE email=%s", (email,))
            row_r = cur_r.fetchone(); cur_r.close(); conn_r.close()
            if row_r:
                new_code = str(random.randint(100000, 999999))
                conn_u = db.get_conn(); cur_u = conn_u.cursor()
                cur_u.execute("UPDATE pending_users SET code=%s WHERE email=%s", (new_code, email))
                conn_u.commit(); cur_u.close(); conn_u.close()
                # ── Replace print with your email-sending call ───────────────
                print(f"[ATLAS RESEND CODE] {email} → {new_code}")
                # ─────────────────────────────────────────────────────────────
            redirect(self, "/signup/verify?email=" + _up.quote(email)); return

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
            import re as _re2, json as _json
            m = _re2.match(r"^/admin/guides/ai-review/(\d+)$", path)
            if m:
                gid = int(m.group(1))
                try:
                    g = guide_db.get_guide_by_id(gid)
                    doc_url = (g or {}).get("doc_url","")
                    if not doc_url:
                        raise ValueError("No document uploaded for this guide.")
                    import urllib.request as _ur
                    req = _ur.Request(
                        "https://api.anthropic.com/v1/messages",
                        data=_json.dumps({
                            "model": "claude-sonnet-4-6",
                            "max_tokens": 512,
                            "messages": [{"role":"user","content":[{"type":"text",
                                "text": f"Analyze this tour guide license/document URL: {doc_url}\nExtract: name, license_number, expiry, doc_type. Flag if suspicious. Reply ONLY in JSON: {{\"name\":\"\",\"license_number\":\"\",\"expiry\":\"\",\"doc_type\":\"\",\"suspicious\":false,\"notes\":\"\"}}"}]}]
                        }).encode(),
                        headers={"Content-Type":"application/json","anthropic-version":"2023-06-01"}
                    )
                    with _ur.urlopen(req, timeout=20) as r:
                        data = _json.loads(r.read())
                    raw = data.get("content",[{}])[0].get("text","{}").strip()
                    raw = _re2.sub(r"```json|```","",raw).strip()
                    result = _json.loads(raw)
                    try: guide_db.save_doc_ai_notes(gid, result.get("notes",""))
                    except: pass
                except Exception as ex:
                    result = {"error": str(ex)}
                resp_b = _json.dumps(result).encode()
                self.send_response(200)
                self.send_header("Content-Type","application/json")
                self.send_header("Content-Length", str(len(resp_b)))
                self.end_headers()
                self.wfile.write(resp_b)
                return
            self.send_error(404)

        elif path == "/profile/photo":
            # ── Upload profile photo (Python 3.14-compatible, no cgi module) ──
            if not user:
                redirect(self, "/login.py"); return
            import os, uuid as _uuid, re as _re

            if "multipart/form-data" not in content_type:
                redirect(self, "/profile.py?err=bad+request"); return

            # Extract boundary — may be quoted or unquoted
            boundary_match = _re.search(r'boundary=[""]?([^""\s;]+)[""]?', content_type)
            if not boundary_match:
                redirect(self, "/profile.py?err=Missing+multipart+boundary"); return
            boundary = boundary_match.group(1).encode("latin-1")

            # raw_body is always bytes from do_POST
            body_bytes = raw_body if isinstance(raw_body, bytes) else raw_body

            filename   = None
            file_bytes = None

            # Split body on --boundary (browsers always use \r\n)
            delimiter = b"--" + boundary
            parts = body_bytes.split(delimiter)

            for part in parts:
                # Skip preamble, epilogue marker (--)
                stripped = part.strip(b"\r\n")
                if not stripped or stripped == b"--":
                    continue

                # Normalize: remove leading \r\n
                if part.startswith(b"\r\n"):
                    part = part[2:]
                elif part.startswith(b"\n"):
                    part = part[1:]

                # Find end of headers: \r\n\r\n or \n\n
                sep = b"\r\n\r\n" if b"\r\n\r\n" in part else b"\n\n"
                if sep not in part:
                    continue

                headers_raw, _, part_body = part.partition(sep)
                headers_text = headers_raw.decode("latin-1", errors="replace")

                # Must be the photo_file field
                if 'name="photo_file"' not in headers_text and "name='photo_file'" not in headers_text:
                    continue

                # Extract filename
                fname_match = _re.search(r'filename=["\']([^"\']+)["\']', headers_text, _re.IGNORECASE)
                if not fname_match:
                    continue

                filename = fname_match.group(1)

                # Strip trailing \r\n or -- that belongs to the next boundary
                if part_body.endswith(b"\r\n"):
                    part_body = part_body[:-2]
                elif part_body.endswith(b"\n"):
                    part_body = part_body[:-1]

                file_bytes = part_body
                break

            if not filename or not file_bytes:
                redirect(self, "/profile.py?err=No+file+received+-+please+select+a+file+and+try+again"); return

            ext = os.path.splitext(filename)[-1].lower().lstrip(".")

            ALLOWED_EXT = {"jpg", "jpeg", "png", "webp"}
            MAX_SIZE    = 3 * 1024 * 1024  # 3 MB

            if ext not in ALLOWED_EXT:
                redirect(self, "/profile.py?err=Only+JPG%2C+PNG+or+WEBP+allowed"); return
            if len(file_bytes) > MAX_SIZE:
                redirect(self, "/profile.py?err=File+too+large+%28max+3+MB%29"); return
            if len(file_bytes) == 0:
                redirect(self, "/profile.py?err=Empty+file"); return

            uploads_dir = os.path.join(BASE, "uploads")
            os.makedirs(uploads_dir, exist_ok=True)
            safe_name   = f"user_{user['id']}_{_uuid.uuid4().hex[:8]}.{ext}"
            save_path   = os.path.join(uploads_dir, safe_name)
            with open(save_path, "wb") as fh:
                fh.write(file_bytes)

            db.update_photo_url(user["id"], f"/uploads/{safe_name}")
            redirect(self, "/profile.py?msg=Photo+updated+successfully"); return

        elif path == "/profile/update":
            # ── Update email or change password ──────────────────────────────
            if not user:
                redirect(self, "/login.py"); return
            action = form.get("action", "")
            if action == "update_profile":
                new_email = form.get("email", "").strip().lower()
                if not new_email or "@" not in new_email:
                    send_html(self, profile_page.render(user=user, err="Please enter a valid email address."))
                    return
                db.update_profile(user["id"], new_email)
                # Refresh user from DB so the page shows updated data
                user = db.get_user_by_token(token)
                send_html(self, profile_page.render(user=user, msg="Profile updated successfully."))
            elif action == "change_password":
                old_pw  = form.get("old_pw",  "").strip()
                new_pw  = form.get("new_pw",  "").strip()
                new_pw2 = form.get("new_pw2", "").strip()
                if not old_pw or not new_pw:
                    send_html(self, profile_page.render(user=user, err="Please fill in all password fields."))
                    return
                if new_pw != new_pw2:
                    send_html(self, profile_page.render(user=user, err="New passwords do not match."))
                    return
                ok, msg = db.change_password(user["id"], old_pw, new_pw)
                if ok:
                    send_html(self, profile_page.render(user=user, msg=msg))
                else:
                    send_html(self, profile_page.render(user=user, err=msg))
            else:
                redirect(self, "/profile.py")

        elif path == "/auth/google/complete":
            # ── New Google user completes registration (sets name + password) ──
            import login as login_page
            g_email = form.get("email", "").strip().lower()
            fname   = form.get("fname", "").strip()
            lname   = form.get("lname", "").strip()
            pw      = form.get("password",  "").strip()
            pw2     = form.get("password2", "").strip()

            if not g_email or not fname or not pw:
                send_html(self, login_page.render_register_complete(
                    g_email, error="Please fill in all fields.")); return
            if pw != pw2:
                send_html(self, login_page.render_register_complete(
                    g_email, error="Passwords do not match.")); return
            if len(pw) < 8:
                send_html(self, login_page.render_register_complete(
                    g_email, error="Password must be at least 8 characters.")); return

            target_user = db.get_user_by_email(g_email)
            if not target_user:
                send_html(self, login_page.render_register_complete(
                    g_email, error="Account not found. Please sign in with Google again.")); return

            db.set_user_name_and_password(target_user["id"], fname, lname, pw)
            # Issue a fresh session token
            new_token = secrets.token_hex(32)
            import mysql.connector as _mc
            _conn = db.get_conn(); _cur = _conn.cursor()
            _cur.execute("INSERT INTO sessions (token,user_id) VALUES (%s,%s)", (new_token, target_user["id"]))
            _conn.commit(); _cur.close(); _conn.close()
            redirect(self, "/profile.py",
                     f"atlas_token={new_token}; Path=/; Max-Age=86400"); return



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