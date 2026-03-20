import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guide_template import build_guide_shell
import guide_db

CITIES = ["Manila","Baguio","Tagaytay","Vigan","Ilocos Norte","Batangas","Albay","Pangasinan","Bataan"]
DAYS   = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
STATUS_COLORS = {"pending":"#D97706","accepted":"#059669","rejected":"#DC2626","cancelled":"#6B7280","rescheduled":"#2563EB"}
STATUS_BG     = {"pending":"#FFFBEB","accepted":"#ECFDF5","rejected":"#FEF2F2","cancelled":"#F9FAFB","rescheduled":"#EFF6FF"}

def render_login(error="", success=""):
    err = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:10px;padding:10px 14px;color:#DC2626;font-size:13px;margin-bottom:18px">&#9888; {error}</div>' if error else ""
    suc = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:10px;padding:10px 14px;color:#065F46;font-size:13px;margin-bottom:18px">&#10003; {success}</div>' if success else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Guide Login - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{min-height:100vh;display:flex;flex-direction:row;font-family:'Segoe UI',sans-serif;}}
.split-left{{width:55%;background:linear-gradient(160deg,#3B0764 0%,#4C1D95 50%,#1e1b4b 100%);position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 48px;overflow:hidden;min-height:100vh}}
.blob1{{position:absolute;width:420px;height:420px;border-radius:50%;background:rgba(255,255,255,.06);top:-100px;left:-80px}}
.blob2{{position:absolute;width:280px;height:280px;border-radius:50%;background:rgba(255,255,255,.04);bottom:-60px;right:-40px}}
.split-right{{width:45%;flex-shrink:0;background:linear-gradient(180deg,#F8F4FF 0%,#fff 40%);display:flex;flex-direction:column;justify-content:center;padding:52px 48px;min-height:100vh;overflow-y:auto}}
.tab-row{{display:flex;background:#F3F4F6;border-radius:12px;padding:4px;margin-bottom:32px}}
.tab{{flex:1;padding:10px;text-align:center;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none;color:#6B7280}}
.tab.active{{background:#fff;color:#1F2937;box-shadow:0 1px 4px rgba(0,0,0,.1)}}
.field{{margin-bottom:18px}}
.field label{{display:block;font-size:12px;font-weight:700;color:#374151;margin-bottom:6px;text-transform:uppercase;letter-spacing:.5px}}
.field input{{width:100%;padding:13px 16px;border:1.5px solid #E5E7EB;border-radius:10px;font-size:14px;color:#1F2937;outline:none;background:#F9FAFB}}
.field input:focus{{border-color:#6B21A8;background:#fff;box-shadow:0 0 0 3px rgba(107,33,168,.08)}}
.submit-btn{{width:100%;padding:14px;background:linear-gradient(135deg,#6B21A8,#4C1D95);color:#fff;border:none;border-radius:12px;font-size:15px;font-weight:700;cursor:pointer;margin-top:4px}}
.back-link{{position:fixed;top:20px;left:20px;display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.15);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.3);color:#fff;text-decoration:none;padding:8px 16px;border-radius:30px;font-size:13px;font-weight:600;z-index:999}}
@media(max-width:700px){{.split-left{{display:none}}.split-right{{width:100%}}}}
</style>
</head>
<body>
<a href="/" class="back-link">&#8592; Tourist Site</a>
<div class="split-left">
  <div class="blob1"></div><div class="blob2"></div>
  <div style="position:relative;z-index:2;text-align:center;color:#fff">
    <div style="font-size:72px;margin-bottom:20px">&#129517;</div>
    <div style="font-size:34px;font-weight:900;line-height:1.2;margin-bottom:14px">ATLAS<br/>Guide Portal</div>
    <div style="font-size:15px;opacity:.8;line-height:1.8;margin-bottom:32px;max-width:300px">Manage your tours, bookings and packages — all in one place.</div>
    <div style="display:flex;flex-direction:column;gap:10px;font-size:14px;opacity:.9;text-align:left">
      <div style="display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.1);padding:11px 16px;border-radius:12px"><span>&#128196;</span> Create & manage tour packages</div>
      <div style="display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.1);padding:11px 16px;border-radius:12px"><span>&#128197;</span> Accept or reject bookings</div>
      <div style="display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.1);padding:11px 16px;border-radius:12px"><span>&#128336;</span> Set your weekly availability</div>
      <div style="display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.1);padding:11px 16px;border-radius:12px"><span>&#11088;</span> View ratings & feedback</div>
    </div>
  </div>
</div>
<div class="split-right">
  <div style="margin-bottom:28px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
      <img src="/ATLAS_LOGO.jpg" alt="ATLAS" style="width:32px;height:32px;border-radius:50%;object-fit:cover;flex-shrink:0"/>
      <span style="font-weight:900;font-size:18px;color:#1F2937">Guide Portal</span>
    </div>
    <div style="font-size:13px;color:#6B7280">ATLAS Tour Guide Management</div>
  </div>
  <div class="tab-row">
    <a href="/guide" class="tab active">Log In</a>
    <a href="/guide/register" class="tab">Register</a>
  </div>
  <div style="font-size:22px;font-weight:800;color:#1F2937;margin-bottom:6px">Welcome back!</div>
  <div style="font-size:14px;color:#6B7280;margin-bottom:24px">Sign in to your guide account</div>
  {err}{suc}
  <form method="post" action="/guide/login">
    <div class="field"><label>Email Address</label><input type="email" name="email" placeholder="yourname@email.com" required/></div>
    <div class="field"><label>Password</label><input type="password" name="password" placeholder="Enter your password" required/></div>
    <button class="submit-btn" type="submit">Log In &#8594;</button>
  </form>
  <div style="text-align:center;margin-top:24px;font-size:13px;color:#6B7280">
    Don't have an account? <a href="/guide/register" style="color:#6B21A8;font-weight:700">Register as Guide</a>
  </div>
</div>
</body></html>"""

def render_register(error=""):
    err = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:10px;padding:10px 14px;color:#DC2626;font-size:13px;margin-bottom:18px">&#9888; {error}</div>' if error else ""
    city_opts = "".join(f'<option>{c}</option>' for c in CITIES)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Guide Register - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{min-height:100vh;display:flex;flex-direction:row;font-family:'Segoe UI',sans-serif;}}
.split-left{{width:55%;background:linear-gradient(160deg,#4C1D95 0%,#6B21A8 50%,#3B0764 100%);position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 48px;overflow:hidden;min-height:100vh}}
.blob1{{position:absolute;width:400px;height:400px;border-radius:50%;background:rgba(255,255,255,.06);top:-80px;right:-80px}}
.blob2{{position:absolute;width:280px;height:280px;border-radius:50%;background:rgba(255,255,255,.04);bottom:-60px;left:-40px}}
.split-right{{width:45%;flex-shrink:0;background:linear-gradient(180deg,#F8F4FF 0%,#fff 40%);display:flex;flex-direction:column;justify-content:center;padding:48px;min-height:100vh;overflow-y:auto}}
.tab-row{{display:flex;background:#F3F4F6;border-radius:12px;padding:4px;margin-bottom:28px}}
.tab{{flex:1;padding:10px;text-align:center;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none;color:#6B7280}}
.tab.active{{background:#fff;color:#1F2937;box-shadow:0 1px 4px rgba(0,0,0,.1)}}
.field{{margin-bottom:16px}}
.field label{{display:block;font-size:12px;font-weight:700;color:#374151;margin-bottom:6px;text-transform:uppercase;letter-spacing:.5px}}
.field input,.field select{{width:100%;padding:13px 16px;border:1.5px solid #E5E7EB;border-radius:10px;font-size:14px;color:#1F2937;outline:none;background:#F9FAFB}}
.field input:focus,.field select:focus{{border-color:#6B21A8;background:#fff;box-shadow:0 0 0 3px rgba(107,33,168,.08)}}
.submit-btn{{width:100%;padding:14px;background:linear-gradient(135deg,#6B21A8,#4C1D95);color:#fff;border:none;border-radius:12px;font-size:15px;font-weight:700;cursor:pointer;margin-top:4px}}
.back-link{{position:fixed;top:20px;left:20px;display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.15);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.3);color:#fff;text-decoration:none;padding:8px 16px;border-radius:30px;font-size:13px;font-weight:600;z-index:999}}
@media(max-width:700px){{.split-left{{display:none}}.split-right{{width:100%}}}}
</style>
</head>
<body>
<a href="/" class="back-link">&#8592; Tourist Site</a>
<div class="split-left">
  <div class="blob1"></div><div class="blob2"></div>
  <div style="position:relative;z-index:2;text-align:center;color:#fff">
    <div style="font-size:72px;margin-bottom:20px">&#127758;</div>
    <div style="font-size:34px;font-weight:900;line-height:1.2;margin-bottom:14px">Join ATLAS<br/>as a Guide!</div>
    <div style="font-size:15px;opacity:.8;line-height:1.8;margin-bottom:32px;max-width:300px">Share your knowledge of Luzon and earn income helping tourists discover the Philippines.</div>
    <div style="display:flex;flex-direction:column;gap:12px;font-size:14px;opacity:.9;text-align:left">
      <div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.1);padding:12px 16px;border-radius:12px"><span style="font-size:22px">&#128184;</span><div><div style="font-weight:700">Earn Income</div><div style="font-size:12px;opacity:.8">Set your own rates and packages</div></div></div>
      <div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.1);padding:12px 16px;border-radius:12px"><span style="font-size:22px">&#128101;</span><div><div style="font-weight:700">Meet Tourists</div><div style="font-size:12px;opacity:.8">Connect with travelers from everywhere</div></div></div>
      <div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.1);padding:12px 16px;border-radius:12px"><span style="font-size:22px">&#11088;</span><div><div style="font-weight:700">Build Your Reputation</div><div style="font-size:12px;opacity:.8">Collect ratings and grow your business</div></div></div>
    </div>
  </div>
</div>
<div class="split-right">
  <div style="margin-bottom:24px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
      <img src="/ATLAS_LOGO.jpg" alt="ATLAS" style="width:32px;height:32px;border-radius:50%;object-fit:cover;flex-shrink:0"/>
      <span style="font-weight:900;font-size:18px;color:#1F2937">Guide Portal</span>
    </div>
    <div style="font-size:13px;color:#6B7280">ATLAS Tour Guide Management</div>
  </div>
  <div class="tab-row">
    <a href="/guide" class="tab">Log In</a>
    <a href="/guide/register" class="tab active">Register</a>
  </div>
  <div style="font-size:22px;font-weight:800;color:#1F2937;margin-bottom:6px">Create Guide Account</div>
  <div style="font-size:14px;color:#6B7280;margin-bottom:22px">Join our network of verified local guides</div>
  {err}
  <form method="post" action="/guide/register">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
      <div class="field"><label>First Name *</label><input name="fname" placeholder="Juan" required/></div>
      <div class="field"><label>Last Name *</label><input name="lname" placeholder="Dela Cruz" required/></div>
    </div>
    <div class="field"><label>Email Address *</label><input type="email" name="email" placeholder="juan@email.com" required/></div>
    <div class="field"><label>Phone Number *</label><input name="phone" placeholder="09XX-XXX-XXXX" required/></div>
    <div class="field"><label>Your City / Area *</label><select name="city">{city_opts}</select></div>
    <div class="field"><label>Password * (min 6 characters)</label><input type="password" name="password" required/></div>
    <div class="field"><label>Confirm Password *</label><input type="password" name="password2" required/></div>
    <button class="submit-btn" type="submit">Create Account &#8594;</button>
  </form>
  <div style="text-align:center;margin-top:20px;font-size:13px;color:#6B7280">
    Already have an account? <a href="/guide" style="color:#6B21A8;font-weight:700">Log In</a>
  </div>
</div>
</body></html>"""

# ─────────────────────── DASHBOARD ───────────────────────
def render_dashboard(guide, msg="", err=""):
    gid = guide["id"]
    packages = guide_db.get_packages(gid)
    bookings = guide_db.get_bookings(gid)
    ratings  = guide_db.get_ratings(gid)
    avg_rating, rating_count = guide_db.get_avg_rating(gid)
    today = datetime.date.today().isoformat()
    pending  = [b for b in bookings if b["status"] == "pending"]
    upcoming = [b for b in bookings if b["status"] == "accepted" and b["tour_date"] >= today]

    alert = ""
    if msg: alert = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:10px;padding:12px 16px;color:#065F46;font-size:13px;margin-bottom:20px;display:flex;align-items:center;gap:8px">&#10003; {msg}</div>'
    if err: alert = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:10px;padding:12px 16px;color:#DC2626;font-size:13px;margin-bottom:20px;display:flex;align-items:center;gap:8px">&#9888; {err}</div>'

    # Stat cards
    stats = f"""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px">
      <div class="g-stat" style="background:linear-gradient(135deg,#6B21A8,#7C3AED)"><div style="font-size:32px;font-weight:900">{len(packages)}</div><div style="font-size:12px;opacity:.85;margin-top:4px">Packages</div></div>
      <div class="g-stat" style="background:linear-gradient(135deg,#D97706,#F59E0B)"><div style="font-size:32px;font-weight:900">{len(pending)}</div><div style="font-size:12px;opacity:.85;margin-top:4px">Pending</div></div>
      <div class="g-stat" style="background:linear-gradient(135deg,#059669,#10B981)"><div style="font-size:32px;font-weight:900">{len(upcoming)}</div><div style="font-size:12px;opacity:.85;margin-top:4px">Upcoming</div></div>
      <div class="g-stat" style="background:linear-gradient(135deg,#DC2626,#EF4444)"><div style="font-size:32px;font-weight:900">{avg_rating}&#9733;</div><div style="font-size:12px;opacity:.85;margin-top:4px">Avg Rating</div></div>
    </div>"""

    # Pending requests
    pending_html = ""
    if pending:
        rows = "".join(f"""
        <div style="border:1px solid #FDE68A;border-radius:10px;padding:14px 16px;background:#FFFBEB;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">
          <div>
            <div style="font-weight:700;color:#1F2937;font-size:15px">{b["tourist_name"]}</div>
            <div style="font-size:12px;color:#6B7280;margin-top:3px">&#128197; {b["tour_date"]} &bull; {b["pax"]} pax &bull; {b["package_title"] or "Custom Tour"}</div>
            {"" if not b["notes"] else f'<div style="font-size:12px;color:#92400E;margin-top:4px;font-style:italic">"{b["notes"]}"</div>'}
          </div>
          <div style="display:flex;gap:8px">
            <form method="post" action="/guide/dashboard?section=dashboard"><input type="hidden" name="action" value="accept_booking"/><input type="hidden" name="booking_id" value="{b["id"]}"/><button class="g-btn" style="background:#059669;color:#fff;padding:8px 16px;font-size:13px">&#10003; Accept</button></form>
            <form method="post" action="/guide/dashboard?section=dashboard"><input type="hidden" name="action" value="reject_booking"/><input type="hidden" name="booking_id" value="{b["id"]}"/><button class="g-btn" style="background:#DC2626;color:#fff;padding:8px 16px;font-size:13px">&#10007; Reject</button></form>
          </div>
        </div>""" for b in pending)
        pending_html = f'<div class="g-card"><div class="g-card-hdr" style="background:#D97706">&#9888; Pending Booking Requests ({len(pending)})</div><div class="g-card-body">{rows}</div></div>'

    # Upcoming bookings table
    upcoming_html = ""
    if upcoming:
        rows = "".join(f'<tr style="border-bottom:1px solid #F3F4F6"><td style="padding:11px 14px;font-weight:600">{b["tourist_name"]}</td><td style="padding:11px 14px;color:#6B7280">{b["tour_date"]}</td><td style="padding:11px 14px;color:#6B7280">{b["package_title"] or "Custom"}</td><td style="padding:11px 14px;color:#6B7280">{b["pax"]} pax</td></tr>' for b in upcoming[:6])
        upcoming_html = f'<div class="g-card"><div class="g-card-hdr" style="background:#2563EB">&#128197; Upcoming Bookings</div><div class="g-card-body" style="padding:0"><table style="width:100%;border-collapse:collapse"><thead><tr style="background:#F8FAFC"><th style="padding:11px 14px;text-align:left;font-size:12px;color:#6B7280;font-weight:600">Tourist</th><th style="padding:11px 14px;text-align:left;font-size:12px;color:#6B7280;font-weight:600">Date</th><th style="padding:11px 14px;text-align:left;font-size:12px;color:#6B7280;font-weight:600">Package</th><th style="padding:11px 14px;text-align:left;font-size:12px;color:#6B7280;font-weight:600">Pax</th></tr></thead><tbody>{rows}</tbody></table></div></div>'

    body = f"""
    <div style="margin-bottom:24px">
      <div style="font-size:24px;font-weight:900;color:#1F2937">Dashboard</div>
      <div style="font-size:14px;color:#6B7280">Welcome back, {guide["fname"]}! &#128075;</div>
    </div>
    {alert}{stats}{pending_html}{upcoming_html}
    {"" if upcoming_html or pending_html else '<div class="g-card"><div class="g-card-body" style="text-align:center;padding:40px;color:#9CA3AF"><div style="font-size:48px;margin-bottom:12px">&#128197;</div><div style="font-weight:700;font-size:16px">No bookings yet</div><div style="font-size:13px;margin-top:6px">Add packages to start receiving bookings!</div></div></div>'}"""
    return build_guide_shell("Dashboard", body, "dashboard", guide)

# ─────────────────────── PACKAGES ───────────────────────
def render_packages(guide, msg="", err=""):
    gid = guide["id"]
    packages = guide_db.get_packages(gid)
    city_opts = "".join(f'<option>{c}</option>' for c in CITIES)

    alert = ""
    if msg: alert = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:10px;padding:12px 16px;color:#065F46;font-size:13px;margin-bottom:20px">&#10003; {msg}</div>'
    if err: alert = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:10px;padding:12px 16px;color:#DC2626;font-size:13px;margin-bottom:20px">&#9888; {err}</div>'

    pkg_cards = ""
    for p in packages:
        incl = "".join(f'<span style="background:#EDE9FE;color:#5B21B6;padding:3px 10px;border-radius:20px;font-size:12px;margin:2px 2px 2px 0;display:inline-block">{i.strip()}</span>' for i in p["inclusions"].split(",") if i.strip())
        pkg_cards += f"""
        <div style="border:1px solid #E2E8F0;border-radius:12px;padding:18px;background:#fff;margin-bottom:14px">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px">
            <div style="flex:1">
              <div style="font-weight:800;font-size:16px;color:#1F2937">{p["title"]}</div>
              <div style="font-size:12px;color:#6B7280;margin-top:3px">&#128205; {p["city"]} &bull; &#9202; {p["duration"]}</div>
              {"" if not p["description"] else f'<div style="font-size:13px;color:#4B5563;margin-top:8px;line-height:1.6">{p["description"]}</div>'}
              {"" if not incl else f'<div style="margin-top:10px">{incl}</div>'}
            </div>
            <div style="text-align:right">
              <div style="font-size:22px;font-weight:900;color:#6B21A8;white-space:nowrap">{p["price"]}</div>
              <form method="post" action="/guide/packages" style="margin-top:8px">
                <input type="hidden" name="action" value="delete_package"/>
                <input type="hidden" name="pkg_id" value="{p["id"]}"/>
                <button class="g-btn" style="background:#FEE2E2;color:#DC2626;padding:6px 12px;font-size:12px" onclick="return confirm('Delete this package?')">&#128465; Delete</button>
              </form>
            </div>
          </div>
        </div>"""

    body = f"""
    <div style="margin-bottom:24px">
      <div style="font-size:24px;font-weight:900;color:#1F2937">My Packages</div>
      <div style="font-size:14px;color:#6B7280">Create and manage your tour packages</div>
    </div>
    {alert}
    <div class="g-card">
      <div class="g-card-hdr" style="background:#6B21A8">&#43; Add New Package</div>
      <div class="g-card-body">
        <form method="post" action="/guide/packages" style="display:flex;flex-direction:column;gap:14px">
          <input type="hidden" name="action" value="add_package"/>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
            <div><label class="g-lbl">Package Title *</label><input class="g-inp" name="title" placeholder="e.g. Mayon Volcano Day Tour" required/></div>
            <div><label class="g-lbl">Price *</label><input class="g-inp" name="price" placeholder="e.g. P1,500/person" required/></div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
            <div><label class="g-lbl">Duration</label>
              <select class="g-inp" name="duration"><option>Half Day</option><option selected>Full Day</option><option>2 Days</option><option>3 Days</option><option>Custom</option></select>
            </div>
            <div><label class="g-lbl">City</label><select class="g-inp" name="city">{city_opts}</select></div>
          </div>
          <div><label class="g-lbl">Description</label><textarea class="g-inp" name="description" rows="2" placeholder="What's included in this tour package?" style="resize:none"></textarea></div>
          <div><label class="g-lbl">Inclusions (comma separated)</label><input class="g-inp" name="inclusions" placeholder="e.g. Transportation, Lunch, Guide fee, Entrance fees"/></div>
          <div><button class="g-btn" type="submit" style="background:#6B21A8;color:#fff;padding:11px 24px">Add Package</button></div>
        </form>
      </div>
    </div>
    <div style="font-weight:700;font-size:16px;color:#1F2937;margin-bottom:14px">{len(packages)} Package{"s" if len(packages)!=1 else ""}</div>
    {pkg_cards or '<div class="g-card"><div class="g-card-body" style="text-align:center;padding:40px;color:#9CA3AF"><div style="font-size:48px;margin-bottom:12px">&#128196;</div><div style="font-weight:700">No packages yet</div></div></div>'}"""
    return build_guide_shell("My Packages", body, "packages", guide)

# ─────────────────────── BOOKINGS ───────────────────────
def render_bookings(guide, filter_status="all", msg="", err=""):
    gid = guide["id"]
    all_bookings = guide_db.get_bookings(gid)
    shown = all_bookings if filter_status == "all" else [b for b in all_bookings if b["status"] == filter_status]

    alert = ""
    if msg: alert = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:10px;padding:12px 16px;color:#065F46;font-size:13px;margin-bottom:20px">&#10003; {msg}</div>'
    if err: alert = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:10px;padding:12px 16px;color:#DC2626;font-size:13px;margin-bottom:20px">&#9888; {err}</div>'

    tabs = "".join(
        f'<a href="/guide/bookings?filter={s}" style="padding:8px 18px;border-radius:20px;text-decoration:none;font-size:13px;font-weight:600;background:{"#6B21A8" if filter_status==s else "#fff"};color:{"#fff" if filter_status==s else "#374151"};border:1px solid {"#6B21A8" if filter_status==s else "#E2E8F0"}">{s.title()} {"("+str(len([b for b in all_bookings if b["status"]==s]))+")" if s!="all" else "("+str(len(all_bookings))+")"}</a>'
        for s in ["all","pending","accepted","rejected","cancelled","rescheduled"]
    )

    cards = ""
    for b in shown:
        sc = STATUS_COLORS.get(b["status"],"#6B7280")
        sb = STATUS_BG.get(b["status"],"#F9FAFB")
        actions = ""
        if b["status"] == "pending":
            actions = f"""
            <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
              <form method="post" action="/guide/bookings?filter={filter_status}"><input type="hidden" name="action" value="accept_booking"/><input type="hidden" name="booking_id" value="{b["id"]}"/><button class="g-btn" style="background:#059669;color:#fff;padding:8px 16px;font-size:13px">&#10003; Accept</button></form>
              <form method="post" action="/guide/bookings?filter={filter_status}"><input type="hidden" name="action" value="reject_booking"/><input type="hidden" name="booking_id" value="{b["id"]}"/><button class="g-btn" style="background:#DC2626;color:#fff;padding:8px 16px;font-size:13px">&#10007; Reject</button></form>
            </div>"""
        elif b["status"] == "accepted":
            actions = f"""
            <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;align-items:center">
              <form method="post" action="/guide/bookings?filter={filter_status}"><input type="hidden" name="action" value="cancel_booking"/><input type="hidden" name="booking_id" value="{b["id"]}"/><button class="g-btn" style="background:#6B7280;color:#fff;padding:8px 16px;font-size:13px">Cancel</button></form>
              <form method="post" action="/guide/bookings?filter={filter_status}" style="display:flex;align-items:center;gap:8px"><input type="hidden" name="action" value="reschedule_booking"/><input type="hidden" name="booking_id" value="{b["id"]}"/><input class="g-inp" type="date" name="new_date" required style="width:160px;padding:7px 10px"/><button class="g-btn" style="background:#2563EB;color:#fff;padding:8px 16px;font-size:13px">Reschedule</button></form>
            </div>"""
        cards += f"""
        <div style="border:1px solid #E2E8F0;border-radius:12px;padding:18px;background:{sb};margin-bottom:12px">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px">
            <div>
              <div style="font-weight:800;font-size:16px;color:#1F2937">{b["tourist_name"]}</div>
              <div style="font-size:12px;color:#6B7280;margin-top:4px">
                &#128222; {b.get("tourist_phone","N/A")} &bull; &#128197; {b["tour_date"]} &bull; &#128101; {b["pax"]} pax
              </div>
              <div style="font-size:13px;color:#4B5563;margin-top:4px">Package: <strong>{b["package_title"] or "Custom Tour"}</strong></div>
              {"" if not b["notes"] else f'<div style="font-size:12px;color:#6B7280;margin-top:4px;font-style:italic;background:rgba(0,0,0,.03);padding:6px 10px;border-radius:6px">"{b["notes"]}"</div>'}
              {"" if not b["guide_notes"] else f'<div style="font-size:12px;color:#2563EB;margin-top:4px">&#128221; {b["guide_notes"]}</div>'}
            </div>
            <span style="background:{sc}22;color:{sc};padding:5px 14px;border-radius:20px;font-size:12px;font-weight:700;white-space:nowrap">{b["status"].upper()}</span>
          </div>
          {actions}
        </div>"""

    body = f"""
    <div style="margin-bottom:24px">
      <div style="font-size:24px;font-weight:900;color:#1F2937">Bookings</div>
      <div style="font-size:14px;color:#6B7280">Manage all your tour bookings</div>
    </div>
    {alert}
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px">{tabs}</div>
    {cards or '<div class="g-card"><div class="g-card-body" style="text-align:center;padding:40px;color:#9CA3AF"><div style="font-size:48px;margin-bottom:12px">&#128197;</div><div style="font-weight:700">No bookings found</div></div></div>'}"""
    return build_guide_shell("Bookings", body, "bookings", guide)

# ─────────────────────── AVAILABILITY ───────────────────────
def render_availability(guide, msg="", err=""):
    avail = guide.get("availability","Mon,Tue,Wed,Thu,Fri,Sat,Sun")
    checked = [d.strip() for d in avail.split(",") if d.strip()]

    alert = ""
    if msg: alert = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:10px;padding:12px 16px;color:#065F46;font-size:13px;margin-bottom:20px">&#10003; {msg}</div>'

    checkboxes = "".join(
        f'<label style="display:flex;align-items:center;gap:10px;padding:14px 18px;border:2px solid {"#6B21A8" if d in checked else "#E2E8F0"};border-radius:10px;cursor:pointer;background:{"#F3E8FF" if d in checked else "#fff"};font-weight:{"700" if d in checked else "400"};color:{"#6B21A8" if d in checked else "#4B5563"}">'
        f'<input type="checkbox" name="days" value="{d}" {"checked" if d in checked else ""} style="width:18px;height:18px;accent-color:#6B21A8"/> {d}</label>'
        for d in DAYS
    )

    body = f"""
    <div style="margin-bottom:24px">
      <div style="font-size:24px;font-weight:900;color:#1F2937">Availability</div>
      <div style="font-size:14px;color:#6B7280">Set the days you are available for tours</div>
    </div>
    {alert}
    <div class="g-card" style="max-width:600px">
      <div class="g-card-hdr" style="background:#6B21A8">&#128336; Weekly Schedule</div>
      <div class="g-card-body">
        <form method="post" action="/guide/availability" style="display:flex;flex-direction:column;gap:16px">
          <input type="hidden" name="action" value="update_availability"/>
          <div style="font-size:13px;color:#6B7280;margin-bottom:8px">Select the days you are available:</div>
          <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px">{checkboxes}</div>
          <div>
            <label class="g-lbl">Additional Notes (optional)</label>
            <input class="g-inp" name="avail_note" placeholder="e.g. Available on holidays, Off on rainy season..."/>
          </div>
          <div><button class="g-btn" type="submit" style="background:#6B21A8;color:#fff;padding:12px 28px">Save Availability</button></div>
        </form>
      </div>
    </div>"""
    return build_guide_shell("Availability", body, "availability", guide)

# ─────────────────────── RATINGS ───────────────────────
def render_ratings(guide):
    gid = guide["id"]
    ratings = guide_db.get_ratings(gid)
    avg_rating, rating_count = guide_db.get_avg_rating(gid)

    stars_bar = ""
    for s in range(5, 0, -1):
        cnt = len([r for r in ratings if r["rating"] == s])
        pct = int(cnt / rating_count * 100) if rating_count else 0
        stars_bar += f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px"><span style="font-size:13px;min-width:25px;color:#6B7280">{s}&#9733;</span><div style="flex:1;height:12px;background:#F3F4F6;border-radius:6px;overflow:hidden"><div style="height:100%;width:{pct}%;background:#F59E0B;border-radius:6px"></div></div><span style="font-size:12px;color:#6B7280;min-width:30px">{cnt}</span></div>'

    cards = "".join(f"""
    <div style="border:1px solid #E2E8F0;border-radius:12px;padding:16px;margin-bottom:12px;background:#fff">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
        <div style="font-weight:700;color:#1F2937">{r["tourist_name"]}</div>
        <div style="color:#F59E0B;font-size:16px">{"&#9733;"*r["rating"]}{"&#9734;"*(5-r["rating"])}</div>
      </div>
      {"" if not r["feedback"] else f'<div style="font-size:13px;color:#4B5563;line-height:1.6;font-style:italic">&ldquo;{r["feedback"]}&rdquo;</div>'}
      <div style="font-size:11px;color:#9CA3AF;margin-top:8px">{r["created"][:10]}</div>
    </div>""" for r in ratings) or '<div style="text-align:center;padding:40px;color:#9CA3AF"><div style="font-size:48px;margin-bottom:12px">&#11088;</div><div style="font-weight:700">No reviews yet</div></div>'

    body = f"""
    <div style="margin-bottom:24px">
      <div style="font-size:24px;font-weight:900;color:#1F2937">Ratings & Feedback</div>
      <div style="font-size:14px;color:#6B7280">See what tourists say about your tours</div>
    </div>
    <div style="display:grid;grid-template-columns:300px 1fr;gap:20px;margin-bottom:24px">
      <div class="g-card">
        <div class="g-card-hdr" style="background:#D97706">&#11088; Overall Rating</div>
        <div class="g-card-body" style="text-align:center">
          <div style="font-size:64px;font-weight:900;color:#D97706;line-height:1">{avg_rating}</div>
          <div style="color:#F59E0B;font-size:24px;margin:8px 0">{"&#9733;"*int(avg_rating)}{"&#9734;"*(5-int(avg_rating))}</div>
          <div style="font-size:14px;color:#6B7280">{rating_count} review{"s" if rating_count!=1 else ""}</div>
        </div>
      </div>
      <div class="g-card">
        <div class="g-card-hdr" style="background:#6B21A8">Rating Breakdown</div>
        <div class="g-card-body">{stars_bar}</div>
      </div>
    </div>
    <div style="font-weight:700;font-size:16px;color:#1F2937;margin-bottom:16px">All Reviews</div>
    {cards}"""
    return build_guide_shell("Ratings & Feedback", body, "ratings", guide)

# ─────────────────────── PROFILE ───────────────────────
def render_profile(guide, msg="", err=""):
    city_opts = "".join(f'<option {"selected" if c==guide.get("city","Manila") else ""}>{c}</option>' for c in CITIES)

    alert = ""
    if msg: alert = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:10px;padding:12px 16px;color:#065F46;font-size:13px;margin-bottom:20px">&#10003; {msg}</div>'
    if err: alert = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:10px;padding:12px 16px;color:#DC2626;font-size:13px;margin-bottom:20px">&#9888; {err}</div>'

    body = f"""
    <div style="margin-bottom:24px">
      <div style="font-size:24px;font-weight:900;color:#1F2937">My Profile</div>
      <div style="font-size:14px;color:#6B7280">Update your public guide profile</div>
    </div>
    {alert}
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
      <div class="g-card">
        <div class="g-card-hdr" style="background:#6B21A8">&#128100; Profile Information</div>
        <div class="g-card-body">
          <form method="post" action="/guide/profile" style="display:flex;flex-direction:column;gap:14px">
            <input type="hidden" name="action" value="update_profile"/>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
              <div><label class="g-lbl">First Name</label><input class="g-inp" name="fname" value="{guide.get("fname","")}"/></div>
              <div><label class="g-lbl">Last Name</label><input class="g-inp" name="lname" value="{guide.get("lname","")}"/></div>
            </div>
            <div><label class="g-lbl">Phone</label><input class="g-inp" name="phone" value="{guide.get("phone","")}"/></div>
            <div><label class="g-lbl">City</label><select class="g-inp" name="city">{city_opts}</select></div>
            <div><label class="g-lbl">Languages</label><input class="g-inp" name="languages" value="{guide.get("languages","EN, FIL")}" placeholder="e.g. EN, FIL, ES"/></div>
            <div><label class="g-lbl">Speciality</label><input class="g-inp" name="speciality" value="{guide.get("speciality","")}" placeholder="e.g. Nature Tours, Historical"/></div>
            <div><label class="g-lbl">Daily Rate</label><input class="g-inp" name="rate" value="{guide.get("rate","P1,500/day")}" placeholder="e.g. P1,500/day"/></div>
            <div><label class="g-lbl">Bio / About You</label><textarea class="g-inp" name="bio" rows="4" placeholder="Tell tourists about yourself..." style="resize:none">{guide.get("bio","")}</textarea></div>
            <button class="g-btn" type="submit" style="background:#6B21A8;color:#fff;padding:12px">Save Profile</button>
          </form>
        </div>
      </div>
      <div class="g-card">
        <div class="g-card-hdr" style="background:#DC2626">&#128274; Change Password</div>
        <div class="g-card-body">
          <form method="post" action="/guide/profile" style="display:flex;flex-direction:column;gap:14px">
            <input type="hidden" name="action" value="change_password"/>
            <div><label class="g-lbl">New Password</label><input class="g-inp" type="password" name="new_pw" placeholder="Min. 6 characters"/></div>
            <div><label class="g-lbl">Confirm New Password</label><input class="g-inp" type="password" name="new_pw2" placeholder="Repeat new password"/></div>
            <button class="g-btn" type="submit" style="background:#DC2626;color:#fff;padding:12px">Change Password</button>
          </form>
        </div>
      </div>
    </div>"""
    return build_guide_shell("My Profile", body, "profile", guide)
