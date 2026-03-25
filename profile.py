import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell

def render(user=None, msg="", err="", tab="profile"):
    if not user:
        return build_shell("Profile", '<div class="page-wrap"><div class="card"><div class="card-body" style="text-align:center;padding:40px"><div style="font-size:40px;margin-bottom:16px">&#128100;</div><div style="font-size:18px;font-weight:700;margin-bottom:12px">Please log in to view your profile</div><a href="/login.py"><button class="btn" style="background:#0038A8;color:#fff;padding:10px 28px">Log In</button></a></div></div></div>', "home", user=None)

    fname    = user.get("fname","")
    lname    = user.get("lname","")
    email    = user.get("email","")
    initials = (fname[0] if fname else "?").upper()

    msg_html = f'<div style="background:#D1FAE5;color:#065F46;padding:12px 16px;border-radius:8px;margin-bottom:16px;font-weight:600">&#10003; {msg}</div>' if msg else ""
    err_html = f'<div style="background:#FEE2E2;color:#CE1126;padding:12px 16px;border-radius:8px;margin-bottom:16px;font-weight:600">&#9888; {err}</div>' if err else ""

    # ── Load bookings for this tourist ──
    current_bookings = []
    history_bookings = []
    try:
        import guide_db
        import sqlite3, os as _os
        DB = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "atlas.db")
        conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
        today = datetime.date.today().isoformat()
        rows = conn.execute("""
            SELECT b.*, g.fname as gfname, g.lname as glname, g.city as gcity, g.phone as gphone
            FROM bookings b
            LEFT JOIN tour_guides g ON g.id = b.guide_id
            WHERE b.tourist_email = ?
            ORDER BY b.tour_date DESC
        """, (email,)).fetchall()
        conn.close()
        for r in rows:
            d = dict(r)
            if d["status"] in ("cancelled","rejected"):
                history_bookings.append(d)
            elif d["tour_date"] < today and d["status"] == "accepted":
                history_bookings.append(d)
            else:
                current_bookings.append(d)
    except Exception as e:
        pass

    STATUS_COLOR = {"pending":"#D97706","accepted":"#059669","rejected":"#DC2626","cancelled":"#6B7280","rescheduled":"#2563EB","completed":"#059669"}
    STATUS_BG    = {"pending":"#FFFBEB","accepted":"#ECFDF5","rejected":"#FEF2F2","cancelled":"#F9FAFB","rescheduled":"#EFF6FF","completed":"#ECFDF5"}

    def booking_card(b):
        sc = STATUS_COLOR.get(b["status"],"#6B7280")
        sb = STATUS_BG.get(b["status"],"#F9FAFB")
        gname = f'{b.get("gfname","")} {b.get("glname","")}'.strip() or "Tour Guide"
        return f"""
        <div style="border:1px solid #E2E8F0;border-radius:12px;padding:16px 18px;background:{sb};margin-bottom:12px">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">
            <div>
              <div style="font-weight:800;font-size:15px;color:#1F2937">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0038A8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                {gname}
              </div>
              <div style="font-size:12px;color:#6B7280;margin-top:4px;display:flex;gap:12px;flex-wrap:wrap">
                <span>
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                  {b["tour_date"]}
                </span>
                <span>&#128101; {b["pax"]} pax</span>
                <span>&#128196; {b.get("package_title","Custom Tour") or "Custom Tour"}</span>
                {f'<span>&#128205; {b.get("gcity","")}</span>' if b.get("gcity") else ""}
              </div>
              {f'<div style="font-size:12px;color:#4B5563;margin-top:6px;font-style:italic;background:rgba(0,0,0,.03);padding:6px 10px;border-radius:6px">"{b["notes"]}"</div>' if b.get("notes") else ""}
              {f'<div style="font-size:12px;color:#2563EB;margin-top:4px">Guide note: {b["guide_notes"]}</div>' if b.get("guide_notes") else ""}
            </div>
            <span style="background:{sc}22;color:{sc};padding:5px 14px;border-radius:20px;font-size:11px;font-weight:700;white-space:nowrap">{b["status"].upper()}</span>
          </div>
        </div>"""

    # ── Current bookings tab ──
    if current_bookings:
        cur_html = "".join(booking_card(b) for b in current_bookings)
    else:
        cur_html = '<div style="text-align:center;padding:32px;color:#9CA3AF"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin:0 auto 10px;display:block"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg><div style="font-weight:700">No active bookings</div><div style="font-size:12px;margin-top:4px"><a href="/guides.py" style="color:#0038A8;font-weight:600">Find a tour guide</a></div></div>'

    # ── History tab ──
    if history_bookings:
        hist_html = "".join(booking_card(b) for b in history_bookings)
    else:
        hist_html = '<div style="text-align:center;padding:32px;color:#9CA3AF"><div style="font-size:36px;margin-bottom:8px">&#128197;</div><div style="font-weight:700">No booking history yet</div></div>'

    bookings_section = f"""
    <div class="card" style="margin-bottom:20px">
      <div class="card-hdr" style="background:#0038A8">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        My Tour Guide Bookings
      </div>
      <div style="display:flex;border-bottom:2px solid #E2E8F0;padding:0 16px">
        <button onclick="switchBTab('current')" id="btab-current" class="btab btab-active">
          Current ({len(current_bookings)})
        </button>
        <button onclick="switchBTab('history')" id="btab-history" class="btab">
          History ({len(history_bookings)})
        </button>
      </div>
      <div class="card-body">
        <div id="bpane-current">{cur_html}</div>
        <div id="bpane-history" style="display:none">{hist_html}</div>
      </div>
    </div>
    <style>
      .btab{{padding:10px 20px;border:none;background:none;font-size:13px;font-weight:600;color:#6B7280;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-2px;font-family:inherit}}
      .btab-active{{color:#0038A8;border-bottom-color:#0038A8;background:#F0F4FF}}
    </style>
    <script>
    function switchBTab(tab) {{
      document.getElementById('bpane-current').style.display = tab==='current' ? 'block' : 'none';
      document.getElementById('bpane-history').style.display = tab==='history' ? 'block' : 'none';
      document.getElementById('btab-current').className = 'btab' + (tab==='current' ? ' btab-active' : '');
      document.getElementById('btab-history').className = 'btab' + (tab==='history' ? ' btab-active' : '');
    }}
    </script>"""

    body = f"""
    <div class="page-wrap" style="max-width:760px;margin:0 auto">
      <div style="margin-bottom:24px">
        <div class="section-title">My Profile</div>
        <div class="section-sub">Manage your tourist account details</div>
      </div>
      {msg_html}{err_html}

      <!-- Profile Card -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Account Information
        </div>
        <div class="card-body">
          <div style="display:flex;align-items:center;gap:20px;margin-bottom:24px;padding-bottom:20px;border-bottom:1px solid #F3F4F6">
            <div style="width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#0038A8,#0050d0);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;color:#fff;flex-shrink:0">{initials}</div>
            <div>
              <div style="font-size:22px;font-weight:800;color:#1F2937">{fname} {lname}</div>
              <div style="font-size:14px;color:#6B7280;margin-top:4px">&#9993; {email}</div>
              <div style="margin-top:8px"><span style="background:#DBEAFE;color:#1D4ED8;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600">&#9989; Tourist Account</span></div>
            </div>
          </div>
          <form method="post" action="/profile/update">
            <input type="hidden" name="action" value="update_profile"/>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px">
              <div><label class="lbl">First Name</label><input class="inp" name="fname" value="{fname}" style="width:100%"/></div>
              <div><label class="lbl">Last Name</label><input class="inp" name="lname" value="{lname}" style="width:100%"/></div>
            </div>
            <div style="margin-bottom:16px"><label class="lbl">Email Address</label><input class="inp" name="email" value="{email}" style="width:100%"/></div>
            <button class="btn" style="background:#0038A8;color:#fff;padding:10px 28px" type="submit">Save Changes</button>
          </form>
        </div>
      </div>

      <!-- Change Password -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          Change Password
        </div>
        <div class="card-body">
          <form method="post" action="/profile/update">
            <input type="hidden" name="action" value="change_password"/>
            <div style="display:flex;flex-direction:column;gap:12px">
              <div><label class="lbl">Current Password</label><input class="inp" type="password" name="old_pw" placeholder="Enter current password" style="width:100%"/></div>
              <div><label class="lbl">New Password</label><input class="inp" type="password" name="new_pw" placeholder="At least 6 characters" style="width:100%"/></div>
              <div><label class="lbl">Confirm New Password</label><input class="inp" type="password" name="new_pw2" placeholder="Repeat new password" style="width:100%"/></div>
            </div>
            <button class="btn" style="background:#0038A8;color:#fff;padding:10px 28px;margin-top:16px" type="submit">Update Password</button>
          </form>
        </div>
      </div>

      <!-- My Tour Guide Bookings -->
      {bookings_section}

    </div>"""
    return build_shell("My Profile", body, "profile", user=user)