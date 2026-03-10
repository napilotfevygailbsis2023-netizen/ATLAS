import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
import guide_db

CITIES = ["Manila","Baguio","Tagaytay","Vigan","Ilocos Norte","Batangas","Albay","Pangasinan","Bataan"]
DAYS   = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

STATUS_COLORS = {"pending":"#C8930A","accepted":"#065F46","rejected":"#CE1126","cancelled":"#6B7280","rescheduled":"#0038A8"}
STATUS_BG     = {"pending":"#FFFBEB","accepted":"#ECFDF5","rejected":"#FEF2F2","cancelled":"#F9FAFB","rescheduled":"#EFF6FF"}

def _section(title, color, icon, content):
    return (
        f'<div style="background:#fff;border-radius:14px;box-shadow:0 2px 10px rgba(0,0,0,.08);margin-bottom:24px;overflow:hidden">'
        f'<div style="background:{color};padding:14px 20px;color:#fff;font-weight:800;font-size:16px">{icon} {title}</div>'
        f'<div style="padding:20px">{content}</div>'
        f'</div>'
    )

def render(guide, section="dashboard", form=None, msg="", err=""):
    gid   = guide["id"]
    fname = guide["fname"]

    packages = guide_db.get_packages(gid)
    bookings = guide_db.get_bookings(gid)
    ratings  = guide_db.get_ratings(gid)
    avg_rating, rating_count = guide_db.get_avg_rating(gid)

    pending   = [b for b in bookings if b["status"] == "pending"]
    accepted  = [b for b in bookings if b["status"] == "accepted"]
    upcoming  = [b for b in accepted if b["tour_date"] >= __import__('datetime').date.today().isoformat()]

    # ── NAV ──
    nav_items = [
        ("dashboard","&#127968;","Dashboard"),
        ("packages","&#128196;","My Packages"),
        ("bookings","&#128197;","Bookings"),
        ("availability","&#128336;","Availability"),
        ("ratings","&#11088;","Ratings & Feedback"),
        ("profile","&#128100;","My Profile"),
    ]
    nav_html = "".join(
        f'<a href="/guide_dashboard.py?section={s}" style="display:flex;align-items:center;gap:10px;padding:10px 16px;border-radius:8px;text-decoration:none;font-size:14px;font-weight:{"700" if section==s else "400"};color:{"#fff" if section==s else "#C4B5FD"};background:{"rgba(255,255,255,.2)" if section==s else "none"}">{ic} {lb}</a>'
        for s, ic, lb in nav_items
    )

    alert = ""
    if msg: alert = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:8px;padding:10px 16px;color:#065F46;font-size:13px;margin-bottom:16px">&#10003; {msg}</div>'
    if err: alert = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:8px;padding:10px 16px;color:#DC2626;font-size:13px;margin-bottom:16px">&#9888; {err}</div>'

    # ── SECTIONS ──
    if section == "dashboard":
        content = f"""
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px;margin-bottom:24px">
          <div style="background:#6B21A8;color:#fff;border-radius:12px;padding:16px;text-align:center"><div style="font-size:28px;font-weight:900">{len(packages)}</div><div style="font-size:12px;opacity:.85">Packages</div></div>
          <div style="background:#0038A8;color:#fff;border-radius:12px;padding:16px;text-align:center"><div style="font-size:28px;font-weight:900">{len(pending)}</div><div style="font-size:12px;opacity:.85">Pending</div></div>
          <div style="background:#065F46;color:#fff;border-radius:12px;padding:16px;text-align:center"><div style="font-size:28px;font-weight:900">{len(upcoming)}</div><div style="font-size:12px;opacity:.85">Upcoming</div></div>
          <div style="background:#C8930A;color:#fff;border-radius:12px;padding:16px;text-align:center"><div style="font-size:28px;font-weight:900">{avg_rating}&#9733;</div><div style="font-size:12px;opacity:.85">Avg Rating</div></div>
        </div>"""
        # Upcoming bookings
        if upcoming:
            rows = "".join(
                f'<tr><td style="padding:10px 12px;font-weight:700">{b["tourist_name"]}</td>'
                f'<td style="padding:10px 12px;color:#6B7280">{b["tour_date"]}</td>'
                f'<td style="padding:10px 12px;color:#6B7280">{b["package_title"] or "Custom Tour"}</td>'
                f'<td style="padding:10px 12px;color:#6B7280">{b["pax"]} pax</td></tr>'
                for b in upcoming[:5]
            )
            content += _section("Upcoming Bookings","#0038A8","&#128197;",
                f'<table style="width:100%;border-collapse:collapse"><thead><tr style="background:#F9FAFB"><th style="padding:10px 12px;text-align:left;font-size:12px;color:#6B7280">Tourist</th><th style="padding:10px 12px;text-align:left;font-size:12px;color:#6B7280">Date</th><th style="padding:10px 12px;text-align:left;font-size:12px;color:#6B7280">Package</th><th style="padding:10px 12px;text-align:left;font-size:12px;color:#6B7280">Pax</th></tr></thead><tbody>{rows}</tbody></table>')
        # Pending bookings alert
        if pending:
            rows = "".join(
                f'<div style="border:1px solid #FDE68A;border-radius:8px;padding:12px;background:#FFFBEB;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center">'
                f'<div><div style="font-weight:700;color:#1F2937">{b["tourist_name"]}</div><div style="font-size:12px;color:#6B7280">{b["tour_date"]} &bull; {b["pax"]} pax</div></div>'
                f'<div style="display:flex;gap:8px">'
                f'<form method="post" action="/guide_dashboard.py?section=bookings" style="display:inline"><input type="hidden" name="action" value="accept_booking"/><input type="hidden" name="booking_id" value="{b["id"]}"/><button class="btn" style="background:#065F46;color:#fff;padding:6px 12px;font-size:12px">Accept</button></form>'
                f'<form method="post" action="/guide_dashboard.py?section=bookings" style="display:inline"><input type="hidden" name="action" value="reject_booking"/><input type="hidden" name="booking_id" value="{b["id"]}"/><button class="btn" style="background:#CE1126;color:#fff;padding:6px 12px;font-size:12px">Reject</button></form>'
                f'</div></div>'
                for b in pending
            )
            content += _section("Pending Requests","#C8930A","&#9888;", rows)

    elif section == "packages":
        city_opts = "".join(f'<option>{c}</option>' for c in CITIES)
        add_form = f"""
        <form method="post" action="/guide_dashboard.py?section=packages" style="display:flex;flex-direction:column;gap:12px;margin-bottom:24px;background:#F9FAFB;padding:20px;border-radius:12px;border:1px solid #E5E7EB">
          <div style="font-weight:700;font-size:15px;color:#1F2937;margin-bottom:4px">&#43; Add New Package</div>
          <input type="hidden" name="action" value="add_package"/>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div><label class="lbl">Package Title *</label><input class="inp" name="title" placeholder="e.g. Mayon Volcano Day Tour" required style="width:100%"/></div>
            <div><label class="lbl">Price *</label><input class="inp" name="price" placeholder="e.g. P1,500/person" required style="width:100%"/></div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div><label class="lbl">Duration</label><select class="inp" name="duration" style="width:100%"><option>Half Day</option><option>Full Day</option><option>2 Days</option><option>3 Days</option><option>Custom</option></select></div>
            <div><label class="lbl">City</label><select class="inp" name="city" style="width:100%">{city_opts}</select></div>
          </div>
          <div><label class="lbl">Description</label><textarea class="inp" name="description" rows="2" placeholder="What's included in this tour?" style="width:100%;resize:none"></textarea></div>
          <div><label class="lbl">Inclusions (comma separated)</label><input class="inp" name="inclusions" placeholder="e.g. Transportation, Lunch, Guide fee" style="width:100%"/></div>
          <button class="btn" type="submit" style="background:#6B21A8;color:#fff;padding:10px;font-weight:700;width:fit-content">Add Package</button>
        </form>"""
        pkg_cards = ""
        for p in packages:
            incl = "".join(f'<span style="background:#F3E8FF;color:#6B21A8;padding:2px 8px;border-radius:10px;font-size:11px;margin:2px">{i.strip()}</span>' for i in p["inclusions"].split(",") if i.strip())
            pkg_cards += f"""
            <div style="border:1px solid #E5E7EB;border-radius:12px;padding:16px;margin-bottom:12px;background:#fff">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
                <div><div style="font-weight:800;font-size:15px;color:#1F2937">{p["title"]}</div>
                <div style="font-size:12px;color:#6B7280">{p["city"]} &bull; {p["duration"]}</div></div>
                <div style="display:flex;align-items:center;gap:10px">
                  <span style="font-size:18px;font-weight:800;color:#6B21A8">{p["price"]}</span>
                  <form method="post" action="/guide_dashboard.py?section=packages" style="display:inline">
                    <input type="hidden" name="action" value="delete_package"/>
                    <input type="hidden" name="pkg_id" value="{p["id"]}"/>
                    <button class="btn" style="background:#FEE2E2;color:#CE1126;padding:5px 10px;font-size:12px" onclick="return confirm('Delete this package?')">&#128465;</button>
                  </form>
                </div>
              </div>
              <div style="font-size:13px;color:#4B5563;margin-bottom:8px">{p["description"]}</div>
              <div>{incl}</div>
            </div>"""
        content = add_form + (pkg_cards or '<div style="color:#9CA3AF;text-align:center;padding:30px">No packages yet. Add your first package above!</div>')

    elif section == "bookings":
        status_tabs = "".join(
            f'<a href="/guide_dashboard.py?section=bookings&filter={s}" style="padding:8px 16px;border-radius:20px;text-decoration:none;font-size:13px;font-weight:600;background:{"#6B21A8" if (form or {}).get("filter","")==s else "#F3F4F6"};color:{"#fff" if (form or {}).get("filter","")==s else "#374151"}">{s.title()}</a>'
            for s in ["all","pending","accepted","rejected","cancelled"]
        )
        all_b = bookings
        booking_rows = ""
        for b in all_b:
            sc = STATUS_COLORS.get(b["status"],"#6B7280")
            sb = STATUS_BG.get(b["status"],"#F9FAFB")
            booking_rows += f"""
            <div style="border:1px solid #E5E7EB;border-radius:12px;padding:16px;margin-bottom:12px;background:{sb}">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">
                <div>
                  <div style="font-weight:800;font-size:15px;color:#1F2937">{b["tourist_name"]}</div>
                  <div style="font-size:12px;color:#6B7280">{b.get("tourist_phone","")} &bull; {b["tour_date"]} &bull; {b["pax"]} pax</div>
                  <div style="font-size:12px;color:#4B5563;margin-top:4px">Package: {b["package_title"] or "Custom Tour"}</div>
                  {"" if not b["notes"] else f'<div style="font-size:12px;color:#6B7280;margin-top:4px;font-style:italic">Note: {b["notes"]}</div>'}
                </div>
                <span style="background:{sc}22;color:{sc};padding:4px 12px;border-radius:20px;font-size:12px;font-weight:700;height:fit-content">{b["status"].upper()}</span>
              </div>
              {f'''<div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
                <form method="post" action="/guide_dashboard.py?section=bookings" style="display:inline"><input type="hidden" name="action" value="accept_booking"/><input type="hidden" name="booking_id" value="{b["id"]}"/><button class="btn" style="background:#065F46;color:#fff;padding:7px 14px;font-size:13px">&#10003; Accept</button></form>
                <form method="post" action="/guide_dashboard.py?section=bookings" style="display:inline"><input type="hidden" name="action" value="reject_booking"/><input type="hidden" name="booking_id" value="{b["id"]}"/><button class="btn" style="background:#CE1126;color:#fff;padding:7px 14px;font-size:13px">&#10007; Reject</button></form>
              </div>''' if b["status"]=="pending" else ""}
              {f'''<div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
                <form method="post" action="/guide_dashboard.py?section=bookings" style="display:inline"><input type="hidden" name="action" value="cancel_booking"/><input type="hidden" name="booking_id" value="{b["id"]}"/><button class="btn" style="background:#6B7280;color:#fff;padding:7px 14px;font-size:13px">Cancel</button></form>
                <form method="post" action="/guide_dashboard.py?section=bookings" style="display:inline"><input type="hidden" name="action" value="reschedule_booking"/><input type="hidden" name="booking_id" value="{b["id"]}"/>
                <input class="inp" type="date" name="new_date" required style="padding:6px;font-size:12px"/>
                <button class="btn" style="background:#0038A8;color:#fff;padding:7px 14px;font-size:13px">Reschedule</button></form>
              </div>''' if b["status"]=="accepted" else ""}
            </div>"""
        content = f'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">{status_tabs}</div>' + (booking_rows or '<div style="color:#9CA3AF;text-align:center;padding:30px">No bookings yet.</div>')

    elif section == "availability":
        avail = guide.get("availability","Mon-Sun")
        checked_days = [d.strip() for d in avail.split(",") if d.strip()]
        checkboxes = "".join(
            f'<label style="display:flex;align-items:center;gap:8px;padding:10px 14px;border:1px solid {"#6B21A8" if d in checked_days else "#E5E7EB"};border-radius:8px;cursor:pointer;background:{"#F3E8FF" if d in checked_days else "#fff"}">'
            f'<input type="checkbox" name="days" value="{d}" {"checked" if d in checked_days else ""} style="width:16px;height:16px;accent-color:#6B21A8"/> {d}</label>'
            for d in DAYS
        )
        content = f"""
        <form method="post" action="/guide_dashboard.py?section=availability" style="display:flex;flex-direction:column;gap:16px">
          <input type="hidden" name="action" value="update_availability"/>
          <div>
            <label class="lbl" style="font-size:15px;margin-bottom:12px">Select your available days:</label>
            <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:10px;margin-top:10px">{checkboxes}</div>
          </div>
          <div>
            <label class="lbl">Additional Notes (e.g. "Off on holidays")</label>
            <input class="inp" name="avail_note" placeholder="Optional notes about your availability" style="width:100%"/>
          </div>
          <button class="btn" type="submit" style="background:#6B21A8;color:#fff;padding:11px;font-weight:700;width:fit-content">Save Availability</button>
        </form>"""

    elif section == "ratings":
        stars_bar = ""
        for s in range(5, 0, -1):
            cnt = len([r for r in ratings if r["rating"] == s])
            pct = int((cnt / rating_count * 100)) if rating_count else 0
            stars_bar += f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px"><span style="font-size:13px;min-width:20px">{s}&#9733;</span><div style="flex:1;height:10px;background:#F3F4F6;border-radius:5px;overflow:hidden"><div style="height:100%;width:{pct}%;background:#F59E0B;border-radius:5px"></div></div><span style="font-size:12px;color:#6B7280;min-width:30px">{cnt}</span></div>'
        summary = f"""
        <div style="display:flex;align-items:center;gap:24px;margin-bottom:20px;background:#FFFBEB;border-radius:12px;padding:20px">
          <div style="text-align:center"><div style="font-size:52px;font-weight:900;color:#C8930A">{avg_rating}</div><div style="color:#F59E0B;font-size:20px">{"&#9733;"*int(avg_rating)}{"&#9734;"*(5-int(avg_rating))}</div><div style="font-size:13px;color:#6B7280">{rating_count} review{"s" if rating_count!=1 else ""}</div></div>
          <div style="flex:1">{stars_bar}</div>
        </div>"""
        review_cards = "".join(
            f'<div style="border:1px solid #E5E7EB;border-radius:10px;padding:14px;margin-bottom:10px">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:6px">'
            f'<span style="font-weight:700;color:#1F2937">{r["tourist_name"]}</span>'
            f'<span style="color:#F59E0B">{"&#9733;"*r["rating"]}{"&#9734;"*(5-r["rating"])}</span></div>'
            f'<div style="font-size:13px;color:#4B5563;font-style:italic">&ldquo;{r["feedback"]}&rdquo;</div>'
            f'<div style="font-size:11px;color:#9CA3AF;margin-top:6px">{r["created"][:10]}</div>'
            f'</div>'
            for r in ratings
        ) or '<div style="color:#9CA3AF;text-align:center;padding:30px">No reviews yet.</div>'
        content = summary + review_cards

    elif section == "profile":
        city_opts = "".join(f'<option {"selected" if c==guide.get("city","Manila") else ""}>{c}</option>' for c in CITIES)
        content = f"""
        <form method="post" action="/guide_dashboard.py?section=profile" style="display:flex;flex-direction:column;gap:14px">
          <input type="hidden" name="action" value="update_profile"/>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
            <div><label class="lbl">First Name</label><input class="inp" name="fname" value="{guide.get("fname","")}" style="width:100%"/></div>
            <div><label class="lbl">Last Name</label><input class="inp" name="lname" value="{guide.get("lname","")}" style="width:100%"/></div>
          </div>
          <div><label class="lbl">Phone</label><input class="inp" name="phone" value="{guide.get("phone","")}" style="width:100%"/></div>
          <div><label class="lbl">City</label><select class="inp" name="city" style="width:100%">{city_opts}</select></div>
          <div><label class="lbl">Languages</label><input class="inp" name="languages" value="{guide.get("languages","EN, FIL")}" placeholder="e.g. EN, FIL, ES" style="width:100%"/></div>
          <div><label class="lbl">Speciality</label><input class="inp" name="speciality" value="{guide.get("speciality","")}" placeholder="e.g. Nature Tours, Historical" style="width:100%"/></div>
          <div><label class="lbl">Daily Rate</label><input class="inp" name="rate" value="{guide.get("rate","P1,500/day")}" placeholder="e.g. P1,500/day" style="width:100%"/></div>
          <div><label class="lbl">Bio</label><textarea class="inp" name="bio" rows="3" placeholder="Describe yourself as a tour guide..." style="width:100%;resize:none">{guide.get("bio","")}</textarea></div>
          <button class="btn" type="submit" style="background:#6B21A8;color:#fff;padding:11px;font-weight:700">Save Profile</button>
        </form>
        <hr style="margin:24px 0;border-color:#F3F4F6"/>
        <div style="font-weight:700;font-size:15px;margin-bottom:14px;color:#1F2937">Change Password</div>
        <form method="post" action="/guide_dashboard.py?section=profile" style="display:flex;flex-direction:column;gap:12px">
          <input type="hidden" name="action" value="change_password"/>
          <div><label class="lbl">New Password</label><input class="inp" type="password" name="new_pw" style="width:100%"/></div>
          <div><label class="lbl">Confirm New Password</label><input class="inp" type="password" name="new_pw2" style="width:100%"/></div>
          <button class="btn" type="submit" style="background:#CE1126;color:#fff;padding:10px;font-weight:700;width:fit-content">Change Password</button>
        </form>"""

    else:
        content = ""

    # ── LAYOUT ──
    section_title = {"dashboard":"Dashboard","packages":"My Packages","bookings":"Bookings",
                     "availability":"Availability","ratings":"Ratings & Feedback","profile":"My Profile"}.get(section,"Dashboard")
    body = f"""
    <div style="display:grid;grid-template-columns:220px 1fr;min-height:85vh;gap:0;background:#F8FAFC">
      <!-- Sidebar -->
      <div style="background:linear-gradient(160deg,#6B21A8,#4C1D95);padding:24px 12px;display:flex;flex-direction:column;gap:4px">
        <div style="text-align:center;margin-bottom:24px">
          <div style="width:60px;height:60px;border-radius:50%;background:rgba(255,255,255,.25);display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:900;color:#fff;margin:0 auto 8px">{guide["fname"][0]}{guide["lname"][0]}</div>
          <div style="font-weight:800;color:#fff;font-size:14px">{guide["fname"]} {guide["lname"]}</div>
          <div style="font-size:11px;color:#C4B5FD">{guide.get("city","")}</div>
        </div>
        {nav_html}
        <div style="margin-top:auto;padding-top:20px">
          <a href="/guide_logout.py" style="display:flex;align-items:center;gap:10px;padding:10px 16px;border-radius:8px;text-decoration:none;font-size:13px;color:#C4B5FD">&#128682; Log Out</a>
        </div>
      </div>
      <!-- Main content -->
      <div style="padding:28px 32px;overflow-y:auto">
        <div style="font-size:22px;font-weight:900;color:#1F2937;margin-bottom:4px">{section_title}</div>
        <div style="font-size:13px;color:#6B7280;margin-bottom:20px">Welcome back, {fname}!</div>
        {alert}
        {content}
      </div>
    </div>"""
    return build_shell(f"Guide - {section_title}", body, "guides", user=None)
