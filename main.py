#!/usr/bin/env python3
import http.server, socketserver, urllib.parse, os, sys, re, email
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


import index, flights, weather, attractions, restaurants, guides, transport, itinerary
import login, register, db_sqlite as db
import admin_login, admin_panel, admin_db_sqlite as admin_db
import guide_portal
import profile as profile_page, guide_db_sqlite as guide_db
import flight_booking_sqlite as flight_booking, setup_2fa, guide_verification, system_messaging_sqlite as system_messaging

PORT = int(os.environ.get("PORT", 5000))
BASE = os.path.dirname(os.path.abspath(__file__))
CSS  = os.path.join(BASE, "css", "styles.css")

ROUTES = {
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

    "/setup-2fa":      lambda p, u: setup_2fa.render(u) if u else setup_2fa.render(),
    "/book-flight":    lambda p, u: flight_booking.handle_flight_booking(p, u) if u else None,
    "/booking-confirmation": lambda p, u: flight_booking.render_booking_confirmation(p.get('id', ''), u) if u else None,
    "/guide-verification": lambda p, u: guide_verification.render_verification_panel(u) if u else None,
    "/system-messages": lambda p, u: system_messaging.render_thread_list(u['id']) if u else None,
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
            return  # browser disconnected, safe to ignore
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
        user   = db.get_user_from_token(token)

        # CSS
        if path == "/css/styles.css":
            with open(CSS,"rb") as f: css = f.read()
            self.send_response(200)
            self.send_header("Content-Type","text/css; charset=utf-8")
            self.send_header("Content-Length", str(len(css)))
            self.end_headers()
            self.wfile.write(css)
            return

        # Serve ATLAS logo
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

        # Serve uploaded images
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


        # ── GUIDE PORTAL GET ──
        if path in ("/guide", "/guide/"):
            send_html(self, guide_portal.render_login()); return
        if path == "/guide/register":
            send_html(self, guide_portal.render_register()); return
        if path == "/guide/logout":
            g_tok = get_token(cookie, "atlas_guide")
            if g_tok: guide_db.logout_guide(g_tok)
            redirect(self, "/guide", "atlas_guide=; Path=/; Max-Age=0"); return
        if path == "/guide/dashboard":
            g_tok = get_token(cookie, "atlas_guide")
            guide = guide_db.get_guide_by_token(g_tok)
            if not guide: redirect(self, "/guide"); return
            send_html(self, guide_portal.render_dashboard(guide)); return
        if path == "/guide/packages":
            g_tok = get_token(cookie, "atlas_guide")
            guide = guide_db.get_guide_by_token(g_tok)
            if not guide: redirect(self, "/guide"); return
            send_html(self, guide_portal.render_packages(guide)); return
        if path == "/guide/bookings":
            g_tok = get_token(cookie, "atlas_guide")
            guide = guide_db.get_guide_by_token(g_tok)
            if not guide: redirect(self, "/guide"); return
            params = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(self.path).query))
            send_html(self, guide_portal.render_bookings(guide, params.get("filter","all"))); return
        if path == "/guide/availability":
            g_tok = get_token(cookie, "atlas_guide")
            guide = guide_db.get_guide_by_token(g_tok)
            if not guide: redirect(self, "/guide"); return
            send_html(self, guide_portal.render_availability(guide)); return
        if path == "/guide/ratings":
            g_tok = get_token(cookie, "atlas_guide")
            guide = guide_db.get_guide_by_token(g_tok)
            if not guide: redirect(self, "/guide"); return
            send_html(self, guide_portal.render_ratings(guide)); return
        if path == "/guide/profile":
            g_tok = get_token(cookie, "atlas_guide")
            guide = guide_db.get_guide_by_token(g_tok)
            if not guide: redirect(self, "/guide"); return
            send_html(self, guide_portal.render_profile(guide)); return
        if path == "/guide/profile/photo":
            redirect(self, "/guide/profile"); return

        # User logout
        if path == "/logout.py":
            if token: db.logout_user(token)
            send_html(self, '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"/>
<title>Logged Out - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css"/>
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
<style>
body{font-family:'Segoe UI',sans-serif;background:#F8FAFC;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}
.logout-box{background:#fff;border-radius:16px;padding:48px;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,.1);max-width:400px}
.logout-icon{font-size:64px;margin-bottom:20px}
.logout-title{font-size:24px;font-weight:800;color:#1F2937;margin-bottom:12px}
.logout-text{font-size:16px;color:#6B7280;margin-bottom:24px}
.btn{display:inline-block;padding:12px 24px;background:#0038A8;color:#fff;text-decoration:none;border-radius:8px;font-weight:600}
.btn:hover{background:#0050D0}
</style>
</head>
<body>
<div class="logout-box">
  <div class="logout-icon">&#128075;</div>
  <div class="logout-title">Logged Out Successfully</div>
  <div class="logout-text">You have been safely logged out of your ATLAS account.</div>
  <a href="/" class="btn">Return to Home</a>
</div>
<script>
Swal.fire({
  title: 'Logged Out!',
  text: 'You have been successfully logged out.',
  icon: 'success',
  timer: 2000,
  showConfirmButton: false
});
</script>
</body>
</html>''')
            return

        # Admin entry
        if path in ("/admin", "/admin/"):
            redirect(self, "/admin/login"); return
        if path == "/admin/login":
            send_html(self, admin_login.render()); return
        if path == "/admin/logout":
            _, a_tok = self.get_admin()
            if a_tok: admin_db.admin_logout(a_tok)
            redirect(self, "/admin/login", "atlas_admin=; Path=/; Max-Age=0"); return

        # Protected admin routes
        if path.startswith("/admin/"):
            admin, _ = self.get_admin()
            if not admin:
                redirect(self, "/admin/login"); return

            if path == "/admin/dashboard":
                send_html(self, admin_panel.dashboard(admin)); return
            if path == "/admin/tourists":
                tab = params.get("tab","active")
                send_html(self, admin_panel.tourists_page(admin, tab=tab)); return
            if path.startswith("/admin/tourists/archive/"):
                uid = path.split("/")[-1]
                admin_db.set_tourist_status(uid, "archived")
                redirect(self, "/admin/tourists"); return
            if path.startswith("/admin/tourists/suspend/"):
                admin_db.set_tourist_status(path.split("/")[-1], "suspended")
                redirect(self, "/admin/tourists"); return
            if path.startswith("/admin/tourists/activate/"):
                admin_db.set_tourist_status(path.split("/")[-1], "active")
                redirect(self, "/admin/tourists"); return
            if path.startswith("/admin/tourists/delete/"):
                admin_db.delete_tourist(path.split("/")[-1])
                redirect(self, "/admin/tourists"); return
                send_html(self, admin_panel.flights_page(admin)); return
                admin_db.delete_flight(path.split("/")[-1])
                send_html(self, admin_panel.spots_page(admin)); return
                admin_db.delete_spot(path.split("/")[-1])
                send_html(self, admin_panel.restaurants_page(admin)); return
                admin_db.delete_restaurant(path.split("/")[-1])

            if path == "/admin/spots":
                pg = int(params.get("page","1") or "1")
                send_html(self, admin_panel.spots_page(admin, page=pg)); return
            if path.startswith("/admin/spots/delete/"):
                admin_db.delete_spot(path.split("/")[-1])
                redirect(self, "/admin/spots"); return
            if path == "/admin/restaurants":
                pg = int(params.get("page","1") or "1")
                send_html(self, admin_panel.restaurants_page(admin, page=pg)); return
            if path.startswith("/admin/restaurants/delete/"):
                admin_db.delete_restaurant(path.split("/")[-1])
                redirect(self, "/admin/restaurants"); return
            if path == "/admin/guides":
                pg = int(params.get("page","1") or "1")
                tab = params.get("tab","registered")
                send_html(self, admin_panel.guides_page(admin, page=pg, tab=tab)); return
            if path.startswith("/admin/guides/delete/"):
                admin_db.delete_guide(path.split("/")[-1])
                redirect(self, "/admin/guides"); return
            if path == "/admin/transport":
                pg = int(params.get("page","1") or "1")
                send_html(self, admin_panel.transport_page(admin, page=pg)); return
            if path.startswith("/admin/transport/delete/"):
                admin_db.delete_transport(path.split("/")[-1])
                redirect(self, "/admin/transport"); return
            if path == "/admin/flights":
                send_html(self, admin_panel.flights_page(admin)); return
            if path.startswith("/admin/flights/delete/"):
                admin_db.delete_flight(path.split("/")[-1])
                redirect(self, "/admin/flights"); return
            if path == "/admin/profile":
                send_html(self, admin_panel.profile_page(admin)); return
            redirect(self, "/admin/dashboard"); return

        # Email verification route (GET = show verify page)
        if path == "/verify":
            email = params.get("email","")
            if email:
                send_html(self, register.render_verify(email)); return
            redirect(self, "/register.py"); return

        # Public routes
        handler = ROUTES.get(path)
        if handler is None:
            self.send_error(404, "Page not found"); return
        send_html(self, handler(params, user))

    def do_POST(self):
        path   = urllib.parse.urlparse(self.path).path
        cookie = self.headers.get("Cookie","")
        content_type = self.headers.get("Content-Type","")
        length = int(self.headers.get("Content-Length",0))

        # Handle multipart/form-data (file uploads)
        if "multipart/form-data" in content_type:
            raw = self.rfile.read(length)
            form = {}
            files = {}
            body = ""
            # Extract boundary
            boundary = None
            for part in content_type.split(";"):
                part = part.strip()
                if part.startswith("boundary="):
                    boundary = part[len("boundary="):].strip().encode()
                    break
            if boundary:
                delimiter = b"--" + boundary
                parts = raw.split(delimiter)
                for chunk in parts[1:]:  # skip preamble
                    if chunk.strip() in (b"", b"--", b"--\r\n"):
                        continue
                    # Split headers from body on first blank line
                    if b"\r\n\r\n" in chunk:
                        hdr_raw, _, value = chunk.partition(b"\r\n\r\n")
                    elif b"\n\n" in chunk:
                        hdr_raw, _, value = chunk.partition(b"\n\n")
                    else:
                        continue
                    # Strip trailing boundary delimiter marker
                    value = value.rstrip(b"\r\n")
                    # Parse headers
                    hdr_text = hdr_raw.decode("utf-8", errors="replace")
                    disposition = ""
                    content_name = None
                    filename = None
                    for line in hdr_text.splitlines():
                        if line.lower().startswith("content-disposition:"):
                            disposition = line
                            m = re.search(r'name="([^"]*)"', line)
                            if m: content_name = m.group(1)
                            m = re.search(r'filename="([^"]*)"', line)
                            if m: filename = m.group(1)
                    if content_name is None:
                        continue
                    if filename:
                        files[content_name] = (filename, value)
                    else:
                        form[content_name] = value.decode("utf-8", errors="replace")
        else:
            body = self.rfile.read(length).decode("utf-8")
            form = dict(urllib.parse.parse_qsl(body))
            files = {}

        if path == "/login.py":
            token, err = login.handle_post(form)
            if token: redirect(self, "/", f"atlas_token={token}; Path=/; Max-Age=86400")
            else: send_html(self, err)

        elif path == "/register.py":
            _, html = register.handle_post(form)
            send_html(self, html)

        elif path == "/verify":
            email = form.get("email","").strip().lower()
            code  = form.get("code","").strip()
            if not email or not code:
                send_html(self, register.render_verify(email, error="Missing email or code.")); return
            ok, msg = db.activate_user(email, code)
            if ok:
                send_html(self, login.render(success="Account verified! You can now log in."))
            else:
                send_html(self, register.render_verify(email, error=msg))

        elif path == "/admin/login":
            token, err = admin_login.handle_post(form)
            if token: redirect(self, "/admin/dashboard", f"atlas_admin={token}; Path=/; Max-Age=86400")
            else: send_html(self, err)

        elif path.startswith("/admin/"):
            a_tok = get_token(cookie, "atlas_admin")
            admin = admin_db.get_admin_by_token(a_tok)
            if not admin:
                redirect(self, "/admin/login"); return

                try:
                    admin_db.add_flight(form.get("airline",""),form.get("origin",""),form.get("dest",""),
                        form.get("dep_time",""),form.get("arr_time",""),form.get("price",""),form.get("status","Scheduled"))
                    send_html(self, admin_panel.flights_page(admin, msg="Flight added!"))
                except Exception as e: send_html(self, admin_panel.flights_page(admin))

                try:
                    admin_db.add_spot(form.get("name",""),form.get("city",""),form.get("category",""),
                        form.get("type",""),form.get("rating","4.0"),form.get("entry","Free"),
                        form.get("hours","8AM-5PM"),form.get("desc",""))
                    send_html(self, admin_panel.spots_page(admin, msg="Attraction added!"))
                except Exception as e: send_html(self, admin_panel.spots_page(admin))

                try:
                    admin_db.add_restaurant(form.get("name",""),form.get("city",""),form.get("cuisine",""),
                        form.get("price",""),form.get("rating","4.0"),form.get("hours",""))
                    send_html(self, admin_panel.restaurants_page(admin, msg="Restaurant added!"))
                except Exception as e: send_html(self, admin_panel.restaurants_page(admin))


            elif path == "/admin/spots/add":
                try:
                    img_url = ""
                    if "image_file" in files:
                        fname, fdata = files["image_file"]
                        if fdata: img_url = admin_panel.save_image(fdata, fname)
                    admin_db.add_spot(form.get("name",""),form.get("city",""),form.get("category",""),
                        form.get("type",""),form.get("rating","4.0"),form.get("entry","Free"),
                        form.get("hours","8AM-5PM"),form.get("desc",""),img_url)
                    send_html(self, admin_panel.spots_page(admin, msg="Attraction added!", tab="list"))
                except Exception as e: send_html(self, admin_panel.spots_page(admin, err=str(e)))

            elif path == "/admin/restaurants/add":
                try:
                    img_url = ""
                    if "image_file" in files:
                        fname, fdata = files["image_file"]
                        if fdata: img_url = admin_panel.save_image(fdata, fname)
                    admin_db.add_restaurant(form.get("name",""),form.get("city",""),form.get("cuisine",""),
                        form.get("price",""),form.get("rating","4.0"),form.get("hours",""),img_url)
                    send_html(self, admin_panel.restaurants_page(admin, msg="Restaurant added!", tab="list"))
                except Exception as e: send_html(self, admin_panel.restaurants_page(admin, err=str(e)))
            elif path == "/admin/guides/add":
                try:
                    img_url = ""
                    if "image_file" in files:
                        fname, fdata = files["image_file"]
                        if fdata: img_url = admin_panel.save_image(fdata, fname)
                    admin_db.add_guide(form.get("name",""),form.get("city",""),form.get("language",""),
                        form.get("rate",""),form.get("rating","4.5"),form.get("bio",""),img_url)
                    send_html(self, admin_panel.guides_page(admin, msg="Tour guide added!", tab="added"))
                except Exception as e: send_html(self, admin_panel.guides_page(admin, err=str(e)))

            elif path == "/admin/flights/add":
                try:
                    admin_db.add_flight(form.get("airline",""),form.get("origin",""),form.get("dest",""),
                        form.get("dep_time",""),form.get("arr_time",""),form.get("price",""),form.get("status","Scheduled"))
                    send_html(self, admin_panel.flights_page(admin, msg="Flight added!"))
                except Exception as e: send_html(self, admin_panel.flights_page(admin, err=str(e)))

            elif path == "/admin/transport/add":
                try:
                    admin_db.add_transport(form.get("route",""),form.get("type",""),form.get("origin",""),
                        form.get("dest",""),form.get("dep_time",""),form.get("fare",""))
                    send_html(self, admin_panel.transport_page(admin, msg="Route added!", tab="list"))
                except Exception as e: send_html(self, admin_panel.transport_page(admin, err=str(e)))

            elif path == "/admin/profile/update":
                new_pw  = form.get("new_password","").strip()
                confirm = form.get("confirm_password","").strip()
                if not new_pw:
                    send_html(self, admin_panel.profile_page(admin, err="Please enter a new password."))
                elif new_pw != confirm:
                    send_html(self, admin_panel.profile_page(admin, err="Passwords do not match."))
                elif len(new_pw) < 8:
                    send_html(self, admin_panel.profile_page(admin, err="Password must be at least 8 characters."))
                else:
                    admin_db.update_admin_profile(admin["id"], admin.get("fullname",""), admin.get("email",""), new_pw)
                    updated = admin_db.get_admin_by_token(a_tok)
                    send_html(self, admin_panel.profile_page(updated, msg="Password changed successfully!"))
            else:
                self.send_error(404)


        elif path == "/guide/login":
            email = form.get("email",""); pw = form.get("password","")
            ok, token, guide = guide_db.login_guide(email, pw)
            if ok:
                redirect(self, "/guide/dashboard", f"atlas_guide={token}; Path=/; Max-Age=86400")
            else:
                send_html(self, guide_portal.render_login(error="Invalid email or password."))

        elif path == "/guide/register":
            fname=form.get("fname","").strip(); lname=form.get("lname","").strip()
            email=form.get("email","").strip(); pw=form.get("password","").strip()
            pw2=form.get("password2","").strip(); phone=form.get("phone","").strip()
            city=form.get("city","Manila")
            if not all([fname,lname,email,pw,phone]):
                send_html(self, guide_portal.render_register(error="Please fill in all required fields."))
            elif pw != pw2:
                send_html(self, guide_portal.render_register(error="Passwords do not match."))
            elif len(pw) < 6:
                send_html(self, guide_portal.render_register(error="Password must be at least 6 characters."))
            else:
                ok, msg = guide_db.register_guide(fname, lname, email, pw, phone, city)
                if ok:
                    send_html(self, guide_portal.render_login(success="Account created! Please log in."))
                else:
                    send_html(self, guide_portal.render_register(error=msg))

        elif path == "/guide/profile/photo":
            import uuid as _uuid
            g_tok = get_token(cookie, "atlas_guide")
            guide = guide_db.get_guide_by_token(g_tok)
            if not guide: redirect(self, "/guide"); return
            if "photo_file" in files:
                _fn, fdata = files["photo_file"]
                if fdata and len(fdata) <= 3*1024*1024:
                    ext = os.path.splitext(_fn)[-1].lower() or ".jpg"
                    if ext not in (".jpg",".jpeg",".png",".webp"): ext = ".jpg"
                    ud = os.path.join(BASE, "uploads"); os.makedirs(ud, exist_ok=True)
                    nfn = f"guide_{guide['id']}_{_uuid.uuid4().hex[:8]}{ext}"
                    with open(os.path.join(ud, nfn), "wb") as _f: _f.write(fdata)
                    _c = guide_db.get_conn()
                    _cur = _c.cursor()
                    _cur.execute("UPDATE tour_guides SET photo_url=%s WHERE id=%s", (f"/uploads/{nfn}", guide["id"]))
                    _c.commit(); _cur.close(); _c.close()
                    guide = guide_db.get_guide_by_id(guide["id"])
                    send_html(self, guide_portal.render_profile(guide, msg="Profile photo updated!")); return
                else:
                    send_html(self, guide_portal.render_profile(guide, err="File too large. Max 3 MB.")); return
            redirect(self, "/guide/profile"); return

        elif path.startswith("/guide/"):
            g_tok = get_token(cookie, "atlas_guide")
            guide = guide_db.get_guide_by_token(g_tok)
            if not guide:
                redirect(self, "/guide"); return
            action = form.get("action","")
            msg = ""; err = ""
            if action == "add_package":
                guide_db.add_package(guide["id"], form); msg = "Package added!"
            elif action == "delete_package":
                guide_db.delete_package(int(form.get("pkg_id",0)), guide["id"]); msg = "Package deleted."
            elif action == "accept_booking":
                guide_db.update_booking_status(int(form.get("booking_id",0)), guide["id"], "accepted"); msg = "Booking accepted!"
            elif action == "complete_booking":
                guide_db.update_booking_status(int(form.get("booking_id",0)), guide["id"], "completed"); msg = "Tour marked as completed!"
            elif action == "reject_booking":
                guide_db.update_booking_status(int(form.get("booking_id",0)), guide["id"], "rejected"); msg = "Booking rejected."
            elif action == "cancel_booking":
                guide_db.update_booking_status(int(form.get("booking_id",0)), guide["id"], "cancelled"); msg = "Booking cancelled."
            elif action == "reschedule_booking":
                new_date = form.get("new_date","")
                guide_db.update_booking_status(int(form.get("booking_id",0)), guide["id"], "rescheduled", f"Rescheduled to {new_date}"); msg = f"Rescheduled to {new_date}!"
            elif action == "update_availability":
                avail = ",".join([v for k,v in urllib.parse.parse_qsl(body) if k=="days"])
                if avail:
                    conn = guide_db.get_conn()
                    _cur = conn.cursor()
                    _cur.execute("UPDATE tour_guides SET availability=%s WHERE id=%s", (avail, guide["id"]))
                    conn.commit(); _cur.close(); conn.close()
                    guide = guide_db.get_guide_by_id(guide["id"])
                msg = "Availability updated!"
            elif action == "update_profile":
                guide_db.update_guide_profile(guide["id"], form)
                guide = guide_db.get_guide_by_id(guide["id"]); msg = "Profile updated!"
            elif action == "change_password":
                pw1=form.get("new_pw",""); pw2=form.get("new_pw2","")
                if pw1 and pw1==pw2 and len(pw1)>=6:
                    guide_db.change_guide_password(guide["id"], pw1); msg = "Password changed!"
                else: err = "Passwords do not match or too short."
            # Re-fetch guide to get latest data
            guide = guide_db.get_guide_by_id(guide["id"]) or guide
            # Route response to correct page
            if path == "/guide/dashboard":
                send_html(self, guide_portal.render_dashboard(guide, msg, err))
            elif path == "/guide/packages":
                send_html(self, guide_portal.render_packages(guide, msg, err))
            elif path == "/guide/bookings":
                _qp = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(self.path).query))
                send_html(self, guide_portal.render_bookings(guide, _qp.get("filter","all"), msg, err))
            elif path == "/guide/availability":
                send_html(self, guide_portal.render_availability(guide, msg, err))
            elif path == "/guide/profile":
                send_html(self, guide_portal.render_profile(guide, msg, err))
            elif path == "/guide/ratings":
                send_html(self, guide_portal.render_ratings(guide))
            else:
                redirect(self, "/guide/dashboard")

        elif path == "/profile/photo":
            import uuid as _uuid2
            p_tok2 = get_token(cookie, "atlas_token")
            pu2 = db.get_user_from_token(p_tok2) if p_tok2 else None
            if not pu2: redirect(self, "/login.py"); return
            if "photo_file" in files:
                _fn2, fdata2 = files["photo_file"]
                if fdata2 and len(fdata2) <= 3*1024*1024:
                    ext2 = os.path.splitext(_fn2)[-1].lower() or ".jpg"
                    if ext2 not in (".jpg",".jpeg",".png",".webp"): ext2 = ".jpg"
                    ud2 = os.path.join(BASE, "uploads"); os.makedirs(ud2, exist_ok=True)
                    nfn2 = f"tourist_{pu2['id']}_{_uuid2.uuid4().hex[:8]}{ext2}"
                    with open(os.path.join(ud2, nfn2), "wb") as _f2: _f2.write(fdata2)
                    _c2 = db.get_conn()
                    _cur2 = _c2.cursor()
                    _cur2.execute("UPDATE users SET photo_url=%s WHERE id=%s", (f"/uploads/{nfn2}", pu2["id"]))
                    _c2.commit(); _cur2.close(); _c2.close()
                    pu2 = db.get_user_from_token(p_tok2)
                    send_html(self, profile_page.render(user=pu2, msg="Profile photo updated!")); return
                else:
                    send_html(self, profile_page.render(user=pu2, err="File too large. Max 3 MB.")); return
            redirect(self, "/profile.py"); return

        elif path == "/profile/update":
            import hashlib
            p_token = get_token(cookie, "atlas_token")
            p_user  = db.get_user_from_token(p_token) if p_token else None
            if not p_user:
                redirect(self, "/login.py"); return
            action = form.get("action","")
            if action == "update_profile":
                conn2 = db.get_conn()
                _cur2 = conn2.cursor()
                _cur2.execute("UPDATE users SET email=%s WHERE id=%s",
                    (form.get("email",""), p_user["id"]))
                conn2.commit(); _cur2.close(); conn2.close()
                p_user = db.get_user_from_token(p_token)
                send_html(self, profile_page.render(user=p_user, msg="Profile updated successfully!"))
            elif action == "change_password":
                old_pw   = form.get("old_pw","")
                new_pw   = form.get("new_pw","")
                new_pw2  = form.get("new_pw2","")
                conn2    = db.get_conn()
                _cur2    = conn2.cursor(dictionary=True)
                _cur2.execute("SELECT password FROM users WHERE id=%s", (p_user["id"],))
                row      = _cur2.fetchone()
                _cur2.close(); conn2.close()
                hashed_old = hashlib.sha256(old_pw.encode()).hexdigest()
                if row and row["password"] == hashed_old:
                    if new_pw and new_pw == new_pw2 and len(new_pw) >= 6:
                        conn3 = db.get_conn()
                        _cur3 = conn3.cursor()
                        _cur3.execute("UPDATE users SET password=%s WHERE id=%s",
                            (hashlib.sha256(new_pw.encode()).hexdigest(), p_user["id"]))
                        conn3.commit(); _cur3.close(); conn3.close()
                        send_html(self, profile_page.render(user=p_user, msg="Password changed!"))
                    else:
                        send_html(self, profile_page.render(user=p_user, err="Passwords do not match or too short."))
                else:
                    send_html(self, profile_page.render(user=p_user, err="Current password is incorrect."))
            else:
                send_html(self, profile_page.render(user=p_user))
            return

        elif path == "/book-guide":
            guide_id_raw = form.get("guide_id","").strip()
            print(f"[BOOK-GUIDE] Received form: {form}", flush=True)  # server log
            gid = 0

            # Step 1: Use the numeric guide_id sent from the booking modal
            try:
                gid = int(guide_id_raw) if guide_id_raw else 0
            except Exception:
                gid = 0

            # Step 2: Fallback — match by exact full name if ID missing
            if not gid:
                gname = form.get("guide_name","").strip()
                try:
                    all_g = guide_db.get_public_guides()
                    for g2 in all_g:
                        full_name = f'{g2["fname"]} {g2["lname"]}'.strip()
                        if full_name == gname:
                            gid = g2["id"]; break
                except Exception as e:
                    print(f"[BOOK-GUIDE] Name lookup error: {e}", flush=True)

            print(f"[BOOK-GUIDE] Resolved guide_id={gid}", flush=True)

            # Validate required fields
            tourist_name  = form.get("tourist_name","").strip()
            tourist_phone = form.get("tourist_phone","").strip()
            tour_date     = form.get("tour_date","").strip()

            if not tourist_name or not tourist_phone or not tour_date:
                send_html(self, f"""<html><body style="font-family:sans-serif;padding:40px">
                <h2 style="color:#DC2626">&#9888; Missing Fields</h2>
                <p>Name: '{tourist_name}' | Phone: '{tourist_phone}' | Date: '{tour_date}'</p>
                <p>Full form received: {form}</p>
                <a href="/guides.py">Go back</a></body></html>"""); return

            if not gid:
                send_html(self, f"""<html><body style="font-family:sans-serif;padding:40px">
                <h2 style="color:#DC2626">&#9888; Guide Not Found</h2>
                <p>guide_id_raw='{guide_id_raw}' | guide_name='{form.get("guide_name","")}'</p>
                <p>Full form: {form}</p>
                <a href="/guides.py">Go back</a></body></html>"""); return

            # Use logged-in tourist email if available
            _btok  = get_token(cookie, "atlas_token")
            _buser = db.get_user_from_token(_btok) if _btok else None
            tourist_email = (_buser.get("email","") if _buser else "") or form.get("tourist_email","")

            booking_data = {
                "guide_id":      gid,
                "tourist_name":  tourist_name,
                "tourist_email": tourist_email,
                "tourist_phone": tourist_phone,
                "package_title": form.get("package_title",""),
                "tour_date":     tour_date,
                "pax":           form.get("pax", 1),
                "notes":         form.get("notes",""),
            }
            print(f"[BOOK-GUIDE] Inserting booking: {booking_data}", flush=True)
            try:
                guide_db.add_booking(booking_data)
                print("[BOOK-GUIDE] Booking saved OK", flush=True)
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                print(f"[BOOK-GUIDE] DB ERROR: {e}\n{tb}", flush=True)
                send_html(self, f"""<html><body style="font-family:sans-serif;padding:40px">
                <h2 style="color:#DC2626">&#9888; Database Error</h2>
                <pre style="background:#FEF2F2;padding:16px;border-radius:8px">{tb}</pre>
                <p>Booking data: {booking_data}</p>
                <a href="/guides.py">Go back</a></body></html>"""); return

            self.send_response(302)
            self.send_header("Location", "/guides.py?booked=1")
            self.end_headers(); return

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
    print(f"\n  Admin login: admin / admin123")
    print("  Ctrl+C to stop\n")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), ATLASHandler) as s:
        try: s.serve_forever()
        except KeyboardInterrupt: print("\n  Goodbye!")