import sys, os, datetime, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tourist_ui import build_shell

def e(s):
    return html.escape(str(s) if s is not None else "")

_TYPE_ICON = {
    "flight":     "&#9992;",
    "attraction": "&#127965;",
    "restaurant": "&#127869;",
}
_TYPE_LINK = {
    "flight":     "/flights.py",
    "attraction": "/attractions.py",
    "restaurant": "/restaurants.py",
}
_TYPE_COLOR = {
    "flight":     "#0038A8",
    "attraction": "#059669",
    "restaurant": "#D97706",
}

def _recently_viewed_html(user_email):
    try:
        import db as _db
        conn = _db.get_conn(); cur = conn.cursor(dictionary=True)
        cur.execute("""SELECT vh.* FROM view_history vh
                       JOIN users u ON u.id = vh.user_id
                       WHERE u.email=%s ORDER BY vh.viewed_at DESC LIMIT 15""",
                    (user_email.strip().lower(),))
        rows = cur.fetchall(); cur.close(); conn.close()
    except Exception:
        rows = []
    if not rows:
        return ""
    cards = ""
    for r in rows:
        itype = r.get("item_type","")
        icon  = _TYPE_ICON.get(itype, "&#128269;")
        col   = _TYPE_COLOR.get(itype, "#6B7280")
        base_link = _TYPE_LINK.get(itype, "/")
        item_id = r.get("item_id","")
        # Link directly to the item if we have an id, otherwise category page
        if item_id:
            link = f"{base_link}?id={item_id}"
        else:
            link = base_link
        name  = e(r.get("item_name",""))
        city  = e(r.get("item_city",""))
        extra = e(r.get("item_extra",""))
        ts    = str(r.get("viewed_at",""))[:16]
        cards += f"""
        <a href="{link}" style="text-decoration:none">
          <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;border:1px solid #E2E8F0;border-radius:10px;background:#fff;margin-bottom:8px;transition:background .15s" onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='#fff'">
            <div style="width:36px;height:36px;border-radius:50%;background:{col}18;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0">{icon}</div>
            <div style="flex:1;min-width:0">
              <div style="font-weight:700;font-size:13px;color:#1F2937;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{name}</div>
              <div style="font-size:11px;color:#9CA3AF;margin-top:2px">{itype.title()}{" · " + city if city else ""}{" · " + extra if extra else ""}</div>
            </div>
            <div style="font-size:11px;color:#D1D5DB;flex-shrink:0">{ts}</div>
          </div>
        </a>"""
    return f"""
    <div class="card" style="margin-bottom:20px">
      <div class="card-hdr" style="background:#0038A8">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        Recently Viewed
      </div>
      <div class="card-body">{cards}</div>
    </div>"""

def _flight_bookings_html(user):
    """Shows flight bookings — only visible if user actually has bookings."""
    if not user: return ""
    try:
        import db as _db
        bookings = _db.get_flight_bookings(user["id"])
    except Exception:
        bookings = []
    if not bookings:
        return ""  # Hide section entirely if no bookings
    STATUS_COL = {"Scheduled":"#1E40AF","Active":"#065F46","Landed":"#6B7280",
                  "Delayed":"#D97706","Cancelled":"#991B1B"}
    STATUS_BG  = {"Scheduled":"#DBEAFE","Active":"#D1FAE5","Landed":"#F1F5F9",
                  "Delayed":"#FEF3C7","Cancelled":"#FEE2E2"}
    rows_html = ""
    for b in bookings:
        sc  = STATUS_COL.get(b["status"], "#6B7280")
        sb  = STATUS_BG.get(b["status"],  "#F9FAFB")
        org = e(b["origin"].split("(")[0].strip())
        dst = e(b["destination"].split("(")[0].strip())
        rows_html += f"""
        <div style="border:1px solid #E2E8F0;border-radius:10px;padding:14px 16px;background:{sb};margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">
          <div style="display:flex;align-items:center;gap:12px">
            <div style="font-size:22px">&#9992;</div>
            <div>
              <div style="font-weight:800;font-size:14px;color:#1F2937">{org} &rarr; {dst}</div>
              <div style="font-size:12px;color:#6B7280;margin-top:3px">{e(b["airline"])} &bull; Dep: {e(b["dep_time"] or "—")} &bull; Arr: {e(b["arr_time"] or "—")}</div>
              <div style="font-size:11px;color:#9CA3AF;margin-top:2px">Saved {str(b["booked_at"])[:10]}</div>
            </div>
          </div>
          <span style="background:{sc}22;color:{sc};padding:5px 14px;border-radius:20px;font-size:11px;font-weight:700;white-space:nowrap">{e(b["status"]).upper()}</span>
        </div>"""
    return f"""
    <div class="card" style="margin-bottom:20px">
      <div class="card-hdr" style="background:#0038A8">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13"/><path d="M22 2L15 22 11 13 2 9l20-7z"/></svg>
        My Saved Flights ({len(bookings)})
      </div>
      <div class="card-body">
        <div style="font-size:12px;color:#6B7280;margin-bottom:12px;padding:8px 12px;background:#F8FAFC;border-radius:8px;border-left:3px solid #0038A8">
          &#9432; These flights were saved from our flight search. Confirm all details directly with your airline before travel.
        </div>
        {rows_html}
      </div>
    </div>"""


