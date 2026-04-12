import http.server, socketserver, urllib.parse, os, sys, re, email, hmac, hashlib, secrets
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import login as login_page

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

        # ── Geocode proxy — avoids browser forbidden-header / CORS issues ──
        if path == "/api/transport/geocode":
            import json as _json, urllib.request as _ur, urllib.parse as _up

            def _json_resp_geo(handler, payload):
                b = _json.dumps(payload, ensure_ascii=False).encode("utf-8")
                handler.send_response(200)
                handler.send_header("Content-Type", "application/json; charset=utf-8")
                handler.send_header("Content-Length", str(len(b)))
                handler.send_header("Access-Control-Allow-Origin", "*")
                handler.end_headers()
                handler.wfile.write(b)

            place = params.get("place", "").strip()
            if not place:
                _json_resp_geo(self, {"ok": False, "error": "place required"})
            else:
                try:
                    import urllib.parse as _up2
                    q = place if "Philippines" in place else place + ", Philippines"
                    geo_url = "https://nominatim.openstreetmap.org/search?" + _up2.urlencode({
                        "q": q, "format": "json", "countrycodes": "ph", "limit": 1,
                    })
                    geo_req = _ur.Request(geo_url, headers={
                        "Accept": "application/json",
                        "User-Agent": "ATLAS-Transport/1.0",
                    })
                    with _ur.urlopen(geo_req, timeout=6) as r:
                        geo_data = _json.loads(r.read())
                    if not geo_data:
                        _json_resp_geo(self, {"ok": False, "error": f"Place not found: {place}"})
                    else:
                        _json_resp_geo(self, {"ok": True, "lat": float(geo_data[0]["lat"]), "lng": float(geo_data[0]["lon"])})
                except Exception as e:
                    _json_resp_geo(self, {"ok": False, "error": str(e)})
            return

        if path == "/api/transport/lookup":
            import json as _json, urllib.request as _ur, urllib.parse as _up, math as _math
            origin = params.get("origin", "").strip()
            dest   = params.get("dest",   "").strip()
            ors_key = os.environ.get("ORS_API_KEY", "")

            def _json_resp(handler, payload):
                b = _json.dumps(payload, ensure_ascii=False).encode("utf-8")
                handler.send_response(200)
                handler.send_header("Content-Type", "application/json; charset=utf-8")
                handler.send_header("Content-Length", str(len(b)))
                handler.send_header("Access-Control-Allow-Origin", "*")
                handler.end_headers()
                try:
                    handler.wfile.write(b)
                except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
                    pass  # Browser cancelled the request — harmless

            if not origin or not dest:
                _json_resp(self, {"ok": False, "error": "origin and dest required"}); return

            def _geocode(place):
                """Convert place name to [lon, lat]. Uses a local cache of PH cities first,
                then falls back to Nominatim so we don't burn rate-limit slots."""
                # Built-in coords for common Luzon cities — instant, no HTTP needed
                PH_COORDS = {
                    "manila":                       [120.9842, 14.5995],
                    "quezon city":                  [121.0437, 14.6760],
                    "baguio":                       [120.5960, 16.4023],
                    "baguio city":                  [120.5960, 16.4023],
                    "laoag":                        [120.5939, 18.1977],
                    "laoag city":                   [120.5939, 18.1977],
                    "vigan":                        [120.3869, 17.5747],
                    "vigan city":                   [120.3869, 17.5747],
                    "san fernando":                 [120.3169, 16.6159],
                    "san fernando, la union":       [120.3169, 16.6159],
                    "san fernando, pampanga":       [120.6894, 15.0285],
                    "dagupan":                      [120.3333, 16.0433],
                    "dagupan city":                 [120.3333, 16.0433],
                    "alaminos":                     [119.9814, 16.1554],
                    "alaminos, pangasinan":         [119.9814, 16.1554],
                    "alaminos city":                [119.9814, 16.1554],
                    "urdaneta":                     [120.5714, 15.9757],
                    "urdaneta city":                [120.5714, 15.9757],
                    "lingayen":                     [120.2333, 16.0167],
                    "olongapo":                     [120.2823, 14.8292],
                    "olongapo city":                [120.2823, 14.8292],
                    "subic":                        [120.2300, 14.8800],
                    "subic bay":                    [120.2300, 14.8800],
                    "angeles":                      [120.5900, 15.1430],
                    "angeles city":                 [120.5900, 15.1430],
                    "tarlac":                       [120.5960, 15.4755],
                    "tarlac city":                  [120.5960, 15.4755],
                    "tuguegarao":                   [121.7270, 17.6132],
                    "tuguegarao city":              [121.7270, 17.6132],
                    "cauayan":                      [121.7726, 16.9307],
                    "cauayan city":                 [121.7726, 16.9307],
                    "ilagan":                       [121.8883, 17.1488],
                    "ilagan city":                  [121.8883, 17.1488],
                    "santiago":                     [121.6494, 16.6882],
                    "santiago city":                [121.6494, 16.6882],
                    "cabanatuan":                   [120.9685, 15.4862],
                    "cabanatuan city":              [120.9685, 15.4862],
                    "palayan":                      [121.0833, 15.5500],
                    "palayan city":                 [121.0833, 15.5500],
                    "baler":                        [121.5619, 15.7580],
                    "baler, aurora":                [121.5619, 15.7580],
                    "bayombong":                    [121.1497, 16.4829],
                    "bayombong, nueva vizcaya":     [121.1497, 16.4829],
                    "sagada":                       [120.9000, 17.0833],
                    "banaue":                       [121.0597, 16.9186],
                    "tabuk":                        [121.4447, 17.4189],
                    "tabuk, kalinga":               [121.4447, 17.4189],
                    "malolos":                      [120.8136, 14.8527],
                    "malolos city":                 [120.8136, 14.8527],
                    "meycauayan":                   [120.9600, 14.7368],
                    "meycauayan city":              [120.9600, 14.7368],
                    "marilao":                      [120.9476, 14.7583],
                    "balanga":                      [120.5373, 14.6761],
                    "balanga city":                 [120.5373, 14.6761],
                    "batangas":                     [121.0583, 13.7565],
                    "batangas city":                [121.0583, 13.7565],
                    "lucena":                       [121.6171, 13.9373],
                    "lucena city":                  [121.6171, 13.9373],
                    "lipa":                         [121.1636, 13.9411],
                    "lipa city":                    [121.1636, 13.9411],
                    "tanauan":                      [121.1319, 14.0862],
                    "tanauan city":                 [121.1319, 14.0862],
                    "antipolo":                     [121.1761, 14.5862],
                    "antipolo city":                [121.1761, 14.5862],
                    "calamba":                      [121.1653, 14.2116],
                    "calamba, laguna":              [121.1653, 14.2116],
                    "calamba city":                 [121.1653, 14.2116],
                    "santa cruz":                   [121.4167, 14.2833],
                    "santa cruz, laguna":           [121.4167, 14.2833],
                    "san pablo":                    [121.3253, 14.0689],
                    "san pablo city":               [121.3253, 14.0689],
                    "santa rosa":                   [121.1113, 14.3121],
                    "santa rosa city":              [121.1113, 14.3121],
                    "binan":                        [121.0819, 14.3412],
                    "binan city":                   [121.0819, 14.3412],
                    "naga":                         [123.1936, 13.6192],
                    "naga city":                    [123.1936, 13.6192],
                    "legazpi":                      [123.7438, 13.1391],
                    "legazpi city":                 [123.7438, 13.1391],
                    "sorsogon":                     [123.9933, 12.9722],
                    "sorsogon city":                [123.9933, 12.9722],
                    "irosin":                       [124.0336, 12.7046],
                    "irosin, sorsogon":             [124.0336, 12.7046],
                    "masbate":                      [123.6214, 12.3701],
                    "masbate city":                 [123.6214, 12.3701],
                    "daet":                         [122.9831, 14.1122],
                    "daet, camarines norte":        [122.9831, 14.1122],
                    "tagaytay":                     [120.9621, 14.0956],
                    "tagaytay city":                [120.9621, 14.0956],
                    "puerto galera":                [120.9536, 13.5025],
                }
                key = place.strip().lower()
                if key in PH_COORDS:
                    return PH_COORDS[key]
                # Fallback: Nominatim (rate-limited — only reached for unknown cities)
                try:
                    import time as _time
                    q = place if "Philippines" in place else place + ", Philippines"
                    url = "https://nominatim.openstreetmap.org/search?" + _up.urlencode({
                        "q": q, "format": "json", "countrycodes": "ph", "limit": 1,
                    })
                    req = _ur.Request(url, headers={
                        "Accept": "application/json",
                        "User-Agent": "ATLAS-Transport/1.0 (travel-app)",
                    })
                    with _ur.urlopen(req, timeout=8) as r:
                        data = _json.loads(r.read())
                    if not data:
                        return None
                    return [float(data[0]["lon"]), float(data[0]["lat"])]
                except Exception:
                    return None

            def _haversine_km(lon1, lat1, lon2, lat2):
                """Straight-line distance in km between two coordinates."""
                R = 6371.0
                dlat = _math.radians(lat2 - lat1)
                dlon = _math.radians(lon2 - lon1)
                a = (_math.sin(dlat/2)**2
                     + _math.cos(_math.radians(lat1))
                     * _math.cos(_math.radians(lat2))
                     * _math.sin(dlon/2)**2)
                return R * 2 * _math.atan2(_math.sqrt(a), _math.sqrt(1 - a))

            def _fetch_route_ors(orig_coords, dest_coords, profile="driving-car"):
                """Try ORS for a real road-distance route (requires ORS_API_KEY)."""
                try:
                    body = _json.dumps({
                        "coordinates": [orig_coords, dest_coords],
                        "instructions": False,
                    }).encode("utf-8")
                    url = f"https://api.openrouteservice.org/v2/directions/{profile}"
                    req = _ur.Request(url, data=body, headers={
                        "Authorization": f"Bearer {ors_key}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    })
                    with _ur.urlopen(req, timeout=8) as r:
                        data = _json.loads(r.read())
                    routes = data.get("routes", [])
                    if not routes:
                        return None
                    dist_km = round(routes[0]["summary"]["distance"] / 1000, 1)
                    dur_min = int(routes[0]["summary"]["duration"] / 60)
                    return dist_km, dur_min
                except Exception:
                    return None

            def _fetch_route():
                try:
                    orig_coords = _geocode(origin)
                    dest_coords = _geocode(dest)
                    if not orig_coords or not dest_coords:
                        return None

                    dist_km, dur_min, source = None, None, "est."

                    # Try ORS first if API key is available
                    if ors_key:
                        ors_result = _fetch_route_ors(orig_coords, dest_coords)
                        if ors_result:
                            dist_km, dur_min = ors_result
                            source = "road"

                    # Free fallback: Haversine straight-line x 1.35 road-factor
                    if dist_km is None:
                        straight = _haversine_km(orig_coords[0], orig_coords[1],
                                                  dest_coords[0], dest_coords[1])
                        dist_km = round(straight * 1.35, 1)   # ~35% road-detour factor
                        dur_min = int((dist_km / 60) * 60)    # avg 60 km/h on PH highways
                        source = "est."

                    dur_text  = (f"{dur_min // 60}h {dur_min % 60}m"
                                 if dur_min >= 60 else f"{dur_min} min")
                    dist_text = f"{dist_km} km ({source})"
                    # PH bus/jeepney fare: PHP 13 base + PHP 1.80/km
                    fare_est  = round(13 + dist_km * 1.80)
                    return {
                        "duration": dur_text,
                        "distance": dist_text,
                        "fare":     f"PHP {fare_est}",
                        "type":     "Bus",
                    }
                except Exception:
                    return None

            result = _fetch_route()
            if result:
                _json_resp(self, {
                    "ok":             True,
                    "origin":         origin,
                    "destination":    dest,
                    "duration":       result["duration"],
                    "distance":       result["distance"],
                    "fare":           result["fare"],
                    "suggested_type": result["type"],
                })
            else:
                _json_resp(self, {"ok": False, "error": "Could not locate one or both places"})
            return

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
                redirect(self, "/admin/transport?tab=list&msg=Route+deleted"); return

            m = _re.match(r"^transport/archive/(\d+)$", _sec)
            if m:
                admin_db.archive_transport(int(m.group(1)))
                redirect(self, "/admin/transport?tab=list&msg=Route+archived"); return

            m = _re.match(r"^transport/restore/(\d+)$", _sec)
            if m:
                admin_db.restore_transport(int(m.group(1)))
                redirect(self, "/admin/transport?tab=archived&msg=Route+restored"); return

            # ── Page renders ──
            tab = params.get("tab", "registered")
            html_out = {
                "dashboard":   lambda: admin_panel.dashboard(admin),
                "tourists":    lambda: admin_panel.tourists_page(admin, msg=params.get("msg","")),
                "spots":       lambda: admin_panel.spots_page(admin, page=int(params.get("page",1))),
                "restaurants": lambda: admin_panel.restaurants_page(admin, page=int(params.get("page",1))),
                "guides":      lambda: admin_panel.guides_page(admin, page=int(params.get("page",1)), tab=tab, msg=params.get("msg","")),
                "transport":   lambda: admin_panel.transport_page(admin, page=int(params.get("page",1)), tab=params.get("tab","add"), csrf=_csrf_token(tok)),
                "flights":     lambda: admin_panel.flights_page(admin, dom_page=int(params.get("dom_page",1)), intl_page=int(params.get("intl_page",1))),
                "profile":     lambda: admin_panel.profile_page(admin, msg=params.get("msg",""), err=params.get("err",""), csrf=_csrf_token(tok)),
            }.get(_sec, lambda: admin_panel.dashboard(admin))()
            if tok and "<head>" in html_out:
                html_out = html_out.replace("<head>", f'<head><script>var ATLAS_CSRF="{_csrf_token(tok)}";</script>', 1)
            send_html(self, html_out); return

        # ── Login / Signup GET routes ─────────────────────────────────────────
        if path == "/login.py":
            send_html(self, login_page.render(
                error=params.get("error",""),
                success=params.get("success","")
            )); return
        if path == "/login/password":
            email = params.get("email","").strip().lower()
            if not email:
                redirect(self, "/login.py"); return
            send_html(self, login_page.render_login_password(email,
                error=params.get("error",""))); return
        if path == "/signup/password":
            email = params.get("email","").strip().lower()
            if not email:
                redirect(self, "/login.py"); return
            send_html(self, login_page.render_signup_password(email,
                error=params.get("error",""))); return
        if path == "/signup/verify":
            email = params.get("email","").strip().lower()
            if not email:
                redirect(self, "/login.py"); return
            send_html(self, login_page.render_verify_email(email,
                error=params.get("error",""))); return

        if path == "/login/2fa":
            email = params.get("email","").strip().lower()
            if not email:
                redirect(self, "/login.py"); return
            send_html(self, login_page.render_2fa(email,
                error=params.get("error",""))); return

        if path == "/setup-2fa":
            if not user:
                redirect(self, "/login.py"); return
            send_html(self, login_page.render_2fa_setup(user)); return
        if path == "/guide/setup-2fa":
            g_tok = get_token(cookie, "atlas_guide")
            guide = guide_db.get_guide_by_token(g_tok)
            if not guide:
                redirect(self, "/guide"); return
            send_html(self, guide_portal.render_2fa_setup(guide)); return

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
        if path == "/guide/2fa":
            email = params.get("email","").strip().lower()
            if not email:
                redirect(self, "/guide"); return
            send_html(self, guide_portal.render_guide_2fa(email,
                error=params.get("error",""))); return
        if path == "/login/2fa/resend":
            import urllib.parse as _up
            email = params.get("email","").strip().lower()
            usr_r = db.get_user_by_email(email)
            if usr_r and usr_r.get("totp_enabled"):
                otp_r = db.create_user_otp(usr_r["id"])
                from email_sender import send_otp_email
                send_otp_email(email, otp_r)
            redirect(self, "/login/2fa?email=" + _up.quote(email)); return
        if path == "/guide/2fa/resend":
            import urllib.parse as _up
            email = params.get("email","").strip().lower()
            g_r = guide_db.get_guide_by_email(email)
            if g_r and g_r.get("totp_enabled"):
                otp_r = guide_db.create_guide_otp(g_r["id"])
                from email_sender import send_otp_email
                send_otp_email(email, otp_r)
            redirect(self, "/guide/2fa?email=" + _up.quote(email)); return
        if path.startswith("/guide/"):
            g_tok = get_token(cookie, "atlas_guide")
            guide = guide_db.get_guide_by_token(g_tok)
            if not guide:
                redirect(self, "/guide"); return
            section = path.replace("/guide/","").replace("/guide","") or "dashboard"
            html_out = {
                "dashboard":    lambda: guide_portal.render_dashboard(guide, msg=urllib.parse.unquote_plus(params.get("msg",""))),
                "packages":     lambda: guide_portal.render_packages(guide, msg=urllib.parse.unquote_plus(params.get("msg","")), err=urllib.parse.unquote_plus(params.get("err",""))),
                "bookings":     lambda: guide_portal.render_bookings(guide, params.get("filter", params.get("status","all")), msg=urllib.parse.unquote_plus(params.get("msg",""))),
                "availability": lambda: guide_portal.render_availability(guide, msg=urllib.parse.unquote_plus(params.get("msg",""))),
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

        if path.startswith("/admin/"):
            _sess_tok = get_token(cookie, "atlas_admin") or ""
        elif path.startswith("/guide/"):
            _sess_tok = get_token(cookie, "atlas_guide") or ""
        else:
            _sess_tok = get_token(cookie, "atlas_token") or ""
        _csrf_exempt = {"/login.py", "/login/email", "/login/2fa",
                        "/signup/password", "/signup/verify", "/signup/resend",
                        "/verify", "/admin/login", "/guide/login", "/guide/2fa",
                        "/profile/photo", "/admin/profile/photo", "/auth/google/complete", "/setup-2fa",
                        "/guide/profile/doc", "/guide/profile/photo", "/guide/setup-2fa"}

        if path not in _csrf_exempt and not _csrf_ok(form, _sess_tok):
            self.send_error(403, "Invalid or missing CSRF token"); return

        if path == "/login.py":
            import urllib.parse as _up
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
            # 2FA check — email OTP
            if usr.get("totp_enabled"):
                import urllib.parse as _up2
                otp_code = db.create_user_otp(usr["id"])
                from email_sender import send_otp_email
                send_otp_email(usr["email"], otp_code)
                redirect(self, "/login/2fa?email=" + _up2.quote(usr["email"])); return
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
            import urllib.parse as _up
            email = form.get("email","").strip().lower()
            pw    = form.get("password","").strip()
            if not email:
                redirect(self, "/login.py"); return
            # Server-side password validation — must be at least 12 characters
            if len(pw) < 12:
                redirect(self, "/signup/password?email=" + _up.quote(email) +
                         "&error=Password+must+be+at+least+12+characters"); return
            # Store pending and send code
            code = db.store_signup_pending(email, pw)
            from email_sender import send_verification_email
            fname_guess = email.split("@")[0].capitalize()
            send_verification_email(email, fname_guess, code)
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
                from email_sender import send_verification_email
                fname_guess = email.split("@")[0].capitalize()
                send_verification_email(email, fname_guess, new_code)
            redirect(self, "/signup/verify?email=" + _up.quote(email)); return

        # ── Tourist email OTP verification ──
        elif path == "/login/2fa":
            import urllib.parse as _up
            email = form.get("email","").strip().lower()
            code  = form.get("code","").strip()
            usr2  = db.get_user_by_email(email)
            if not usr2 or not db.verify_user_otp(usr2["id"], code):
                redirect(self, "/login/2fa?email=" + _up.quote(email) +
                         "&error=Invalid+or+expired+code.+Please+try+again."); return
            # Issue session
            tok2 = secrets.token_hex(32)
            import mysql.connector as _mc2
            _conn2a = db.get_conn(); _cur2a = _conn2a.cursor()
            _cur2a.execute("INSERT INTO sessions (token,user_id) VALUES (%s,%s)", (tok2, usr2["id"]))
            _conn2a.commit(); _cur2a.close(); _conn2a.close()
            redirect(self, "/", f"atlas_token={tok2}; Path=/; Max-Age=86400"); return

        # ── Admin POST ──
        elif path == "/admin/login":
            result = admin_login.handle_post(form)
            if result.get("token"):
                redirect(self, "/admin/dashboard", f"atlas_admin={result['token']}; Path=/; Max-Age=86400")
            else:
                send_html(self, admin_login.render(error=result.get("error","")))

        # ── Guide POST ──
        elif path == "/guide/login":
            import urllib.parse as _up
            result = guide_portal.handle_login(form) if hasattr(guide_portal, 'handle_login') else {}
            if result.get("token"):
                guide_obj = guide_db.get_guide_by_token(result["token"])
                if guide_obj and guide_obj.get("totp_enabled"):
                    # 2FA on — invalidate the temp session, send OTP instead
                    guide_db.logout_guide(result["token"])
                    otp_code = guide_db.create_guide_otp(guide_obj["id"])
                    from email_sender import send_otp_email
                    send_otp_email(guide_obj["email"], otp_code)
                    redirect(self, "/guide/2fa?email=" + _up.quote(guide_obj["email"])); return
                dest = "/guide/dashboard?welcome=1" if result.get("new") else "/guide/dashboard"
                redirect(self, dest, f"atlas_guide={result['token']}; Path=/; Max-Age=86400")
            else:
                send_html(self, guide_portal.render_login(error=result.get("error","")))

        elif path == "/guide/2fa":
            import urllib.parse as _up
            email = form.get("email","").strip().lower()
            code  = form.get("code","").strip()
            g_obj = guide_db.get_guide_by_email(email)
            if not g_obj or not guide_db.verify_guide_otp(g_obj["id"], code):
                redirect(self, "/guide/2fa?email=" + _up.quote(email) +
                         "&error=Invalid+or+expired+code.+Please+try+again."); return
            # Issue fresh guide session
            g_tok2 = secrets.token_hex(32)
            _gc = guide_db.get_conn(); _gcu = _gc.cursor()
            _gcu.execute("INSERT INTO guide_sessions (token,guide_id) VALUES (%s,%s)",
                         (g_tok2, g_obj["id"]))
            _gc.commit(); _gcu.close(); _gc.close()
            redirect(self, "/guide/dashboard",
                     f"atlas_guide={g_tok2}; Path=/; Max-Age=86400"); return

        elif path.startswith("/guide/"):
            g_tok = get_token(cookie, "atlas_guide")
            guide = guide_db.get_guide_by_token(g_tok)
            if not guide:
                redirect(self, "/guide"); return
            section = path.replace("/guide/","")
            if section == "dashboard":
                action     = form.get("action", "")
                booking_id = int(form.get("booking_id", 0) or 0)
                if action and booking_id:
                    status_map = {
                        "accept_booking": "accepted",
                        "reject_booking": "rejected",
                    }
                    if action in status_map:
                        guide_db.update_booking_status(booking_id, guide["id"], status_map[action])
                        label = "accepted" if action == "accept_booking" else "rejected"
                        redirect(self, f"/guide/dashboard?msg=Booking+{label}"); return
                send_html(self, guide_portal.render_dashboard(guide, msg=form.get("msg","").replace("+"," ")))
            elif section == "packages":
                action = form.get("action", "")
                if action == "add_package":
                    title = form.get("title", "").strip()
                    price = form.get("price", "").strip()
                    if title and price:
                        guide_db.add_package(guide["id"], {
                            "title":       title,
                            "price":       price,
                            "duration":    form.get("duration", "Full Day").strip(),
                            "city":        form.get("city", "Manila").strip(),
                            "description": form.get("description", "").strip(),
                            "inclusions":  form.get("inclusions", "").strip(),
                        })
                        redirect(self, "/guide/packages?msg=Package+added+successfully"); return
                    else:
                        send_html(self, guide_portal.render_packages(guide, err="Title and price are required.")); return
                elif action == "delete_package":
                    pkg_id = int(form.get("pkg_id", 0) or 0)
                    if pkg_id:
                        guide_db.delete_package(pkg_id, guide["id"])
                    redirect(self, "/guide/packages?msg=Package+deleted"); return
                send_html(self, guide_portal.render_packages(guide))
            elif section == "bookings":
                parsed_post = urllib.parse.urlparse(self.path)
                post_params = dict(urllib.parse.parse_qsl(parsed_post.query))
                filter_status = post_params.get("filter", "all")
                action     = form.get("action", "")
                booking_id = int(form.get("booking_id", 0) or 0)
                if action and booking_id:
                    status_map = {
                        "accept_booking":   "accepted",
                        "reject_booking":   "rejected",
                        "complete_booking": "completed",
                        "cancel_booking":   "cancelled",
                    }
                    if action == "reschedule_booking":
                        new_date = form.get("new_date", "").strip()
                        if new_date:
                            guide_db.reschedule_booking(booking_id, guide["id"], new_date)
                        redirect(self, f"/guide/bookings?filter={filter_status}&msg=Booking+rescheduled"); return
                    elif action in status_map:
                        guide_db.update_booking_status(booking_id, guide["id"], status_map[action])
                        msg_map = {
                            "accept_booking":   "Booking+accepted",
                            "reject_booking":   "Booking+rejected",
                            "complete_booking": "Booking+marked+as+completed",
                            "cancel_booking":   "Booking+cancelled",
                        }
                        redirect(self, f"/guide/bookings?filter={filter_status}&msg={msg_map[action]}"); return
                send_html(self, guide_portal.render_bookings(guide, filter_status))
            elif section == "availability":
                action = form.get("action", "")
                if action == "update_availability":
                    days = urllib.parse.parse_qs(body).get("days", [])
                    avail_str = ", ".join(days) if days else ""
                    avail_note = form.get("avail_note", "").strip()
                    guide_db.update_guide_profile(guide["id"], {
                        "phone":        guide.get("phone", ""),
                        "city":         guide.get("city", "Manila"),
                        "languages":    guide.get("languages", "EN, FIL"),
                        "speciality":   guide.get("speciality", ""),
                        "bio":          guide.get("bio", ""),
                        "rate":         guide.get("rate", "P1,500/day"),
                        "availability": avail_str,
                    })
                    import mysql.connector as _mc
                    try:
                        _conn = guide_db.get_conn(); _cur = _conn.cursor()
                        _cur.execute("UPDATE tour_guides SET avail_note=%s WHERE id=%s", (avail_note, guide["id"]))
                        _conn.commit(); _cur.close(); _conn.close()
                    except Exception:
                        pass
                    guide = guide_db.get_guide_by_token(g_tok)
                    send_html(self, guide_portal.render_availability(guide, msg="Availability updated successfully!")); return
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
            elif section == "profile/doc":
                import uuid as _uuid, re as _re
                if "multipart/form-data" not in content_type:
                    redirect(self, "/guide/profile?err=bad+request"); return
                boundary_match = _re.search(r'boundary=[""]?([^""\s;]+)[""]?', content_type)
                if not boundary_match:
                    redirect(self, "/guide/profile?err=Missing+multipart+boundary"); return
                boundary = boundary_match.group(1).encode("latin-1")
                delimiter = b"--" + boundary
                parts = raw_body.split(delimiter)
                filename = file_bytes = None
                for part in parts:
                    if not part.strip(b"\r\n") or part.strip(b"\r\n") == b"--": continue
                    if part.startswith(b"\r\n"): part = part[2:]
                    elif part.startswith(b"\n"): part = part[1:]
                    sep = b"\r\n\r\n" if b"\r\n\r\n" in part else b"\n\n"
                    if sep not in part: continue
                    hdr, _, pb = part.partition(sep)
                    ht = hdr.decode("latin-1", errors="replace")
                    if 'name="doc_file"' not in ht and "name='doc_file'" not in ht: continue
                    fm = _re.search(r'filename=["\']([^"\']+)["\']', ht, _re.IGNORECASE)
                    if not fm: continue
                    filename = fm.group(1)
                    if pb.endswith(b"\r\n"): pb = pb[:-2]
                    elif pb.endswith(b"\n"): pb = pb[:-1]
                    file_bytes = pb; break
                if not filename or not file_bytes:
                    redirect(self, "/guide/profile?err=No+file+received"); return
                ext = os.path.splitext(filename)[-1].lower().lstrip(".")
                if ext not in {"jpg","jpeg","png","webp","pdf"}:
                    redirect(self, "/guide/profile?err=Only+JPG%2C+PNG%2C+WEBP+or+PDF+allowed"); return
                if len(file_bytes) > 5*1024*1024:
                    redirect(self, "/guide/profile?err=File+too+large+%28max+5+MB%29"); return
                if len(file_bytes) == 0:
                    redirect(self, "/guide/profile?err=Empty+file"); return
                udir = os.path.join(BASE, "uploads"); os.makedirs(udir, exist_ok=True)
                sname = f"guide_doc_{guide['id']}_{_uuid.uuid4().hex[:8]}.{ext}"
                with open(os.path.join(udir, sname), "wb") as fh: fh.write(file_bytes)
                guide_db.save_guide_doc(guide["id"], f"/uploads/{sname}")
                redirect(self, "/guide/profile?msg=Document+uploaded+and+submitted+for+review"); return
            elif section == "profile/photo":
                import uuid as _uuid, re as _re
                if "multipart/form-data" not in content_type:
                    redirect(self, "/guide/profile?err=bad+request"); return
                boundary_match = _re.search(r'boundary=[""]?([^""\s;]+)[""]?', content_type)
                if not boundary_match:
                    redirect(self, "/guide/profile?err=Missing+multipart+boundary"); return
                boundary = boundary_match.group(1).encode("latin-1")
                delimiter = b"--" + boundary
                parts = raw_body.split(delimiter)
                filename = file_bytes = None
                for part in parts:
                    if not part.strip(b"\r\n") or part.strip(b"\r\n") == b"--": continue
                    if part.startswith(b"\r\n"): part = part[2:]
                    elif part.startswith(b"\n"): part = part[1:]
                    sep = b"\r\n\r\n" if b"\r\n\r\n" in part else b"\n\n"
                    if sep not in part: continue
                    hdr, _, pb = part.partition(sep)
                    ht = hdr.decode("latin-1", errors="replace")
                    if 'name="photo_file"' not in ht and "name='photo_file'" not in ht: continue
                    fm = _re.search(r'filename=["\']([^"\']+)["\']', ht, _re.IGNORECASE)
                    if not fm: continue
                    filename = fm.group(1)
                    if pb.endswith(b"\r\n"): pb = pb[:-2]
                    elif pb.endswith(b"\n"): pb = pb[:-1]
                    file_bytes = pb; break
                if not filename or not file_bytes:
                    redirect(self, "/guide/profile?err=No+file+received"); return
                ext = os.path.splitext(filename)[-1].lower().lstrip(".")
                if ext not in {"jpg","jpeg","png","webp"}:
                    redirect(self, "/guide/profile?err=Only+JPG%2C+PNG+or+WEBP+allowed"); return
                if len(file_bytes) > 3*1024*1024:
                    redirect(self, "/guide/profile?err=File+too+large+%28max+3+MB%29"); return
                if len(file_bytes) == 0:
                    redirect(self, "/guide/profile?err=Empty+file"); return
                udir = os.path.join(BASE, "uploads"); os.makedirs(udir, exist_ok=True)
                sname = f"guide_{guide['id']}_{_uuid.uuid4().hex[:8]}.{ext}"
                with open(os.path.join(udir, sname), "wb") as fh: fh.write(file_bytes)
                guide_db.update_guide_photo(guide["id"], f"/uploads/{sname}")
                redirect(self, "/guide/profile?msg=Photo+updated+successfully"); return
            elif section == "setup-2fa":
                action = form.get("action","")
                if action == "enable":
                    guide_db.enable_guide_2fa(guide["id"], True)
                    redirect(self, "/guide/profile?msg=Two-factor+authentication+enabled"); return
                elif action == "disable":
                    guide_db.enable_guide_2fa(guide["id"], False)
                    redirect(self, "/guide/profile?msg=Two-factor+authentication+disabled"); return
                redirect(self, "/guide/setup-2fa"); return
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

            import re as _re2
            m_add = _re2.match(r"^/admin/transport/add$", path)
            if m_add:
                admin_db.add_transport(
                    form.get("route", "").strip(),
                    form.get("type", "Bus").strip(),
                    form.get("origin", "").strip(),
                    form.get("dest", "").strip(),
                    form.get("fare", "").strip(),
                )
                redirect(self, "/admin/transport?tab=list&msg=Route+added")
                return

            m2 = _re2.match(r"^/admin/transport/edit/(\d+)$", path)
            if m2:
                admin, tok = self.require_admin()
                if not admin: return
                tid = int(m2.group(1))
                admin_db.update_transport(
                    tid,
                    form.get("route","").strip(),
                    form.get("type","Bus").strip(),
                    form.get("origin","").strip(),
                    form.get("dest","").strip(),
                    form.get("fare","").strip(),
                )
                redirect(self, "/admin/transport?tab=list&msg=Route+updated")
                return

            if path == "/admin/profile/update":
                action = form.get("action", "change_password")
                if action == "update_info":
                    fullname = form.get("fullname", "").strip()
                    email    = form.get("email", "").strip().lower()
                    if not fullname:
                        send_html(self, admin_panel.profile_page(admin, err="Full name cannot be empty.", csrf=_csrf_token(tok)))
                        return
                    if not email or "@" not in email:
                        send_html(self, admin_panel.profile_page(admin, err="Please enter a valid email address.", csrf=_csrf_token(tok)))
                        return
                    admin_db.update_admin_profile(admin["id"], fullname, email)
                    admin = admin_db.get_admin_by_token(tok)
                    send_html(self, admin_panel.profile_page(admin, msg="Profile updated successfully!", csrf=_csrf_token(tok)))
                else:  # change_password
                    new_password     = form.get("new_password",     "").strip()
                    confirm_password = form.get("confirm_password", "").strip()
                    if not new_password:
                        send_html(self, admin_panel.profile_page(admin, err="Please enter a new password.", csrf=_csrf_token(tok)))
                        return
                    if len(new_password) < 8:
                        send_html(self, admin_panel.profile_page(admin, err="Password must be at least 8 characters.", csrf=_csrf_token(tok)))
                        return
                    if new_password != confirm_password:
                        send_html(self, admin_panel.profile_page(admin, err="Passwords do not match.", csrf=_csrf_token(tok)))
                        return
                    admin_db.update_admin_profile(admin["id"], admin.get("fullname",""), admin.get("email",""), new_password)
                    send_html(self, admin_panel.profile_page(admin, msg="Password changed successfully!", csrf=_csrf_token(tok)))
                return

            if path == "/admin/profile/photo":
                import uuid as _uuid2, re as _re3
                if "multipart/form-data" not in content_type:
                    redirect(self, "/admin/profile"); return
                boundary = ""
                for part in content_type.split(";"):
                    part = part.strip()
                    if part.startswith("boundary="):
                        boundary = part[9:].strip('"')
                        break
                if not boundary:
                    redirect(self, "/admin/profile"); return
                filename = ""; file_bytes = b""
                sep = ("--" + boundary).encode("latin-1")
                parts = raw_body.split(sep)
                for p in parts:
                    if b'name="photo"' not in p: continue
                    header_end = p.find(b"\r\n\r\n")
                    if header_end == -1: continue
                    header_block = p[:header_end].decode("latin-1","replace")
                    fn_match = __import__("re").search(r'filename="([^"]+)"', header_block)
                    if fn_match: filename = fn_match.group(1)
                    body_part = p[header_end+4:]
                    if body_part.endswith(b"\r\n"): body_part = body_part[:-2]
                    file_bytes = body_part; break
                if not filename or not file_bytes:
                    redirect(self, "/admin/profile?err=No+file+received"); return
                ext = os.path.splitext(filename)[-1].lower().lstrip(".")
                if ext not in {"jpg","jpeg","png","webp"}:
                    redirect(self, "/admin/profile?err=Only+JPG%2C+PNG+or+WEBP+allowed"); return
                if len(file_bytes) > 3*1024*1024:
                    redirect(self, "/admin/profile?err=File+too+large+%28max+3+MB%29"); return
                uploads_dir = os.path.join(BASE, "uploads")
                os.makedirs(uploads_dir, exist_ok=True)
                safe_name = f"admin_{admin['id']}_{_uuid2.uuid4().hex[:8]}.{ext}"
                with open(os.path.join(uploads_dir, safe_name), "wb") as fh: fh.write(file_bytes)
                photo_url = f"/uploads/{safe_name}"
                admin_db.update_admin_profile(admin["id"], admin.get("fullname",""), admin.get("email",""), photo_url=photo_url)
                redirect(self, "/admin/profile"); return

        elif path == "/profile/photo":
            # ── Upload profile photo (Python 3.14-compatible, no cgi module) ──
            if not user:
                redirect(self, "/login.py"); return
            import uuid as _uuid, re as _re

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
                user = db.get_user_by_token(token)
                send_html(self, profile_page.render(user=user, msg="Profile updated successfully."))
            elif action == "update_contact":
                phone = form.get("phone", "").strip()
                try:
                    import mysql.connector as _mc
                    _conn = db.get_conn(); _cur = _conn.cursor()
                    _cur.execute("UPDATE users SET phone=%s WHERE id=%s", (phone, user["id"]))
                    _conn.commit(); _cur.close(); _conn.close()
                except Exception:
                    pass
                user = db.get_user_by_token(token)
                send_html(self, profile_page.render(user=user, msg="Contact number saved."))
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

        elif path == "/setup-2fa":
            if not user:
                redirect(self, "/login.py"); return
            action = form.get("action","")
            if action == "enable":
                _conn3 = db.get_conn(); _cur3 = _conn3.cursor()
                _cur3.execute("UPDATE users SET totp_enabled=1 WHERE id=%s", (user["id"],))
                _conn3.commit(); _cur3.close(); _conn3.close()
                redirect(self, "/profile.py?msg=Two-factor+authentication+enabled"); return
            elif action == "disable":
                _conn4 = db.get_conn(); _cur4 = _conn4.cursor()
                _cur4.execute("UPDATE users SET totp_enabled=0 WHERE id=%s", (user["id"],))
                _conn4.commit(); _cur4.close(); _conn4.close()
                redirect(self, "/profile.py?msg=Two-factor+authentication+disabled"); return
            redirect(self, "/setup-2fa")



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