import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import admin_db

CITIES = ["Manila","Baguio","Ilocos Norte","Vigan","Batangas","Tagaytay"]

def shell(title, body, active):
    nav_items = [
        ("dashboard","&#9732;","Dashboard"),
        ("users","&#128100;","Users"),
        ("spots","&#127963;","Attractions"),
        ("restaurants","&#127869;","Restaurants"),
    ]
    nav_html = ""
    for key, icon, label in nav_items:
        a = "background:#1E3A5F;color:#fff;" if active==key else "color:#94A3B8;"
        nav_html += f'<a href="/admin/{key}" style="display:flex;align-items:center;gap:10px;padding:10px 16px;border-radius:8px;text-decoration:none;font-size:13px;font-weight:600;{a}margin-bottom:2px">{icon} {label}</a>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title} - ATLAS Admin</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',sans-serif;background:#0F172A;color:#F1F5F9;min-height:100vh;display:flex}}
.sidebar{{width:220px;flex-shrink:0;background:#1E293B;border-right:1px solid #334155;display:flex;flex-direction:column;padding:24px 14px}}
.s-brand{{display:flex;align-items:center;gap:8px;padding:0 6px;margin-bottom:30px}}
.s-logo{{width:32px;height:32px;background:linear-gradient(135deg,#0038A8,#CE1126);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:15px}}
.s-title{{font-weight:900;font-size:16px;color:#fff}}
.s-badge{{font-size:9px;color:#F87171;font-weight:700;background:rgba(239,68,68,.15);padding:1px 7px;border-radius:10px;border:1px solid rgba(239,68,68,.25)}}
.s-section{{font-size:10px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:.8px;padding:0 6px;margin:14px 0 6px}}
.s-bottom{{margin-top:auto}}
a.logout{{display:flex;align-items:center;gap:10px;padding:10px 16px;border-radius:8px;text-decoration:none;font-size:13px;font-weight:600;color:#F87171;margin-bottom:2px}}
.main{{flex:1;overflow-y:auto;padding:32px}}
.page-hdr{{margin-bottom:28px}}
.page-hdr h1{{font-size:24px;font-weight:800;color:#F1F5F9}}
.page-hdr p{{font-size:13px;color:#64748B;margin-top:4px}}
.stat-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px;margin-bottom:28px}}
.stat{{background:#1E293B;border:1px solid #334155;border-radius:12px;padding:20px 18px}}
.stat-val{{font-size:28px;font-weight:900;color:#F1F5F9;line-height:1}}
.stat-lbl{{font-size:11px;color:#64748B;margin-top:4px;font-weight:600}}
.stat-icon{{font-size:22px;margin-bottom:8px}}
.card{{background:#1E293B;border:1px solid #334155;border-radius:12px;overflow:hidden;margin-bottom:22px}}
.card-hdr{{padding:14px 20px;border-bottom:1px solid #334155;display:flex;align-items:center;justify-content:space-between}}
.card-hdr h3{{font-size:14px;font-weight:700;color:#F1F5F9}}
.card-body{{padding:20px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:left;padding:10px 14px;font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid #334155}}
td{{padding:12px 14px;border-bottom:1px solid #1E293B;color:#CBD5E1;vertical-align:middle}}
tr:last-child td{{border-bottom:none}}
tr:hover td{{background:rgba(255,255,255,.02)}}
.badge-active{{background:rgba(34,197,94,.15);color:#4ADE80;border:1px solid rgba(34,197,94,.3);padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700}}
.badge-suspended{{background:rgba(239,68,68,.15);color:#F87171;border:1px solid rgba(239,68,68,.3);padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700}}
.btn-sm{{padding:5px 12px;border-radius:6px;font-size:11px;font-weight:700;border:none;cursor:pointer;font-family:inherit}}
.btn-danger{{background:rgba(239,68,68,.15);color:#F87171;border:1px solid rgba(239,68,68,.3)}}
.btn-warn{{background:rgba(245,158,11,.15);color:#FCD34D;border:1px solid rgba(245,158,11,.3)}}
.btn-success{{background:rgba(34,197,94,.15);color:#4ADE80;border:1px solid rgba(34,197,94,.3)}}
.btn-primary{{background:#1D4ED8;color:#fff;border:none}}
label{{display:block;font-size:11px;font-weight:700;color:#94A3B8;margin-bottom:4px;text-transform:uppercase;letter-spacing:.4px}}
input,select,textarea{{width:100%;background:#0F172A;border:1.5px solid #334155;border-radius:7px;padding:9px 12px;color:#F1F5F9;font-size:13px;outline:none;font-family:inherit;margin-bottom:12px}}
input:focus,select:focus{{border-color:#3B82F6}}
.form-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.visit-bar-wrap{{background:#0F172A;border-radius:6px;height:10px;overflow:hidden;margin-top:4px}}
.visit-bar{{height:100%;background:linear-gradient(90deg,#0038A8,#3B82F6);border-radius:6px;transition:width .4s}}
</style>
</head>
<body>
<div class="sidebar">
  <div class="s-brand">
    <div class="s-logo">A</div>
    <div>
      <div class="s-title">ATLAS</div>
      <div class="s-badge">ADMIN</div>
    </div>
  </div>
  <div class="s-section">Main Menu</div>
  {nav_html}
  <div class="s-bottom">
    <div class="s-section">Account</div>
    <a class="logout" href="/admin/logout">&#128682; Sign Out</a>
    <a href="/" style="display:flex;align-items:center;gap:10px;padding:10px 16px;border-radius:8px;text-decoration:none;font-size:13px;font-weight:600;color:#64748B">&#127968; View Site</a>
  </div>
</div>
<div class="main">{body}</div>
</body>
</html>"""

# ── DASHBOARD ──
def dashboard():
    s = admin_db.get_stats()
    visits = admin_db.get_visit_stats()
    top_v = visits[:6] if visits else []
    max_v = max((v["cnt"] for v in top_v), default=1)
    stat_cards = [
        ("&#128100;", s["total_users"],  "Total Users",       "#3B82F6"),
        ("&#9989;",   s["active_users"], "Active Users",      "#22C55E"),
        ("&#128683;", s["suspended"],    "Suspended",         "#EF4444"),
        ("&#127963;", s["total_spots"],  "Attractions Added", "#F59E0B"),
        ("&#127869;", s["total_rests"],  "Restaurants Added", "#A855F7"),
        ("&#128065;", s["total_visits"], "Total Page Views",  "#06B6D4"),
    ]
    sc = "".join(f'<div class="stat"><div class="stat-icon" style="color:{c}">{i}</div><div class="stat-val">{v}</div><div class="stat-lbl">{l}</div></div>' for i,v,l,c in stat_cards)
    def vrow(v):
        pct = int(v["cnt"]/max_v*100)
        return f'<tr><td style="color:#F1F5F9;font-weight:600">{v["page"]}</td><td style="width:60%"><div class="visit-bar-wrap"><div class="visit-bar" style="width:{pct}%"></div></div></td><td style="color:#94A3B8;text-align:right">{v["cnt"]}</td></tr>'
    vr = "".join(vrow(v) for v in top_v) or '<tr><td colspan="3" style="color:#475569;text-align:center;padding:20px">No visits recorded yet</td></tr>'
    body = f"""
    <div class="page-hdr"><h1>&#9732; Dashboard</h1><p>Overview of ATLAS activity</p></div>
    <div class="stat-grid">{sc}</div>
    <div class="card">
      <div class="card-hdr"><h3>&#128065; Page Views by Route</h3></div>
      <div class="card-body"><table><thead><tr><th>Page</th><th>Traffic</th><th>Visits</th></tr></thead><tbody>{vr}</tbody></table></div>
    </div>"""
    return shell("Dashboard", body, "dashboard")

# ── USERS ──
def users_page(msg=""):
    users = admin_db.get_all_users()
    alert = f'<div style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.3);border-radius:8px;padding:10px 14px;color:#4ADE80;font-size:13px;margin-bottom:16px">{msg}</div>' if msg else ""
    rows = ""
    for u in users:
        status = u.get("status") or "active"
        badge = f'<span class="badge-active">Active</span>' if status == "active" else f'<span class="badge-suspended">Suspended</span>'
        suspend_btn = f'<a href="/admin/users/suspend/{u["id"]}"><button class="btn-sm btn-warn" style="margin-right:4px">Suspend</button></a>' if status == "active" else f'<a href="/admin/users/activate/{u["id"]}"><button class="btn-sm btn-success" style="margin-right:4px">Activate</button></a>'
        rows += f'<tr><td style="color:#F1F5F9;font-weight:600">{u["fname"]} {u["lname"]}</td><td>{u["email"]}</td><td>{u.get("created","")[:10]}</td><td>{badge}</td><td>{suspend_btn}<a href="/admin/users/delete/{u["id"]}"><button class="btn-sm btn-danger" onclick="return confirm(\'Delete this user?\')">Delete</button></a></td></tr>'
    empty = '<tr><td colspan="5" style="color:#475569;text-align:center;padding:24px">No users registered yet</td></tr>' if not rows else ""
    body = f"""
    <div class="page-hdr"><h1>&#128100; User Management</h1><p>View, suspend, or delete customer accounts</p></div>
    {alert}
    <div class="card">
      <div class="card-hdr"><h3>All Registered Users ({len(users)})</h3></div>
      <div style="overflow-x:auto">
        <table><thead><tr><th>Name</th><th>Email</th><th>Joined</th><th>Status</th><th>Actions</th></tr></thead>
        <tbody>{rows}{empty}</tbody></table>
      </div>
    </div>"""
    return shell("Users", body, "users")

# ── SPOTS ──
def spots_page(msg="", error=""):
    spots = admin_db.get_spots()
    alert = f'<div style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.3);border-radius:8px;padding:10px 14px;color:#4ADE80;font-size:13px;margin-bottom:16px">{msg}</div>' if msg else ""
    err   = f'<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;padding:10px 14px;color:#F87171;font-size:13px;margin-bottom:16px">{error}</div>' if error else ""
    city_opts = "".join(f"<option>{c}</option>" for c in ["Manila","Baguio","Ilocos Norte","Vigan","Batangas","Tagaytay"])
    rows = "".join(f'<tr><td style="color:#F1F5F9;font-weight:600">{s["name"]}</td><td>{s["city"]}</td><td>{s["category"]}</td><td>{"&#9733;"*int(s["rating"])}</td><td>{s["entry"]}</td><td><a href="/admin/spots/delete/{s["id"]}"><button class="btn-sm btn-danger">Delete</button></a></td></tr>' for s in spots) or '<tr><td colspan="6" style="color:#475569;text-align:center;padding:20px">No attractions added yet</td></tr>'
    body = f"""
    <div class="page-hdr"><h1>&#127963; Manage Attractions</h1><p>Add or remove tourist attraction listings</p></div>
    {alert}{err}
    <div class="card" style="margin-bottom:22px">
      <div class="card-hdr"><h3>&#43; Add New Attraction</h3></div>
      <div class="card-body">
        <form method="post" action="/admin/spots/add">
          <div class="form-grid">
            <div><label>Name</label><input name="name" placeholder="Intramuros" required/></div>
            <div><label>City</label><select name="city">{city_opts}</select></div>
            <div><label>Category</label><select name="category"><option>Historical</option><option>Nature</option><option>Heritage</option><option>Landmark</option><option>Park</option><option>Museum</option></select></div>
            <div><label>Type</label><input name="type" placeholder="e.g. Walled City" required/></div>
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
      <div class="card-hdr"><h3>All Custom Attractions ({len(spots)})</h3></div>
      <div style="overflow-x:auto"><table><thead><tr><th>Name</th><th>City</th><th>Category</th><th>Rating</th><th>Entry</th><th>Action</th></tr></thead><tbody>{rows}</tbody></table></div>
    </div>"""
    return shell("Attractions", body, "spots")

# ── RESTAURANTS ──
def restaurants_page(msg="", error=""):
    rests = admin_db.get_restaurants()
    alert = f'<div style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.3);border-radius:8px;padding:10px 14px;color:#4ADE80;font-size:13px;margin-bottom:16px">{msg}</div>' if msg else ""
    err   = f'<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;padding:10px 14px;color:#F87171;font-size:13px;margin-bottom:16px">{error}</div>' if error else ""
    city_opts = "".join(f"<option>{c}</option>" for c in ["Manila","Baguio","Ilocos Norte","Vigan","Batangas","Tagaytay"])
    rows = "".join(f'<tr><td style="color:#F1F5F9;font-weight:600">{r["name"]}</td><td>{r["city"]}</td><td>{r["cuisine"]}</td><td>{r["price"]}</td><td>{"&#9733;"*int(r["rating"])}</td><td><a href="/admin/restaurants/delete/{r["id"]}"><button class="btn-sm btn-danger">Delete</button></a></td></tr>' for r in rests) or '<tr><td colspan="6" style="color:#475569;text-align:center;padding:20px">No restaurants added yet</td></tr>'
    body = f"""
    <div class="page-hdr"><h1>&#127869; Manage Restaurants</h1><p>Add or remove restaurant listings</p></div>
    {alert}{err}
    <div class="card" style="margin-bottom:22px">
      <div class="card-hdr"><h3>&#43; Add New Restaurant</h3></div>
      <div class="card-body">
        <form method="post" action="/admin/restaurants/add">
          <div class="form-grid">
            <div><label>Restaurant Name</label><input name="name" placeholder="Cafe Juanita" required/></div>
            <div><label>City</label><select name="city">{city_opts}</select></div>
            <div><label>Cuisine Type</label><input name="cuisine" placeholder="Filipino / Italian..."/></div>
            <div><label>Price Range</label><input name="price" placeholder="PHP 200-500"/></div>
            <div><label>Rating (1-5)</label><input name="rating" type="number" min="1" max="5" step="0.1" value="4.0"/></div>
            <div><label>Hours</label><input name="hours" placeholder="10AM-10PM"/></div>
          </div>
          <button class="btn-sm btn-primary" type="submit" style="padding:9px 22px;font-size:13px">&#43; Add Restaurant</button>
        </form>
      </div>
    </div>
    <div class="card">
      <div class="card-hdr"><h3>All Custom Restaurants ({len(rests)})</h3></div>
      <div style="overflow-x:auto"><table><thead><tr><th>Name</th><th>City</th><th>Cuisine</th><th>Price</th><th>Rating</th><th>Action</th></tr></thead><tbody>{rows}</tbody></table></div>
    </div>"""
    return shell("Restaurants", body, "restaurants")
