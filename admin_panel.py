import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import admin_db
from datetime import datetime

CITIES = ["Manila","Baguio","Ilocos Norte","Vigan","Batangas","Tagaytay"]

# ── SHELL ──
def shell(title, body, active, admin):
    aname = admin.get("fullname","Admin") if admin else "Admin"
    ainit = aname[0].upper()
    today = datetime.now().strftime("%A, %B %d, %Y")
    nav = [
        ("dashboard", "dashboard.svg", "Dashboard"),
        ("tourists",  "tourists.svg",  "Tourists"),
        ("flights",   "flights.svg",   "Flights"),
        ("spots",     "spots.svg",     "Attractions"),
        ("restaurants","restaurants.svg","Restaurants"),
        ("guides",    "guides.svg",    "Tour Guides"),
        ("transport", "transport.svg", "Transportation"),
        ("profile",   "profile.svg",   "Admin Profile"),
    ]
    icons = {
        "dashboard":   "&#9732;",
        "tourists":    "&#128100;",
        "flights":     "&#9992;",
        "spots":       "&#127963;",
        "restaurants": "&#127869;",
        "guides":      "&#129517;",
        "transport":   "&#128652;",
        "profile":     "&#128100;",
    }
    nav_html = ""
    for key, _, label in nav:
        is_active = active == key
        bg = "background:#EEF2FF;color:#4338CA;font-weight:700;" if is_active else "color:#6B7280;"
        left = "border-left:3px solid #4338CA;" if is_active else "border-left:3px solid transparent;"
        nav_html += f'<a href="/admin/{key}" style="display:flex;align-items:center;gap:10px;padding:10px 20px;text-decoration:none;font-size:13.5px;{bg}{left}transition:all .15s">{icons[key]} {label}</a>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title} - ATLAS Admin</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',sans-serif;background:#F8FAFC;color:#1E293B;min-height:100vh;display:flex}}
