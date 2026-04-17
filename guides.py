import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tourist_ui import build_shell
import guide_db

def get_all_guides_combined(city="All"):
    try:
        db_guides = guide_db.get_public_guides(city if city != "All" else None)
        avg_data = {g["id"]: guide_db.get_avg_rating(g["id"]) for g in db_guides}
        completed_data = {g["id"]: guide_db.get_completed_tours_count(g["id"]) for g in db_guides}
        converted = []
        for g in db_guides:
            pkgs = guide_db.get_packages(g["id"])
            avg, cnt = avg_data.get(g["id"], (4.5, 0))
            converted.append({
                "name":     f'{g["fname"]} {g["lname"]}',
                "city":     g["city"],
                "lang":     g.get("languages", "EN, FIL"),
                "rate":     g.get("rate", "P1,500/day"),
                "rating":   avg if avg > 0 else 4.5,
                "tours":    completed_data.get(g["id"], 0),
                "spec":     g.get("speciality", "General Tours"),
                "avail":    g.get("availability", "Mon-Sun"),
                "bio":      g.get("bio") or "Registered local tour guide.",
                "pkgs":     [f'{p["title"]} - {p["price"]}' for p in pkgs] or ["Custom Tour Available"],
                "guide_id": g["id"],
                "photo_url": g.get("photo_url", ""),
            })
        return converted
    except:
        return []

COLORS = ["#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8"]

def _card(g, i):
    col   = COLORS[i % len(COLORS)]
    name  = g["name"].replace("'","&#39;")
    city  = g["city"]
    full  = int(round(g["rating"]))
    stars = "&#9733;" * full + "&#9734;" * (5 - full)
    pkgs  = "".join(
        f'<div style="font-size:12px;color:#374151;padding:5px 0;border-bottom:1px solid #F3F4F6;display:flex;justify-content:space-between">'
        f'<span>&#10003; {p}</span></div>'
        for p in g["pkgs"]
    )
    avail_color = "#065F46" if "Sun" in g["avail"] or "Mon-Sun" in g["avail"] else "#C8930A"
    guide_id_str = str(g.get("guide_id", g.get("id","")))
    avatar = (
        f'<img src="{g["photo_url"]}" style="width:64px;height:64px;border-radius:50%;object-fit:cover;border:3px solid rgba(255,255,255,.6);margin:0 auto 10px;display:block"/>'
        if g.get("photo_url") else
        f'<div style="width:64px;height:64px;border-radius:50%;background:rgba(255,255,255,.25);border:3px solid rgba(255,255,255,.6);display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:900;color:#fff;margin:0 auto 10px">{g["name"][0]}</div>'
    )
    return (
        '<div class="grid-card" style="display:flex;flex-direction:column">'
        f'<div class="grid-card-top" style="background:linear-gradient(135deg,{col},{col}bb);position:relative">'
        + avatar +
        f'<div style="font-weight:800;font-size:16px;color:#fff;margin-bottom:3px">{g["name"]}</div>'
        f'<div style="font-size:12px;color:rgba(255,255,255,.85);margin-bottom:6px">{g["spec"]}</div>'
        f'<span style="background:rgba(255,255,255,.2);color:#fff;font-size:11px;padding:2px 10px;border-radius:20px">{city}</span>'
        '</div>'
        '<div class="grid-card-body" style="flex:1;display:flex;flex-direction:column">'
        f'<div style="color:#F59E0B;font-size:13px;margin-bottom:6px">{stars} <span style="color:#9CA3AF;font-size:12px">{g["rating"]} ({g["tours"]} tours)</span></div>'
        f'<div style="font-size:12px;color:#6B7280;margin-bottom:2px">&#127760; {g["lang"]}</div>'
        f'<div style="font-size:12px;margin-bottom:2px"><span style="background:{avail_color}22;color:{avail_color};padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600">&#128197; {g["avail"]}</span></div>'
        f'<div style="font-size:13px;color:#4B5563;margin:8px 0;line-height:1.5;font-style:italic">&ldquo;{g["bio"]}&rdquo;</div>'
        f'<div style="font-size:18px;font-weight:800;color:{col};margin-bottom:8px">{g["rate"]}</div>'
        f'<div style="margin-bottom:14px;border:1px solid #E5E7EB;border-radius:8px;overflow:hidden"><div style="background:#F9FAFB;padding:6px 10px;font-size:11px;font-weight:700;color:#6B7280;text-transform:uppercase">Packages</div>{pkgs}</div>'
        '<div style="margin-top:auto;display:flex;flex-direction:column;gap:7px">'
        f'<button class="btn" style="background:{col};color:#fff;width:100%;padding:10px;font-size:14px;font-weight:700"'
        f' data-gid="{guide_id_str}" data-name="{g["name"]}" data-city="{g["city"]}" data-rate="{g["rate"]}"'
        f' onclick="openBookingModalFromBtn(this)">&#128197; Book This Guide</button>'
        f'<button class="btn-outline" style="width:100%;padding:8px;color:{col};border-color:{col}"'
        f' data-gid="{guide_id_str}" data-name="{g["name"]}" data-city="{g["city"]}" data-rate="{g["rate"]}"'
        f' data-spec="{g["spec"]}" data-bio="{g["bio"]}" data-lang="{g["lang"]}" data-avail="{g["avail"]}"'
        f' data-rating="{g["rating"]}" data-tours="{g["tours"]}"'
        f' onclick="openProfileModalFromBtn(this)">&#128100; View Full Profile</button>'
        '</div></div></div>'
    )


