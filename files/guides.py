import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import GUIDES

EXTRA_GUIDES = [
    {"name": "Carlo Mendoza",   "city": "Tagaytay",    "lang": "EN, FIL",     "rate": "P1,800/day", "rating": 4.7, "tours": 63,  "spec": "Volcano & Nature",        "avail": "Mon-Sun", "bio": "Tagaytay native with expertise in Taal Volcano day trips and Highlands tours. Perfect for families.",      "pkgs": ["Taal Volcano Day - P1,500","Sky Ranch + Picnic Grove - P1,200","Full Tagaytay Tour - P1,800"]},
    {"name": "Elena Cruz",      "city": "Tagaytay",    "lang": "EN, FIL",     "rate": "P1,600/day", "rating": 4.5, "tours": 41,  "spec": "Food & Scenic Tours",     "avail": "Wed-Mon", "bio": "Food blogger turned guide. Knows all the best bulalo spots and scenic viewpoints in Tagaytay.",            "pkgs": ["Food Trip Tour - P1,000","Scenic Views Tour - P1,200","Full Day - P1,600"]},
    {"name": "Pedro Villanueva","city": "Albay",        "lang": "EN, FIL",     "rate": "P2,000/day", "rating": 4.8, "tours": 97,  "spec": "Mayon Volcano & ATV",     "avail": "Mon-Sat", "bio": "Certified Mayon Volcano guide. Leads ATV tours on lava trails and sunrise viewing expeditions.",           "pkgs": ["ATV Lava Trail - P1,500","Cagsawa Ruins Tour - P900","Full Albay Day - P2,000"]},
    {"name": "Rosa Bicol",      "city": "Albay",        "lang": "EN, FIL",     "rate": "P1,700/day", "rating": 4.6, "tours": 55,  "spec": "Culture & Food Tours",    "avail": "Tue-Sun", "bio": "Bicolana guide specializing in local culture, cuisine (Bicol Express!), and island hopping trips.",         "pkgs": ["Bicolano Food Tour - P1,200","Island Hopping - P1,500","Cultural Walk - P900"]},
    {"name": "Noel Pangasinan", "city": "Pangasinan",  "lang": "EN, FIL",     "rate": "P1,900/day", "rating": 4.7, "tours": 78,  "spec": "Hundred Islands & Beach", "avail": "Mon-Sun", "bio": "Born in Alaminos, expert in Hundred Islands boat tours, Bolinao Falls, and Pangasinan bangus culture.",   "pkgs": ["Hundred Islands - P1,500","Bolinao Falls - P1,200","Full Province Tour - P1,900"]},
    {"name": "Carla Santos",    "city": "Pangasinan",  "lang": "EN, FIL",     "rate": "P1,500/day", "rating": 4.4, "tours": 34,  "spec": "Pilgrimage & Heritage",   "avail": "Mon-Fri", "bio": "Specialist in religious and heritage tours including Our Lady of Manaoag and ancestral houses.",           "pkgs": ["Manaoag Pilgrimage - P900","Heritage Walk - P1,200","Full Day - P1,500"]},
    {"name": "Danilo Bataan",   "city": "Bataan",       "lang": "EN, FIL",     "rate": "P1,800/day", "rating": 4.9, "tours": 112, "spec": "War History & Corregidor","avail": "Mon-Sun", "bio": "Military history expert. Led hundreds of tours to Corregidor, Mt. Samat, and Death March sites.",         "pkgs": ["Corregidor Island - P2,200","Mt. Samat Shrine - P1,000","Full Bataan History - P1,800"]},
    {"name": "Grace Mariveles", "city": "Bataan",       "lang": "EN, FIL",     "rate": "P1,600/day", "rating": 4.5, "tours": 48,  "spec": "Eco & Beach Tours",       "avail": "Thu-Tue", "bio": "Eco-tourism advocate specializing in Pawikan conservation tours, mangrove forests, and beach hopping.",    "pkgs": ["Pawikan Tour - P900","Las Casas Heritage - P1,500","Beach Eco Tour - P1,600"]},
]

ALL_GUIDES = GUIDES + EXTRA_GUIDES