.sidebar{{width:230px;flex-shrink:0;background:#fff;border-right:1px solid #E2E8F0;display:flex;flex-direction:column;height:100vh;position:sticky;top:0}}
.s-brand{{padding:20px 20px 16px;border-bottom:1px solid #E2E8F0}}
.s-logo-row{{display:flex;align-items:center;gap:10px}}
.s-logo{{width:36px;height:36px;background:linear-gradient(135deg,#0038A8,#CE1126);border-radius:10px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:16px}}
.s-title{{font-weight:900;font-size:17px;color:#1E293B}}
.s-badge{{font-size:9px;color:#6366F1;font-weight:700;background:#EEF2FF;padding:2px 8px;border-radius:10px;margin-top:2px;display:inline-block}}
.s-section{{font-size:10px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.8px;padding:16px 20px 6px}}
.s-bottom{{margin-top:auto;border-top:1px solid #E2E8F0;padding:12px 0}}
.main{{flex:1;display:flex;flex-direction:column;min-height:100vh;overflow-x:hidden}}
.topbar{{background:#fff;border-bottom:1px solid #E2E8F0;padding:14px 28px;display:flex;align-items:center;justify-content:space-between}}
.topbar-title{{font-size:20px;font-weight:800;color:#1E293B}}
.topbar-right{{display:flex;align-items:center;gap:16px}}
.topbar-date{{font-size:12px;color:#94A3B8}}
.admin-chip{{display:flex;align-items:center;gap:8px;background:#F1F5F9;border-radius:30px;padding:5px 14px 5px 6px}}
.admin-avatar{{width:28px;height:28px;background:linear-gradient(135deg,#0038A8,#CE1126);border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:13px}}
.admin-name{{font-size:13px;font-weight:700;color:#1E293B}}
.content{{padding:28px;flex:1}}
.stat-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px;margin-bottom:24px}}
.stat-card{{background:#fff;border:1px solid #E2E8F0;border-radius:14px;padding:20px;position:relative;overflow:hidden}}
.stat-label{{font-size:12px;font-weight:600;color:#94A3B8;margin-bottom:6px}}
.stat-val{{font-size:30px;font-weight:900;color:#1E293B}}
.stat-sub{{font-size:11px;color:#94A3B8;margin-top:3px}}
.stat-badge{{position:absolute;top:16px;right:16px;font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px}}
.stat-icon{{font-size:26px;margin-bottom:8px}}
.card{{background:#fff;border:1px solid #E2E8F0;border-radius:14px;overflow:hidden;margin-bottom:20px}}
.card-hdr{{padding:16px 20px;border-bottom:1px solid #F1F5F9;display:flex;align-items:center;justify-content:space-between}}
.card-hdr h3{{font-size:14px;font-weight:700;color:#1E293B}}
.card-body{{padding:20px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:left;padding:10px 16px;font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid #F1F5F9;background:#FAFAFA}}
td{{padding:13px 16px;border-bottom:1px solid #F8FAFC;color:#475569;vertical-align:middle}}
tr:last-child td{{border-bottom:none}}
tr:hover td{{background:#FAFAFA}}
.badge-active{{background:#DCFCE7;color:#16A34A;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700}}
.badge-suspended{{background:#FEE2E2;color:#DC2626;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700}}
.badge-blue{{background:#DBEAFE;color:#1D4ED8;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700}}
.btn-sm{{padding:5px 12px;border-radius:6px;font-size:11px;font-weight:700;border:none;cursor:pointer;font-family:inherit}}
.btn-danger{{background:#FEE2E2;color:#DC2626}}
.btn-warn{{background:#FEF3C7;color:#D97706}}
.btn-success{{background:#DCFCE7;color:#16A34A}}
.btn-primary{{background:#4338CA;color:#fff}}
.btn-blue{{background:#DBEAFE;color:#1D4ED8}}
label{{display:block;font-size:11px;font-weight:700;color:#64748B;margin-bottom:4px;text-transform:uppercase;letter-spacing:.4px}}
input,select,textarea{{width:100%;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:8px;padding:9px 12px;color:#1E293B;font-size:13px;outline:none;font-family:inherit;margin-bottom:12px}}
input:focus,select:focus,textarea:focus{{border-color:#6366F1;background:#fff}}
.form-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.form-grid3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}}
.page-hdr{{margin-bottom:22px}}
.page-hdr h1{{font-size:22px;font-weight:800;color:#1E293B}}
.page-hdr p{{font-size:13px;color:#94A3B8;margin-top:3px}}
.view-all{{font-size:12px;font-weight:600;color:#6366F1;text-decoration:none;background:#EEF2FF;padding:5px 12px;border-radius:20px}}
.empty-row td{{text-align:center;color:#94A3B8;padding:28px!important;font-size:13px}}
a.nav-logout{{display:flex;align-items:center;gap:10px;padding:10px 20px;text-decoration:none;font-size:13.5px;color:#EF4444;border-left:3px solid transparent}}
a.nav-view{{display:flex;align-items:center;gap:10px;padding:10px 20px;text-decoration:none;font-size:13.5px;color:#94A3B8;border-left:3px solid transparent}}
</style>
</head>
<body>
<div class="sidebar">
  <div class="s-brand">
    <div class="s-logo-row">
      <div class="s-logo">A</div>
      <div>
        <div class="s-title">ATLAS</div>
        <div class="s-badge">ADMIN PANEL</div>
      </div>
    </div>
  </div>
  <div class="s-section">Main</div>
  {nav_html}
  <div class="s-bottom">
    <a class="nav-logout" href="/admin/logout">&#128682; Log Out</a>
    <a class="nav-view" href="/" target="_blank">&#127968; View Site</a>
  </div>
</div>
<div class="main">
  <div class="topbar">
    <div class="topbar-title">{title}</div>
    <div class="topbar-right">
      <span class="topbar-date">{today}</span>
      <div class="admin-chip">
        <div class="admin-avatar">{ainit}</div>
        <span class="admin-name">{aname}</span>
      </div>
    </div>
  </div>
  <div class="content">{body}</div>
</div>
</body>
</html>"""

# ── DASHBOARD ──
def dashboard(admin):
    s = admin_db.get_stats()
    recent = admin_db.get_recent_tourists(5)
    stat_cards = [
        ("&#128100;","Tourists","active","#DBEAFE","#1D4ED8", s["total_tourists"], s["active_tourists"], "registered"),
        ("&#9992;","Flights","Listings","#DCFCE7","#16A34A", s["total_flights"], None, "in system"),
        ("&#127963;","Attractions","Listings","#FEF3C7","#D97706", s["total_spots"], None, "added"),
        ("&#127869;","Restaurants","Listings","#FCE7F3","#BE185D", s["total_rests"], None, "added"),
        ("&#129517;","Tour Guides","Listings","#EDE9FE","#7C3AED", s["total_guides"], None, "available"),
        ("&#128652;","Transport","Routes","#E0F2FE","#0369A1", s["total_transport"], None, "routes"),
    ]
    sc = ""
    for icon, label, badge, bg, color, val, sub_val, sub_label in stat_cards:
        sub = f'<div class="stat-sub">{sub_val} active</div>' if sub_val is not None else f'<div class="stat-sub">{val} {sub_label}</div>'
        sc += f'<div class="stat-card"><div class="stat-icon" style="color:{color}">{icon}</div><div class="stat-label">{label}</div><div class="stat-val">{val}</div>{sub}<span class="stat-badge" style="background:{bg};color:{color}">{badge}</span></div>'

    rows = ""
    for u in recent:
        status = u.get("status") or "active"
        badge = '<span class="badge-active">Active</span>' if status == "active" else '<span class="badge-suspended">Suspended</span>'
        rows += f'<tr><td style="font-weight:600;color:#1E293B">{u["fname"]} {u["lname"]}</td><td>{u["email"]}</td><td>{(u.get("created") or "")[:10]}</td><td>{badge}</td></tr>'
    if not rows:
        rows = '<tr class="empty-row"><td colspan="4">No tourists registered yet</td></tr>'

    body = f"""
    <div class="page-hdr"><h1>Dashboard</h1><p>Welcome back, {admin.get("fullname","Admin")}! Here is your overview.</p></div>
    <div class="stat-grid">{sc}</div>
    <div class="card">
      <div class="card-hdr"><h3>&#128100; Recent Tourists</h3><a class="view-all" href="/admin/tourists">View All</a></div>
      <table><thead><tr><th>Name</th><th>Email</th><th>Joined</th><th>Status</th></tr></thead>
      <tbody>{rows}</tbody></table>
    </div>"""
    return shell("Dashboard", body, "dashboard", admin)

# ── TOURISTS ──
def tourists_page(admin, msg=""):
    users = admin_db.get_all_tourists()
    alert = f'<div style="background:#DCFCE7;border:1px solid #BBF7D0;border-radius:8px;padding:10px 14px;color:#15803D;font-size:13px;margin-bottom:16px">{msg}</div>' if msg else ""
    rows = ""
    for u in users:
        status = u.get("status") or "active"
        badge = '<span class="badge-active">Active</span>' if status == "active" else '<span class="badge-suspended">Suspended</span>'
        toggle = f'<a href="/admin/tourists/suspend/{u["id"]}"><button class="btn-sm btn-warn" style="margin-right:4px">Suspend</button></a>' if status == "active" else f'<a href="/admin/tourists/activate/{u["id"]}"><button class="btn-sm btn-success" style="margin-right:4px">Activate</button></a>'
        rows += f'<tr><td style="font-weight:600;color:#1E293B">{u["fname"]} {u["lname"]}</td><td>{u["email"]}</td><td>{(u.get("created") or "")[:10]}</td><td>{badge}</td><td>{toggle}<a href="/admin/tourists/delete/{u["id"]}"><button class="btn-sm btn-danger">Delete</button></a></td></tr>'
    if not rows:
        rows = '<tr class="empty-row"><td colspan="5">No tourists registered yet</td></tr>'
    body = f"""
    <div class="page-hdr"><h1>&#128100; Tourists</h1><p>Manage tourist accounts</p></div>{alert}
    <div class="card">
      <div class="card-hdr"><h3>All Tourists ({len(users)})</h3></div>
      <table><thead><tr><th>Name</th><th>Email</th><th>Joined</th><th>Status</th><th>Actions</th></tr></thead>
      <tbody>{rows}</tbody></table>
    </div>"""
    return shell("Tourists", body, "tourists", admin)

def _city_opts(sel="Manila"):
    return "".join(f'<option {"selected" if c==sel else ""}>{c}</option>' for c in CITIES)

# ── FLIGHTS ──
def flights_page(admin, msg=""):
    flights = admin_db.get_flights()
    alert = f'<div style="background:#DCFCE7;border:1px solid #BBF7D0;border-radius:8px;padding:10px 14px;color:#15803D;font-size:13px;margin-bottom:16px">{msg}</div>' if msg else ""
    rows = "".join(f'<tr><td style="font-weight:600;color:#1E293B">{f["airline"]}</td><td>{f["origin"]} &#8594; {f["dest"]}</td><td>{f["dep_time"]}</td><td>{f["arr_time"]}</td><td style="color:#16A34A;font-weight:700">{f["price"]}</td><td><span class="badge-blue">{f["status"]}</span></td><td><a href="/admin/flights/delete/{f["id"]}"><button class="btn-sm btn-danger">Delete</button></a></td></tr>' for f in flights) or '<tr class="empty-row"><td colspan="7">No flights added yet</td></tr>'
    body = f"""
    <div class="page-hdr"><h1>&#9992; Flights</h1><p>Manage flight listings</p></div>{alert}
    <div class="card" style="margin-bottom:20px">
      <div class="card-hdr"><h3>&#43; Add Flight</h3></div>
      <div class="card-body">
        <form method="post" action="/admin/flights/add">
          <div class="form-grid">
            <div><label>Airline</label><input name="airline" placeholder="Philippine Airlines" required/></div>
            <div><label>Origin City</label><select name="origin">{_city_opts()}</select></div>
            <div><label>Destination City</label><select name="dest">{_city_opts("Baguio")}</select></div>
            <div><label>Departure Time</label><input name="dep_time" placeholder="06:00 AM" required/></div>
            <div><label>Arrival Time</label><input name="arr_time" placeholder="07:30 AM" required/></div>
            <div><label>Price</label><input name="price" placeholder="PHP 2,500" required/></div>
            <div><label>Status</label><select name="status"><option>Scheduled</option><option>On Time</option><option>Delayed</option><option>Cancelled</option></select></div>
          </div>
          <button class="btn-sm btn-primary" type="submit" style="padding:9px 22px;font-size:13px">&#43; Add Flight</button>
        </form>
      </div>
    </div>
    <div class="card">
      <div class="card-hdr"><h3>All Flights ({len(flights)})</h3></div>
      <table><thead><tr><th>Airline</th><th>Route</th><th>Departure</th><th>Arrival</th><th>Price</th><th>Status</th><th>Action</th></tr></thead>
      <tbody>{rows}</tbody></table>
    </div>"""
    return shell("Flights", body, "flights", admin)

# ── SPOTS ──
def spots_page(admin, msg=""):
    spots = admin_db.get_spots()
    alert = f'<div style="background:#DCFCE7;border:1px solid #BBF7D0;border-radius:8px;padding:10px 14px;color:#15803D;font-size:13px;margin-bottom:16px">{msg}</div>' if msg else ""
    rows = "".join(f'<tr><td style="font-weight:600;color:#1E293B">{s["name"]}</td><td>{s["city"]}</td><td><span class="badge-blue">{s["category"]}</span></td><td>{"&#9733;"*int(s["rating"])}</td><td>{s["entry"]}</td><td><a href="/admin/spots/delete/{s["id"]}"><button class="btn-sm btn-danger">Delete</button></a></td></tr>' for s in spots) or '<tr class="empty-row"><td colspan="6">No attractions added yet</td></tr>'
    body = f"""
    <div class="page-hdr"><h1>&#127963; Tourist Attractions</h1><p>Manage attraction listings</p></div>{alert}
    <div class="card" style="margin-bottom:20px">
      <div class="card-hdr"><h3>&#43; Add Attraction</h3></div>
      <div class="card-body">
        <form method="post" action="/admin/spots/add">
          <div class="form-grid">
            <div><label>Name</label><input name="name" placeholder="Intramuros" required/></div>
            <div><label>City</label><select name="city">{_city_opts()}</select></div>
            <div><label>Category</label><select name="category"><option>Historical</option><option>Nature</option><option>Heritage</option><option>Landmark</option><option>Park</option><option>Museum</option></select></div>
            <div><label>Type</label><input name="type" placeholder="Walled City"/></div>
            <div><label>Rating (1-5)</label><input name="rating" type="number" min="1" max="5" step="0.1" value="4.5"/></div>
            <div><label>Entry Fee</label><input name="entry" placeholder="Free / PHP 75"/></div>
            <div><label>Hours</label><input name="hours" placeholder="8AM-5PM"/></div>
            <div><label>Description</label><input name="desc" placeholder="Short description..."/></div>
          </div>
          <button class="btn-sm btn-primary" type="submit" style="padding:9px 22px;font-size:13px">&#43; Add Attraction</button>
        </form>
      </div>
    </div>
    <div class="card">
      <div class="card-hdr"><h3>All Attractions ({len(spots)})</h3></div>
      <table><thead><tr><th>Name</th><th>City</th><th>Category</th><th>Rating</th><th>Entry</th><th>Action</th></tr></thead>
      <tbody>{rows}</tbody></table>
    </div>"""
    return shell("Attractions", body, "spots", admin)

# ── RESTAURANTS ──
def restaurants_page(admin, msg=""):
    rests = admin_db.get_restaurants()
    alert = f'<div style="background:#DCFCE7;border:1px solid #BBF7D0;border-radius:8px;padding:10px 14px;color:#15803D;font-size:13px;margin-bottom:16px">{msg}</div>' if msg else ""
    rows = "".join(f'<tr><td style="font-weight:600;color:#1E293B">{r["name"]}</td><td>{r["city"]}</td><td>{r["cuisine"]}</td><td style="color:#16A34A;font-weight:700">{r["price"]}</td><td>{"&#9733;"*int(r["rating"])}</td><td><a href="/admin/restaurants/delete/{r["id"]}"><button class="btn-sm btn-danger">Delete</button></a></td></tr>' for r in rests) or '<tr class="empty-row"><td colspan="6">No restaurants added yet</td></tr>'
    body = f"""
    <div class="page-hdr"><h1>&#127869; Restaurants</h1><p>Manage restaurant listings</p></div>{alert}
    <div class="card" style="margin-bottom:20px">
      <div class="card-hdr"><h3>&#43; Add Restaurant</h3></div>
      <div class="card-body">
        <form method="post" action="/admin/restaurants/add">
          <div class="form-grid">
            <div><label>Name</label><input name="name" placeholder="Cafe Juanita" required/></div>
            <div><label>City</label><select name="city">{_city_opts()}</select></div>
            <div><label>Cuisine</label><input name="cuisine" placeholder="Filipino / Italian"/></div>
            <div><label>Price Range</label><input name="price" placeholder="PHP 200-500"/></div>
            <div><label>Rating (1-5)</label><input name="rating" type="number" min="1" max="5" step="0.1" value="4.0"/></div>
            <div><label>Hours</label><input name="hours" placeholder="10AM-10PM"/></div>
          </div>
          <button class="btn-sm btn-primary" type="submit" style="padding:9px 22px;font-size:13px">&#43; Add Restaurant</button>
        </form>
      </div>
    </div>
    <div class="card">
      <div class="card-hdr"><h3>All Restaurants ({len(rests)})</h3></div>
      <table><thead><tr><th>Name</th><th>City</th><th>Cuisine</th><th>Price</th><th>Rating</th><th>Action</th></tr></thead>
      <tbody>{rows}</tbody></table>
    </div>"""
    return shell("Restaurants", body, "restaurants", admin)

# ── GUIDES ──
def guides_page(admin, msg=""):
    guides = admin_db.get_guides()
    alert = f'<div style="background:#DCFCE7;border:1px solid #BBF7D0;border-radius:8px;padding:10px 14px;color:#15803D;font-size:13px;margin-bottom:16px">{msg}</div>' if msg else ""
    rows = "".join(f'<tr><td style="font-weight:600;color:#1E293B">{g["name"]}</td><td>{g["city"]}</td><td>{g["language"]}</td><td style="color:#7C3AED;font-weight:700">{g["rate"]}</td><td>{"&#9733;"*int(g["rating"])}</td><td><a href="/admin/guides/delete/{g["id"]}"><button class="btn-sm btn-danger">Delete</button></a></td></tr>' for g in guides) or '<tr class="empty-row"><td colspan="6">No tour guides added yet</td></tr>'
    body = f"""
    <div class="page-hdr"><h1>&#129517; Tour Guides</h1><p>Manage tour guide listings</p></div>{alert}
    <div class="card" style="margin-bottom:20px">
      <div class="card-hdr"><h3>&#43; Add Tour Guide</h3></div>
      <div class="card-body">
        <form method="post" action="/admin/guides/add">
          <div class="form-grid">
            <div><label>Full Name</label><input name="name" placeholder="Maria Santos" required/></div>
            <div><label>City</label><select name="city">{_city_opts()}</select></div>
            <div><label>Languages</label><input name="language" placeholder="English, Filipino"/></div>
            <div><label>Daily Rate</label><input name="rate" placeholder="PHP 1,500/day"/></div>
            <div><label>Rating (1-5)</label><input name="rating" type="number" min="1" max="5" step="0.1" value="4.5"/></div>
            <div><label>Bio</label><input name="bio" placeholder="Short bio..."/></div>
          </div>
          <button class="btn-sm btn-primary" type="submit" style="padding:9px 22px;font-size:13px">&#43; Add Guide</button>
        </form>
      </div>
    </div>
    <div class="card">
      <div class="card-hdr"><h3>All Tour Guides ({len(guides)})</h3></div>
      <table><thead><tr><th>Name</th><th>City</th><th>Languages</th><th>Rate</th><th>Rating</th><th>Action</th></tr></thead>
      <tbody>{rows}</tbody></table>
    </div>"""
    return shell("Tour Guides", body, "guides", admin)

# ── TRANSPORT ──
def transport_page(admin, msg=""):
    transport = admin_db.get_transport()
    alert = f'<div style="background:#DCFCE7;border:1px solid #BBF7D0;border-radius:8px;padding:10px 14px;color:#15803D;font-size:13px;margin-bottom:16px">{msg}</div>' if msg else ""
    rows = "".join(f'<tr><td style="font-weight:600;color:#1E293B">{t["route"]}</td><td><span class="badge-blue">{t["type"]}</span></td><td>{t["origin"]} &#8594; {t["dest"]}</td><td>{t["dep_time"]}</td><td style="color:#0369A1;font-weight:700">{t["fare"]}</td><td><a href="/admin/transport/delete/{t["id"]}"><button class="btn-sm btn-danger">Delete</button></a></td></tr>' for t in transport) or '<tr class="empty-row"><td colspan="6">No transport routes added yet</td></tr>'
    body = f"""
    <div class="page-hdr"><h1>&#128652; Transportation</h1><p>Manage transportation routes</p></div>{alert}
    <div class="card" style="margin-bottom:20px">
      <div class="card-hdr"><h3>&#43; Add Route</h3></div>
      <div class="card-body">
        <form method="post" action="/admin/transport/add">
          <div class="form-grid">
            <div><label>Route Name</label><input name="route" placeholder="Manila to Baguio Express" required/></div>
            <div><label>Type</label><select name="type"><option>Bus</option><option>Van</option><option>Train</option><option>Ferry</option><option>Jeepney</option></select></div>
            <div><label>Origin</label><select name="origin">{_city_opts()}</select></div>
            <div><label>Destination</label><select name="dest">{_city_opts("Baguio")}</select></div>
            <div><label>Departure Time</label><input name="dep_time" placeholder="6:00 AM" required/></div>
            <div><label>Fare</label><input name="fare" placeholder="PHP 450"/></div>
          </div>
          <button class="btn-sm btn-primary" type="submit" style="padding:9px 22px;font-size:13px">&#43; Add Route</button>
        </form>
      </div>
    </div>
    <div class="card">
      <div class="card-hdr"><h3>All Routes ({len(transport)})</h3></div>
      <table><thead><tr><th>Route</th><th>Type</th><th>From &#8594; To</th><th>Departure</th><th>Fare</th><th>Action</th></tr></thead>
      <tbody>{rows}</tbody></table>
    </div>"""
    return shell("Transportation", body, "transport", admin)

# ── PROFILE ──
def profile_page(admin, msg="", error=""):
    alert = f'<div style="background:#DCFCE7;border:1px solid #BBF7D0;border-radius:8px;padding:10px 14px;color:#15803D;font-size:13px;margin-bottom:16px">{msg}</div>' if msg else ""
    err   = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:8px;padding:10px 14px;color:#DC2626;font-size:13px;margin-bottom:16px">{error}</div>' if error else ""
    ainit = (admin.get("fullname","A") or "A")[0].upper()
    body = f"""
    <div class="page-hdr"><h1>&#128100; Admin Profile</h1><p>Update your account information</p></div>
    {alert}{err}
    <div style="display:grid;grid-template-columns:280px 1fr;gap:20px">
      <div class="card">
        <div class="card-body" style="text-align:center;padding:32px 20px">
          <div style="width:80px;height:80px;background:linear-gradient(135deg,#0038A8,#CE1126);border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:32px;margin:0 auto 16px">{ainit}</div>
          <div style="font-size:18px;font-weight:800;color:#1E293B">{admin.get("fullname","Admin")}</div>
          <div style="font-size:13px;color:#94A3B8;margin-top:4px">{admin.get("email","")}</div>
          <div style="margin-top:12px"><span class="badge-blue">Super Admin</span></div>
          <div style="font-size:11px;color:#CBD5E1;margin-top:16px">Member since {(admin.get("created","") or "")[:10]}</div>
        </div>
      </div>
      <div class="card">
        <div class="card-hdr"><h3>Edit Profile</h3></div>
        <div class="card-body">
          <form method="post" action="/admin/profile/update">
            <label>Full Name</label>
            <input name="fullname" value="{admin.get("fullname","")}" placeholder="ATLAS Administrator" required/>
            <label>Email Address</label>
            <input name="email" type="email" value="{admin.get("email","")}" placeholder="admin@atlas.ph" required/>
            <div style="height:1px;background:#F1F5F9;margin:8px 0 16px"></div>
            <div style="font-size:12px;font-weight:700;color:#94A3B8;margin-bottom:12px;text-transform:uppercase;letter-spacing:.4px">Change Password (leave blank to keep current)</div>
            <label>New Password</label>
            <input name="new_password" type="password" placeholder="Min. 8 characters"/>
            <label>Confirm New Password</label>
            <input name="confirm_password" type="password" placeholder="Repeat new password"/>
            <button class="btn-sm btn-primary" type="submit" style="padding:10px 24px;font-size:13px">Save Changes</button>
          </form>
        </div>
      </div>
    </div>"""
    return shell("Admin Profile", body, "profile", admin)