def render(filter_city="All", filter_lang="All", user=None, booked=False):
    try:
        all_db_guides = guide_db.get_public_guides()
        cities = ["All"] + sorted(set(g["city"] for g in all_db_guides))
    except:
        cities = ["All"]

    city_opts = "".join(f'<option {"selected" if c==filter_city else ""}>{c}</option>' for c in cities)
    lang_opts = "".join(f'<option {"selected" if l==filter_lang else ""}>{l}</option>' for l in ["All","EN","FIL","ES","IL"])
    combined  = get_all_guides_combined(filter_city)
    filtered  = [g for g in combined if (filter_lang=="All" or filter_lang in g["lang"])]
    guide_html = "".join(_card(g,i) for i,g in enumerate(filtered)) if filtered else (
        '<div class="guide-empty"><div style="font-size:48px;margin-bottom:12px">&#129517;</div>'
        '<div style="font-weight:700;font-size:18px">No Tour Guides Found</div>'
        '<div style="color:#6B7280;font-size:14px;margin-top:8px">No guides have registered yet. Check back soon!</div></div>'
    )
    count = f"{len(filtered)} guide(s) available" if filtered else "0 guides found"

    booked_banner = '<div style="background:#D1FAE5;color:#065F46;padding:14px 20px;border-radius:10px;margin-bottom:20px;font-weight:700;font-size:15px">&#10003; Booking submitted! Your guide will confirm your booking shortly.</div>' if booked else ""
    body = f"""
    <div class="page-wrap">
      {booked_banner}
      <div style="margin-bottom:22px">
        <div class="section-title">Tour Guide Booking</div>
        <div class="section-sub">Book a verified local guide for your Luzon adventure</div>
      </div>

      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8"><span>Find Your Guide</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div><label class="lbl">City</label><select class="inp" name="city" style="width:180px">{city_opts}</select></div>
            <div><label class="lbl">Language</label><select class="inp" name="lang" style="width:140px">{lang_opts}</select></div>
            <button class="btn" style="background:#0038A8;color:#fff" type="submit">Find Guides</button>
          </form>
        </div>
      </div>

      <div style="font-size:13px;color:#6B7280;margin-bottom:16px">{count}</div>
      <div class="page-grid3">{guide_html}</div>
    </div>

    <!-- Booking Modal -->
    <div id="booking-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;align-items:center;justify-content:center">
      <div style="background:#fff;border-radius:16px;padding:28px;max-width:440px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,.3)">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
          <div style="font-size:18px;font-weight:800;color:#1F2937">Book a Tour Guide</div>
          <button onclick="closeBookingModal()" style="background:none;border:none;font-size:22px;cursor:pointer;color:#6B7280">&times;</button>
        </div>
        <div id="booking-guide-info" style="background:#F9FAFB;border-radius:10px;padding:12px;margin-bottom:16px;font-size:14px;color:#374151"></div>
        <div style="display:flex;flex-direction:column;gap:10px">
          <div><label class="lbl">Your Name</label><input class="inp" id="bk-name" placeholder="Juan Dela Cruz" style="width:100%"/></div>
          <div><label class="lbl">Contact Number</label><input class="inp" id="bk-phone" placeholder="09XX-XXX-XXXX" style="width:100%"/></div>
          <div><label class="lbl">Tour Date</label><input class="inp" type="date" id="bk-date" style="width:100%"/></div>
          <div><label class="lbl">Select Package</label>
            <select class="inp" id="bk-pkg" style="width:100%">
              <option>Half Day Tour</option><option>Full Day Tour</option><option>Private Group Tour</option>
            </select>
          </div>
          <div><label class="lbl">Special Requests</label><textarea class="inp" id="bk-notes" rows="2" placeholder="Any special requests..." style="width:100%;resize:none"></textarea></div>
        </div>
        <div style="display:flex;gap:10px;margin-top:18px">
          <button class="btn" style="flex:1;background:#0038A8;color:#fff;padding:11px;font-weight:700" onclick="confirmBooking()">&#10003; Confirm Booking</button>
          <button class="btn-outline" style="flex:1;padding:11px" onclick="closeBookingModal()">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Profile Modal -->
    <div id="profile-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;align-items:center;justify-content:center">
      <div style="background:#fff;border-radius:16px;padding:28px;max-width:460px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,.3)">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
          <div style="font-size:18px;font-weight:800;color:#1F2937">Guide Profile</div>
          <button onclick="closeProfileModal()" style="background:none;border:none;font-size:22px;cursor:pointer;color:#6B7280">&times;</button>
        </div>
        <div id="profile-content"></div>
        <button class="btn" id="profile-book-btn" style="width:100%;background:#0038A8;color:#fff;padding:11px;margin-top:16px;font-weight:700">&#128197; Book This Guide</button>
      </div>
    </div>

    <script>
    var _bookingGuide   = "";
    var _bookingCity    = "";
    var _bookingRate    = "";
    var _bookingGuideId = "";

    function openBookingModalFromBtn(btn) {{
      _bookingGuideId = btn.getAttribute("data-gid")  || "";
      _bookingGuide   = btn.getAttribute("data-name") || "";
      _bookingCity    = btn.getAttribute("data-city") || "";
      _bookingRate    = btn.getAttribute("data-rate") || "";
      console.log("BOOKING: guide_id=" + _bookingGuideId + " name=" + _bookingGuide);
      document.getElementById("booking-guide-info").innerHTML =
        "<strong>&#128100; " + _bookingGuide + "</strong> &mdash; " + _bookingCity +
        "<br>Rate: <strong style='color:#0038A8'>" + _bookingRate + "</strong>";
      document.getElementById("booking-modal").style.display = "flex";
    }}
    function openProfileModalFromBtn(btn) {{
      var gid   = btn.getAttribute("data-gid")    || "";
      var name  = btn.getAttribute("data-name")   || "";
      var city  = btn.getAttribute("data-city")   || "";
      var rate  = btn.getAttribute("data-rate")   || "";
      var spec  = btn.getAttribute("data-spec")   || "";
      var bio   = btn.getAttribute("data-bio")    || "";
      var lang  = btn.getAttribute("data-lang")   || "";
      var avail = btn.getAttribute("data-avail")  || "";
      var rating= btn.getAttribute("data-rating") || "";
      var tours = btn.getAttribute("data-tours")  || "";
      openProfileModal(name, city, spec, bio, lang, avail, rate, rating, tours, gid);
    }}
    function openBookingModal(name, city, rate, guideId) {{
      if(typeof ATLAS_LOGGED_IN!=='undefined' && !ATLAS_LOGGED_IN){{ window.location='/login.py'; return; }}
      _bookingGuide = name; _bookingCity = city; _bookingRate = rate; _bookingGuideId = guideId || "";
      document.getElementById("booking-guide-info").innerHTML =
        "<strong>&#128100; " + name + "</strong> &mdash; " + city + "<br>Rate: <strong style='color:#0038A8'>" + rate + "</strong>";
      document.getElementById("booking-modal").style.display = "flex";
    }}
    function closeBookingModal() {{ document.getElementById("booking-modal").style.display = "none"; }}

    function confirmBooking() {{
      var name  = document.getElementById("bk-name").value.trim();
      var phone = document.getElementById("bk-phone").value.trim();
      var date  = document.getElementById("bk-date").value;
      var pkg   = document.getElementById("bk-pkg").value;
      var notes = document.getElementById("bk-notes").value.trim();
      if (!name || !phone || !date) {{ alert("Please fill in your name, contact number, and date."); return; }}
      var form = document.createElement("form");
      form.method = "post";
      form.action = "/book-guide";
      var fields = {{
        guide_name: _bookingGuide,
        guide_city: _bookingCity,
        guide_rate: _bookingRate,
        guide_id:   _bookingGuideId,
        tourist_name: name,
        tourist_phone: phone,
        tour_date: date,
        package_title: pkg,
        notes: notes
      }};
      Object.keys(fields).forEach(function(k) {{
        var inp = document.createElement("input");
        inp.type = "hidden"; inp.name = k; inp.value = fields[k];
        form.appendChild(inp);
      }});
      document.body.appendChild(form);
      form.submit();
    }}

    function openProfileModal(name, city, spec, bio, lang, avail, rate, rating, tours, guideId) {{
      document.getElementById("profile-content").innerHTML =
        '<div style="text-align:center;margin-bottom:16px">' +
        '<div style="width:72px;height:72px;border-radius:50%;background:#0038A8;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;color:#fff;margin:0 auto 10px">' + name[0] + '</div>' +
        '<div style="font-size:20px;font-weight:800">' + name + '</div>' +
        '<div style="color:#6B7280;font-size:13px">' + spec + '</div></div>' +
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px">' +
        '<div style="background:#F3F4F6;border-radius:8px;padding:10px;text-align:center"><div style="font-size:18px;font-weight:800;color:#0038A8">&#11088; ' + rating + '</div><div style="font-size:11px;color:#6B7280">Rating</div></div>' +
        '<div style="background:#F3F4F6;border-radius:8px;padding:10px;text-align:center"><div style="font-size:18px;font-weight:800;color:#CE1126">' + tours + '</div><div style="font-size:11px;color:#6B7280">Tours Done</div></div>' +
        '</div>' +
        '<div style="font-size:13px;color:#374151;margin-bottom:12px;line-height:1.6;background:#FFFBEB;border-left:3px solid #C8930A;padding:10px">' + bio + '</div>' +
        '<div style="font-size:13px;color:#6B7280;margin-bottom:4px">&#127760; Languages: <strong>' + lang + '</strong></div>' +
        '<div style="font-size:13px;color:#6B7280;margin-bottom:4px">&#128197; Available: <strong>' + avail + '</strong></div>' +
        '<div style="font-size:13px;color:#6B7280">&#128205; City: <strong>' + city + '</strong></div>' +
        '<div style="font-size:20px;font-weight:800;color:#0038A8;margin-top:10px">' + rate + '</div>';
      document.getElementById("profile-book-btn").onclick = function() {{
        closeProfileModal(); openBookingModal(name, city, rate, guideId);
      }};
      document.getElementById("profile-modal").style.display = "flex";
    }}
    function closeProfileModal() {{ document.getElementById("profile-modal").style.display = "none"; }}
    </script>
    """
    return build_shell("Tour Guides", body, "guides", user=user)