def get_all_guides_combined(city="All"):
    import guide_db
    try:
        db_guides = guide_db.get_public_guides(city if city != "All" else None)
        avg_data = {g["id"]: guide_db.get_avg_rating(g["id"]) for g in db_guides}
        converted = []
        for g in db_guides:
            pkgs = guide_db.get_packages(g["id"])
            avg, cnt = avg_data.get(g["id"], (4.5, 0))
            converted.append({
                "name":   f'{g["fname"]} {g["lname"]}',
                "city":   g["city"],
                "lang":   g.get("languages","EN, FIL"),
                "rate":   g.get("rate","P1,500/day"),
                "rating": avg if avg > 0 else 4.5,
                "tours":  cnt,
                "spec":   g.get("speciality","General Tours"),
                "avail":  g.get("availability","Mon-Sun"),
                "bio":    g.get("bio","Registered local tour guide."),
                "pkgs":   [f'{p["title"]} - {p["price"]}' for p in pkgs] or ["Custom Tour Available"],
                "guide_id": g["id"],
            })
        static = [g for g in ALL_GUIDES if city == "All" or g["city"] == city]
        return converted + static
    except:
        return [g for g in ALL_GUIDES if city == "All" or g["city"] == city]

COLORS = ["#0038A8","#CE1126","#C8930A","#6B21A8","#0077B6","#065F46","#B45309","#047857","#9D174D","#0369A1","#7C3AED","#DC2626"]

def _card(g, i):
    col   = COLORS[i % len(COLORS)]
    name  = g["name"].replace("'","&#39;")
    city  = g["city"]
    full  = int(round(g["rating"]))
    stars = "<i class=&#34;fa-solid fa-star&#34;></i>" * full + "<i class=&#34;fa-regular fa-star&#34;></i>" * (5 - full)
    pkgs  = "".join(
        f'<div style="font-size:12px;color:#374151;padding:5px 0;border-bottom:1px solid #F3F4F6;display:flex;justify-content:space-between">'
        f'<span><i class=&#34;fa-solid fa-check&#34;></i> {p}</span></div>'
        for p in g["pkgs"]
    )
    avail_color = "#065F46" if "Sun" in g["avail"] or "Mon-Sun" in g["avail"] else "#C8930A"
    return (
        '<div class="grid-card" style="display:flex;flex-direction:column">'
        f'<div class="grid-card-top" style="background:linear-gradient(135deg,{col},{col}bb);position:relative">'
        f'<div style="width:64px;height:64px;border-radius:50%;background:rgba(255,255,255,.25);border:3px solid rgba(255,255,255,.6);display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800;color:#fff;margin:0 auto 10px">{g["name"][0]}</div>'
        f'<div style="font-weight:800;font-size:16px;color:#fff;margin-bottom:3px">{g["name"]}</div>'
        f'<div style="font-size:12px;color:rgba(255,255,255,.85);margin-bottom:6px">{g["spec"]}</div>'
        f'<span style="background:rgba(255,255,255,.2);color:#fff;font-size:11px;padding:2px 10px;border-radius:20px">{city}</span>'
        '</div>'
        '<div class="grid-card-body" style="flex:1;display:flex;flex-direction:column">'
        f'<div style="color:#D97706;font-size:13px;margin-bottom:6px">{stars} <span style="color:#94A3B8;font-size:12px">{g["rating"]} ({g["tours"]} tours)</span></div>'
        f'<div style="font-size:12px;color:#475569;margin-bottom:2px"><i class=&#34;fa-solid fa-earth-americas&#34;></i> {g["lang"]}</div>'
        f'<div style="font-size:12px;margin-bottom:2px"><span style="background:{avail_color}22;color:{avail_color};padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600"><i class=&#34;fa-regular fa-calendar&#34;></i> {g["avail"]}</span></div>'
        f'<div style="font-size:13px;color:#4B5563;margin:8px 0;line-height:1.5;font-style:italic">&ldquo;{g["bio"]}&rdquo;</div>'
        f'<div style="font-size:18px;font-weight:800;color:{col};margin-bottom:8px">{g["rate"]}</div>'
        f'<div style="margin-bottom:14px;border:1px solid #E5E7EB;border-radius:8px;overflow:hidden"><div style="background:#F9FAFB;padding:6px 10px;font-size:11px;font-weight:700;color:#475569;text-transform:uppercase">Packages</div>{pkgs}</div>'
        '<div style="margin-top:auto;display:flex;flex-direction:column;gap:7px">'
        '<button class="btn" style="background:'+col+';color:#fff;width:100%;padding:10px;font-size:14px;font-weight:700" onclick="openBookingModal(\'' + name + '\',\'' + city + '\',\'' + g["rate"] + '\',\'' + str(g.get("guide_id", g.get("id",""))) + '\')"><i class=&#34;fa-regular fa-calendar&#34;></i> Book This Guide</button>'
        f'<button class="btn-outline" style="width:100%;padding:8px;color:{col};border-color:{col}" onclick="openProfileModal(\'{name}\',\'{city}\',\'{g["spec"]}\',\'{g["bio"]}\',\'{g["lang"]}\',\'{g["avail"]}\',\'{g["rate"]}\',\'{g["rating"]}\',\'{g["tours"]}\',\''+str(g.get("guide_id", g.get("id","")))+'\')"><i class=&#34;fa-solid fa-user&#34;></i> View Full Profile</button>'
        '</div></div></div>'
    )