def _guide_feedback_modal():
    """Returns the guide rating/feedback modal HTML."""
    return """
    <!-- Guide Feedback Modal -->
    <div id="feedback-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;align-items:center;justify-content:center;backdrop-filter:blur(2px)">
      <div style="background:#fff;border-radius:16px;padding:28px;max-width:440px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,.3)">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
          <div style="font-size:18px;font-weight:800;color:#1F2937">Rate Your Guide</div>
          <button onclick="closeFeedback()" style="background:none;border:none;font-size:22px;cursor:pointer;color:#6B7280">&times;</button>
        </div>
        <div id="feedback-guide-name" style="font-size:14px;color:#6B7280;margin-bottom:16px"></div>
        <input type="hidden" id="feedback-booking-id"/>
        <input type="hidden" id="feedback-guide-id"/>
        <div style="margin-bottom:16px">
          <label style="font-size:12px;font-weight:700;color:#374151;text-transform:uppercase;letter-spacing:.3px">Your Rating</label>
          <div style="display:flex;gap:8px;margin-top:8px" id="star-row">
            <span class="fb-star" data-v="1" onclick="setRating(1)" style="font-size:32px;cursor:pointer;color:#D1D5DB">&#9733;</span>
            <span class="fb-star" data-v="2" onclick="setRating(2)" style="font-size:32px;cursor:pointer;color:#D1D5DB">&#9733;</span>
            <span class="fb-star" data-v="3" onclick="setRating(3)" style="font-size:32px;cursor:pointer;color:#D1D5DB">&#9733;</span>
            <span class="fb-star" data-v="4" onclick="setRating(4)" style="font-size:32px;cursor:pointer;color:#D1D5DB">&#9733;</span>
            <span class="fb-star" data-v="5" onclick="setRating(5)" style="font-size:32px;cursor:pointer;color:#D1D5DB">&#9733;</span>
          </div>
          <div id="rating-label" style="font-size:12px;color:#9CA3AF;margin-top:4px">Click a star to rate</div>
        </div>
        <div style="margin-bottom:16px">
          <label style="font-size:12px;font-weight:700;color:#374151;text-transform:uppercase;letter-spacing:.3px">Your Feedback</label>
          <textarea id="feedback-text" rows="3" placeholder="Share your experience with this guide..." style="width:100%;margin-top:6px;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:8px;font-size:13px;font-family:inherit;resize:none;outline:none;box-sizing:border-box"></textarea>
        </div>
        <div style="display:flex;gap:10px">
          <button class="btn" style="flex:1;background:#0038A8;color:#fff;padding:11px;font-weight:700" onclick="submitFeedback()">&#10003; Submit Review</button>
          <button class="btn-outline" style="flex:1;padding:11px" onclick="closeFeedback()">Cancel</button>
        </div>
      </div>
    </div>
    <script>
    var _fbRating = 0;
    var RATING_LABELS = ['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent'];
    function openFeedback(bookingId, guideId, guideName) {{
      _fbRating = 0;
      document.getElementById('feedback-booking-id').value = bookingId;
      document.getElementById('feedback-guide-id').value = guideId;
      document.getElementById('feedback-guide-name').textContent = 'Guide: ' + guideName;
      document.getElementById('feedback-text').value = '';
      setRating(0);
      document.getElementById('feedback-modal').style.display = 'flex';
    }}
    function closeFeedback() {{
      document.getElementById('feedback-modal').style.display = 'none';
    }}
    function setRating(val) {{
      _fbRating = val;
      var stars = document.querySelectorAll('.fb-star');
      stars.forEach(function(s) {{
        s.style.color = parseInt(s.getAttribute('data-v')) <= val ? '#F59E0B' : '#D1D5DB';
      }});
      document.getElementById('rating-label').textContent = val ? (val + ' star — ' + RATING_LABELS[val]) : 'Click a star to rate';
    }}
    function submitFeedback() {{
      var bookingId = document.getElementById('feedback-booking-id').value;
      var guideId   = document.getElementById('feedback-guide-id').value;
      var comment   = document.getElementById('feedback-text').value.trim();
      if (!_fbRating) {{ alert('Please select a rating.'); return; }}
      var form = document.createElement('form');
      form.method = 'post';
      form.action = '/submit-review';
      var fields = {{ booking_id: bookingId, guide_id: guideId, rating: _fbRating, comment: comment }};
      Object.keys(fields).forEach(function(k) {{
        var inp = document.createElement('input');
        inp.type = 'hidden'; inp.name = k; inp.value = fields[k];
        form.appendChild(inp);
      }});
      document.body.appendChild(form);
      form.submit();
    }}
    </script>"""