def render(filter_city="All", filter_lang="All", user=None, booked=False):
    cities   = ["All"] + sorted(set(g["city"] for g in ALL_GUIDES))
    city_opts = "".join(f'<option {"selected" if c==filter_city else ""}>{c}</option>' for c in cities)
    lang_opts = "".join(f'<option {"selected" if l==filter_lang else ""}>{l}</option>' for l in ["All","EN","FIL","ES","IL"])
    combined  = get_all_guides_combined(filter_city)
    filtered  = [g for g in combined
        if (filter_lang=="All" or filter_lang in g["lang"])]
    guide_html = "".join(_card(g,i) for i,g in enumerate(filtered)) if filtered else (
        '<div class="guide-empty"><div style="font-size:48px;margin-bottom:12px"><i class=&#34;fa-solid fa-user-tie&#34;></i></div>'
        '<div style="font-weight:700;font-size:18px">No Tour Guides Found</div></div>'
    )
    count = f"{len(filtered)} guide(s) available" if filtered else "0 guides found"

    booked_banner = '<div style="background:#D1FAE5;color:#065F46;padding:14px 20px;border-radius:10px;margin-bottom:20px;font-weight:700;font-size:15px"><i class=&#34;fa-solid fa-check&#34;></i> Booking submitted! Your guide will confirm your booking shortly.</div>' if booked else ""
    body = f"""
    <div class="page-wrap">
      {booked_banner}
      <div style="margin-bottom:22px">
        <div class="section-title">Tour Guide Booking</div>
        <div class="section-sub">Book a verified local guide for your Luzon adventure</div>
      </div>

      <!-- Stats bar -->
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:20px">
        <div style="background:#0038A8;color:#fff;border-radius:12px;padding:14px;text-align:center">
          <div style="font-size:24px;font-weight:800">{len(ALL_GUIDES)}</div>
          <div style="font-size:12px;opacity:.85">Verified Guides</div>
        </div>
        <div style="background:#0038A8;color:#fff;border-radius:12px;padding:14px;text-align:center">
          <div style="font-size:24px;font-weight:800">9</div>
          <div style="font-size:12px;opacity:.85">Cities Covered</div>
        </div>
        <div style="background:#1E3A5F;color:#fff;border-radius:12px;padding:14px;text-align:center">
          <div style="font-size:24px;font-weight:800">4.7<i class=&#34;fa-solid fa-star&#34;></i></div>
          <div style="font-size:12px;opacity:.85">Avg. Rating</div>
        </div>
        <div style="background:#1E3A5F;color:#fff;border-radius:12px;padding:14px;text-align:center">
          <div style="font-size:24px;font-weight:800">900+</div>
          <div style="font-size:12px;opacity:.85">Tours Completed</div>
        </div>
      </div>

      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#1E3A5F"><span>Find Your Guide</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div><label class="lbl">City</label><select class="inp" name="city" style="width:180px">{city_opts}</select></div>
            <div><label class="lbl">Language</label><select class="inp" name="lang" style="width:140px">{lang_opts}</select></div>
            <button class="btn" style="background:#1E3A5F;color:#fff" type="submit">Find Guides</button>
          </form>
        </div>
      </div>

      <div style="font-size:13px;color:#475569;margin-bottom:16px">{count}</div>
      <div class="page-grid3">{guide_html}</div>
    </div>

    <!-- Booking Modal -->
    <div id="booking-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;align-items:center;justify-content:center">
      <div style="background:#fff;border-radius:16px;padding:28px;max-width:440px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,.3)">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
          <div style="font-size:18px;font-weight:800;color:#1F2937">Book a Tour Guide</div>
          <button onclick="closeBookingModal()" style="background:none;border:none;font-size:22px;cursor:pointer;color:#475569">&times;</button>
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
          <button class="btn" style="flex:1;background:#1E3A5F;color:#fff;padding:11px;font-weight:700" onclick="confirmBooking()"><i class=&#34;fa-solid fa-check&#34;></i> Confirm Booking</button>
          <button class="btn-outline" style="flex:1;padding:11px" onclick="closeBookingModal()">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Profile Modal -->
    <div id="profile-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;align-items:center;justify-content:center">
      <div style="background:#fff;border-radius:16px;padding:28px;max-width:460px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,.3)">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
          <div style="font-size:18px;font-weight:800;color:#1F2937">Guide Profile</div>
          <button onclick="closeProfileModal()" style="background:none;border:none;font-size:22px;cursor:pointer;color:#475569">&times;</button>
        </div>
        <div id="profile-content"></div>
        <button class="btn" id="profile-book-btn" style="width:100%;background:#1E3A5F;color:#fff;padding:11px;margin-top:16px;font-weight:700"><i class=&#34;fa-regular fa-calendar&#34;></i> Book This Guide</button>
      </div>
    </div>

    <script>
    var _bookingGuide   = "";
    var _bookingCity    = "";
    var _bookingRate    = "";
    var _bookingGuideId = "";

    function openBookingModal(name, city, rate, guideId) {{
      if(typeof ATLAS_LOGGED_IN!=='undefined' && !ATLAS_LOGGED_IN){{ openSigninGate(); return; }}
      _bookingGuide = name; _bookingCity = city; _bookingRate = rate; _bookingGuideId = guideId || "";
      document.getElementById("booking-guide-info").innerHTML =
        "<strong><i class=&#34;fa-solid fa-user&#34;></i> " + name + "</strong> &mdash; " + city + "<br>Rate: <strong style='color:#0038A8'>" + rate + "</strong>";
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
      // POST to server so guide receives the booking
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
        '<div style="width:72px;height:72px;border-radius:50%;background:#6B21A8;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:800;color:#fff;margin:0 auto 10px">' + name[0] + '</div>' +
        '<div style="font-size:20px;font-weight:800">' + name + '</div>' +
        '<div style="color:#475569;font-size:13px">' + spec + '</div></div>' +
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px">' +
        '<div style="background:#F3F4F6;border-radius:8px;padding:10px;text-align:center"><div style="font-size:18px;font-weight:800;color:#0038A8"><i class=&#34;fa-solid fa-star&#34;></i> ' + rating + '</div><div style="font-size:11px;color:#475569">Rating</div></div>' +
        '<div style="background:#F3F4F6;border-radius:8px;padding:10px;text-align:center"><div style="font-size:18px;font-weight:800;color:#DC2626">' + tours + '</div><div style="font-size:11px;color:#475569">Tours Done</div></div>' +
        '</div>' +
        '<div style="font-size:13px;color:#374151;margin-bottom:12px;line-height:1.6;background:#FFFBEB;border-left:3px solid #C8930A;padding:10px">' + bio + '</div>' +
        '<div style="font-size:13px;color:#475569;margin-bottom:4px"><i class=&#34;fa-solid fa-earth-americas&#34;></i> Languages: <strong>' + lang + '</strong></div>' +
        '<div style="font-size:13px;color:#475569;margin-bottom:4px"><i class=&#34;fa-regular fa-calendar&#34;></i> Available: <strong>' + avail + '</strong></div>' +
        '<div style="font-size:13px;color:#475569"><i class=&#34;fa-solid fa-location-dot&#34;></i> City: <strong>' + city + '</strong></div>' +
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