def render(user=None, msg="", err="", tab="profile"):
    if not user:
        return build_shell("Profile", '<div class="page-wrap"><div class="card"><div class="card-body" style="text-align:center;padding:40px"><div style="font-size:40px;margin-bottom:16px">&#128100;</div><div style="font-size:18px;font-weight:700;margin-bottom:12px">Please log in to view your profile</div><a href="/login.py"><button class="btn" style="background:#0038A8;color:#fff;padding:10px 28px">Log In</button></a></div></div></div>', "home", user=None)

    fname    = e(user.get("fname",""))
    lname    = e(user.get("lname",""))
    email    = e(user.get("email",""))
    initials = (fname[0] if fname else "?").upper()
    photo_url = user.get("photo_url","")

    # ── PHOTO REQUIRED banner ──────────────────────────────────────────────
    photo_missing = not photo_url
    photo_banner = ""
    if photo_missing:
        photo_banner = """
        <div style="background:linear-gradient(135deg,#FEF3C7,#FDE68A);border:2px solid #F59E0B;
                    border-radius:12px;padding:16px 20px;margin-bottom:20px;
                    display:flex;align-items:flex-start;gap:14px">
          <div style="font-size:28px;flex-shrink:0">📷</div>
          <div>
            <div style="font-weight:800;font-size:15px;color:#92400E;margin-bottom:4px">
              Profile photo required
            </div>
            <div style="font-size:13px;color:#92400E;line-height:1.6">
              A profile photo is <strong>mandatory</strong> to use ATLAS fully.
              Please upload a photo below to unlock all features.
            </div>
          </div>
        </div>"""

    msg_html = f'<div style="background:#D1FAE5;color:#065F46;padding:12px 16px;border-radius:8px;margin-bottom:16px;font-weight:600">&#10003; {msg}</div>' if msg else ""
    err_html = f'<div style="background:#FEE2E2;color:#CE1126;padding:12px 16px;border-radius:8px;margin-bottom:16px;font-weight:600">&#9888; {err}</div>' if err else ""

    # Load guide bookings
    current_bookings = []
    history_bookings = []
    try:
        import guide_db
        today = datetime.date.today().isoformat()
        rows = guide_db.get_bookings_by_tourist_email(email)
        for r in rows:
            d = dict(r)
            if "fname" in d and "gfname" not in d:
                d["gfname"] = d.pop("fname")
            if "lname" in d and "glname" not in d:
                d["glname"] = d.pop("lname")
            if d["status"] in ("cancelled", "rejected", "completed"):
                history_bookings.append(d)
            elif d["tour_date"] < today and d["status"] == "accepted":
                history_bookings.append(d)
            else:
                current_bookings.append(d)
    except Exception:
        pass

    STATUS_COLOR = {"pending":"#D97706","accepted":"#059669","rejected":"#DC2626","cancelled":"#6B7280","rescheduled":"#2563EB","completed":"#7C3AED"}
    STATUS_BG    = {"pending":"#FFFBEB","accepted":"#ECFDF5","rejected":"#FEF2F2","cancelled":"#F9FAFB","rescheduled":"#EFF6FF","completed":"#F5F3FF"}

    def booking_card(b):
        sc = STATUS_COLOR.get(b["status"],"#6B7280")
        sb = STATUS_BG.get(b["status"],"#F9FAFB")
        gname = e(f'{b.get("gfname","")} {b.get("glname","")}'.strip() or "Tour Guide")
        guide_id_val = b.get("guide_id","")
        booking_id_val = b.get("id","")
        can_review = b["status"] == "completed" and not b.get("reviewed")
        review_btn = (
            f'<button onclick="openFeedback(\'{booking_id_val}\',\'{guide_id_val}\',\'{gname}\')" '
            f'style="margin-top:8px;padding:7px 14px;background:#0038A8;color:#fff;border:none;border-radius:8px;font-size:12px;font-weight:700;cursor:pointer">&#9733; Leave a Review</button>'
            if can_review else ""
        )
        return f"""
        <div style="border:1px solid #E2E8F0;border-radius:12px;padding:16px 18px;background:{sb};margin-bottom:12px">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">
            <div>
              <div style="font-weight:800;font-size:15px;color:#1F2937">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0038A8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                {gname}
              </div>
              <div style="font-size:12px;color:#6B7280;margin-top:4px;display:flex;gap:12px;flex-wrap:wrap">
                <span><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> {e(b["tour_date"])}</span>
                <span>&#128101; {e(b["pax"])} pax</span>
                <span>&#128196; {e(b.get("package_title","Custom Tour") or "Custom Tour")}</span>
                {f'<span>&#128205; {e(b.get("gcity",""))}</span>' if b.get("gcity") else ""}
              </div>
              {f'<div style="font-size:12px;color:#4B5563;margin-top:6px;font-style:italic;background:rgba(0,0,0,.03);padding:6px 10px;border-radius:6px">"{e(b["notes"])}"</div>' if b.get("notes") else ""}
              {f'<div style="font-size:12px;color:#2563EB;margin-top:4px">Guide note: {e(b["guide_notes"])}</div>' if b.get("guide_notes") else ""}
              {review_btn}
            </div>
            <span style="background:{sc}22;color:{sc};padding:5px 14px;border-radius:20px;font-size:11px;font-weight:700;white-space:nowrap">{e(b["status"]).upper()}</span>
          </div>
        </div>"""

    if current_bookings:
        cur_html = "".join(booking_card(b) for b in current_bookings)
    else:
        cur_html = '<div style="text-align:center;padding:32px;color:#9CA3AF"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin:0 auto 10px;display:block"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg><div style="font-weight:700">No active bookings</div><div style="font-size:12px;margin-top:4px"><a href="/guides.py" style="color:#0038A8;font-weight:600">Find a tour guide</a></div></div>'

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

    # 2FA section — just says Enable/Disable
    tfa_enabled = user.get("totp_enabled")
    tfa_label = "Disable 2FA" if tfa_enabled else "Enable 2FA"
    tfa_status = "&#10003; Enabled — your account is protected with 2FA" if tfa_enabled else "Not enabled — add an extra layer of security to your account"
    tfa_btn_style = "background:#FEE2E2;color:#DC2626" if tfa_enabled else "background:#0038A8;color:#fff"

    phone    = e(user.get("phone","") or "")

    body = f"""
    <div class="page-wrap" style="max-width:1100px;margin:0 auto">
      <div style="margin-bottom:24px">
        <div class="section-title">My Profile</div>
        <div class="section-sub">Manage your tourist account details</div>
      </div>
      {photo_banner}{msg_html}{err_html}

      <!-- Two-column layout -->
      <div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;align-items:start">

      <!-- LEFT COLUMN: Photo + Account Info + Password + 2FA -->
      <div>

      <!-- Profile Photo Card -->
      <div class="card" style="margin-bottom:20px{';border:2px solid #F59E0B;box-shadow:0 0 0 4px #FEF3C755' if photo_missing else ''}">
        <div class="card-hdr" style="background:{'#D97706' if photo_missing else '#0038A8'}">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
          Profile Photo {'<span style="background:#fff;color:#D97706;font-size:10px;font-weight:800;padding:2px 8px;border-radius:10px;margin-left:8px">REQUIRED</span>' if photo_missing else ''}
        </div>
        <div class="card-body" style="display:flex;align-items:center;gap:20px;flex-wrap:wrap">
          <div style="flex-shrink:0">
            {f'<img src="{photo_url}" style="width:80px;height:80px;border-radius:50%;object-fit:cover;border:3px solid #E2E8F0"/>' if photo_url else f'<div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#F59E0B,#D97706);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;color:#fff;border:3px dashed #FCD34D">{initials}</div>'}
          </div>
          <div style="flex:1;min-width:180px">
            <div style="font-size:20px;font-weight:800;color:#1F2937;margin-bottom:2px">{fname} {lname}</div>
            <div style="font-size:13px;color:#6B7280;margin-bottom:10px">&#9993; {email}</div>
            {'<div style="font-size:12px;color:#D97706;font-weight:700;margin-bottom:10px;display:flex;align-items:center;gap:6px"><i class="fa-solid fa-circle-exclamation"></i> No photo uploaded yet — required to use ATLAS</div>' if photo_missing else ''}
            <form method="post" action="/profile/photo" enctype="multipart/form-data" id="photo-form" style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
              <label style="display:flex;align-items:center;gap:6px;padding:7px 12px;border:1.5px {'dashed #F59E0B;background:#FFFBEB' if photo_missing else 'dashed #CBD5E1;background:#F8FAFC'};border-radius:8px;cursor:pointer;font-size:13px;color:#6B7280" onmouseover="this.style.borderColor='#0038A8'" onmouseout="this.style.borderColor='{'#F59E0B' if photo_missing else '#CBD5E1'}'">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="{'#D97706' if photo_missing else '#94A3B8'}" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                <span id="t-photo-lbl">Choose photo</span>
                <input type="file" name="photo_file" accept="image/jpeg,image/png,image/webp"
                       style="display:none" id="photo-input"
                       onchange="handlePhotoSelect(this)"/>
              </label>
              <button class="btn" type="submit" id="photo-upload-btn"
                style="background:{'#D97706' if photo_missing else '#0038A8'};color:#fff;padding:8px 18px;font-size:13px;font-weight:700">
                {'<i class="fa-solid fa-camera"></i> Upload Photo' if photo_missing else 'Upload'}
              </button>
            </form>
            <div style="font-size:11px;color:#9CA3AF;margin-top:5px">JPG, PNG or WEBP · Max 3 MB</div>
            <!-- Preview before upload -->
            <div id="photo-preview-wrap" style="display:none;margin-top:10px;align-items:center;gap:10px">
              <img id="photo-preview" style="width:52px;height:52px;border-radius:50%;object-fit:cover;border:2px solid #E2E8F0"/>
              <div style="font-size:12px;color:#059669;font-weight:600"><i class="fa-solid fa-check"></i> Ready to upload</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Account Info -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Account Information
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px">
            <div>
              <label class="lbl">First Name</label>
              <div style="padding:10px 12px;background:#F3F4F6;border:1.5px solid #E2E8F0;border-radius:8px;font-size:14px;color:#6B7280">{fname}</div>
              <div style="font-size:11px;color:#9CA3AF;margin-top:3px">Cannot be changed</div>
            </div>
            <div>
              <label class="lbl">Last Name</label>
              <div style="padding:10px 12px;background:#F3F4F6;border:1.5px solid #E2E8F0;border-radius:8px;font-size:14px;color:#6B7280">{lname}</div>
              <div style="font-size:11px;color:#9CA3AF;margin-top:3px">Cannot be changed</div>
            </div>
          </div>
          <div style="margin-bottom:14px">
            <label class="lbl">Email Address</label>
            <div style="padding:10px 12px;background:#F3F4F6;border:1.5px solid #E2E8F0;border-radius:8px;font-size:14px;color:#6B7280">{email}</div>
            <div style="font-size:11px;color:#9CA3AF;margin-top:3px">Cannot be changed</div>
          </div>
          <form method="post" action="/profile/update">
            <input type="hidden" name="action" value="update_contact"/>
            <div style="margin-bottom:16px">
              <label class="lbl">Contact Number</label>
              <input class="inp" name="phone" type="tel" value="{phone}" placeholder="+63 9XX XXX XXXX" style="width:100%"/>
            </div>
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

      <!-- Two-Factor Authentication -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          Two-Factor Authentication
        </div>
        <div class="card-body" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px">
          <div>
            <div style="font-weight:700;font-size:14px;color:#1F2937;margin-bottom:4px">Google Authenticator (2FA)</div>
            <div style="font-size:13px;color:#6B7280">{tfa_status}</div>
          </div>
          <a href="/setup-2fa">
            <button class="btn" style="{tfa_btn_style};padding:9px 20px;font-size:13px">{tfa_label}</button>
          </a>
        </div>
      </div>

      </div><!-- end LEFT COLUMN -->

      <!-- RIGHT COLUMN: Flights + Tour Guide Bookings + Recently Viewed -->
      <div>

      <!-- My Saved Flights (only if bookings exist) -->
      {_flight_bookings_html(user)}

      <!-- My Tour Guide Bookings -->
      {bookings_section}

      <!-- Recently Viewed -->
      {_recently_viewed_html(email)}

      </div><!-- end RIGHT COLUMN -->
      </div><!-- end grid -->

    </div>
    {_guide_feedback_modal()}
    <script>
    function handlePhotoSelect(input) {{
      var lbl = document.getElementById('t-photo-lbl');
      var wrap = document.getElementById('photo-preview-wrap');
      var prev = document.getElementById('photo-preview');
      var btn  = document.getElementById('photo-upload-btn');
      if (input.files && input.files[0]) {{
        var f = input.files[0];
        if (f.size > 3 * 1024 * 1024) {{
          alert('File too large. Maximum size is 3 MB.');
          input.value = '';
          lbl.textContent = 'Choose photo';
          wrap.style.display = 'none';
          if (btn) btn.disabled = true;
          return;
        }}
        lbl.textContent = f.name.length > 22 ? f.name.slice(0,20)+'...' : f.name;
        if (btn) btn.disabled = false;
        var reader = new FileReader();
        reader.onload = function(ev) {{
          prev.src = ev.target.result;
          wrap.style.display = 'flex';
        }};
        reader.readAsDataURL(f);
      }}
    }}
    // Disable upload button until a file is chosen
    (function() {{
      var btn = document.getElementById('photo-upload-btn');
      var inp = document.getElementById('photo-input');
      if (btn && inp) {{
        btn.disabled = true;
        inp.addEventListener('change', function() {{
          btn.disabled = !inp.files || !inp.files[0];
        }});
      }}
      // Validate on submit
      var form = document.getElementById('photo-form');
      if (form) {{
        form.addEventListener('submit', function(e) {{
          if (!inp || !inp.files || !inp.files[0]) {{
            e.preventDefault();
            alert('Please select a photo file first.');
          }}
        }});
      }}
    }})();
    </script>"""
    return build_shell("My Profile", body, "profile", user=user)
