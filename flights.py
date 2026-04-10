import sys, os, urllib.request, urllib.parse, json, datetime, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tourist_ui import build_shell
from data import FLIGHTS as FALLBACK

API_KEY = "eff886bb35240c10f8071ebbcbd235c5"
DEPARTURE_AIRPORTS = {"Manila (MNL)": "MNL", "Pampanga (CRK)": "CRK"}

INTERNATIONAL_FALLBACK = [
    {"from": "Singapore Changi (SIN)", "to": "Tokyo Haneda (HND)", "airline": "Singapore Airlines", "dep": "08:10", "arr": "16:20", "dur": "7h 10m", "price": "Check airline", "seats": 9, "status": "Scheduled"},
    {"from": "Dubai International (DXB)", "to": "London Heathrow (LHR)", "airline": "Emirates", "dep": "09:45", "arr": "14:10", "dur": "7h 25m", "price": "Check airline", "seats": 6, "status": "Scheduled"},
    {"from": "Incheon International (ICN)", "to": "Sydney Kingsford Smith (SYD)", "airline": "Korean Air", "dep": "19:20", "arr": "07:10", "dur": "10h 50m", "price": "Check airline", "seats": 11, "status": "Scheduled"},
    {"from": "Los Angeles (LAX)", "to": "Vancouver (YVR)", "airline": "Air Canada", "dep": "11:00", "arr": "13:55", "dur": "2h 55m", "price": "Check airline", "seats": 14, "status": "Scheduled"},
    {"from": "Paris Charles de Gaulle (CDG)", "to": "Rome Fiumicino (FCO)", "airline": "Air France", "dep": "13:40", "arr": "15:45", "dur": "2h 05m", "price": "Check airline", "seats": 12, "status": "Scheduled"},
]

AIRLINE_COLORS = {"Philippine Airlines":"#0038A8","Cebu Pacific":"#C8930A",
                  "AirAsia":"#CE1126","PAL Express":"#0038A8"}

def fetch_flights(dep_iata="MNL"):
    try:
        url = f"https://api.aviationstack.com/v1/flights?access_key={API_KEY}&dep_iata={dep_iata}&limit=6"
        with urllib.request.urlopen(url, timeout=6) as r:
            d = json.loads(r.read())
        results = []
        dep_iata = dep_iata.upper()
        for f in (d.get("data") or [])[:10]:
            dep = f.get("departure",{})
            arr = f.get("arrival",{})
            if (dep.get("iata") or "").upper() != dep_iata:
                continue
            al  = f.get("airline",{}).get("name","Unknown")
            results.append({
                "from": f"{dep.get('airport','?')} ({dep.get('iata','?')})",
                "to":   f"{arr.get('airport','?')} ({arr.get('iata','?')})",
                "airline": al,
                "dep": (dep.get("scheduled") or "")[:16].replace("T"," ")[11:16] or "--:--",
                "arr": (arr.get("scheduled") or "")[:16].replace("T"," ")[11:16] or "--:--",
                "dur": "--",
                "price": "Check airline",
                "seats": 10,
                "status": f.get("flight_status","scheduled").title()
            })
        return results[:6] if results else FALLBACK
    except:
        return FALLBACK

def _card(f, user=None):
    col = AIRLINE_COLORS.get(f["airline"], "#0038A8")
    origin = f["from"].split("(")[0].strip()
    dest = f["to"].split("(")[0].strip()
    airline = f["airline"]
    status = f.get("status", "Scheduled")
    gf_q = urllib.parse.quote(f"{origin} to {dest}")
    booking_link = f"https://www.google.com/travel/flights?q={gf_q}"
    status_color = {"Scheduled":"#1E40AF","Active":"#065F46","Landed":"#475569","Cancelled":"#991B1B"}.get(status,"#475569")
    status_bg = {"Scheduled":"#DBEAFE","Active":"#D1FAE5","Landed":"#F1F5F9","Cancelled":"#FEE2E2"}.get(status,"#F1F5F9")

    # Book button — only for logged-in users, only for schedulable flights
    book_btn = ""
    if user and status not in ("Landed","Cancelled"):
        safe_airline  = html.escape(airline)
        safe_origin   = html.escape(f["from"])
        safe_dest     = html.escape(f["to"])
        safe_dep      = html.escape(f["dep"])
        safe_arr      = html.escape(f["arr"])
        book_btn = f"""
        <form method="post" action="/book-flight" style="margin-top:8px">
          <input type="hidden" name="airline"     value="{safe_airline}"/>
          <input type="hidden" name="origin"      value="{safe_origin}"/>
          <input type="hidden" name="destination" value="{safe_dest}"/>
          <input type="hidden" name="dep_time"    value="{safe_dep}"/>
          <input type="hidden" name="arr_time"    value="{safe_arr}"/>
          <button class="btn" type="submit" style="background:#059669;color:#fff;width:100%;padding:10px;font-weight:700;display:flex;align-items:center;justify-content:center;gap:6px">
            <i class="fa-solid fa-bookmark"></i> Book This Flight
          </button>
        </form>"""

    return f"""
    <div class="grid-card">
        <div class="grid-card-top" style="background:#0038A8">
            <div style="margin-bottom:12px"><i class="fa-solid fa-plane" style="font-size:28px;color:#fff"></i></div>
            <div style="font-weight:700;font-size:13px;color:rgba(255,255,255,.85);margin-bottom:10px">{airline}</div>
            <div style="display:flex;align-items:center;justify-content:center;gap:10px;color:#fff">
                <span style="font-weight:800;font-size:15px">{origin}</span>
                <i class="fa-solid fa-arrow-right" style="opacity:.7"></i>
                <span style="font-weight:800;font-size:15px">{dest}</span>
            </div>
            <div style="margin-top:10px;display:inline-block;background:{status_bg};color:{status_color};padding:3px 12px;border-radius:20px;font-size:11px;font-weight:700">{status}</div>
        </div>
        <div class="grid-card-body">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px">
                <div class="info-stat"><div style="font-size:11px;color:#94A3B8;margin-bottom:2px">Departs</div><div style="font-weight:700;font-size:14px">{f["dep"]}</div></div>
                <div class="info-stat"><div style="font-size:11px;color:#94A3B8;margin-bottom:2px">Arrives</div><div style="font-weight:700;font-size:14px">{f["arr"]}</div></div>
                <div class="info-stat"><div style="font-size:11px;color:#94A3B8;margin-bottom:2px">Duration</div><div style="font-weight:700;font-size:13px">{f["dur"]}</div></div>
                <div class="info-stat"><div style="font-size:11px;color:#94A3B8;margin-bottom:2px">Price</div><div style="font-weight:700;font-size:13px;color:#0038A8">{f["price"]}</div></div>
            </div>
            <a href="{booking_link}" target="_blank" style="text-decoration:none">
                <button class="btn" style="background:#0038A8;color:#fff;width:100%;padding:10px;font-weight:700;display:flex;align-items:center;justify-content:center;gap:6px">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i> View Details
                </button>
            </a>
            {book_btn}
        </div>
    </div>"""


def render(filters=None, user=None):
    filters = filters or {}
    # Log view history
    if user:
        import db as _db
        origin_q = (filters.get("origin","") or "").strip()
        dest_q   = (filters.get("destination","") or "").strip()
        if origin_q or dest_q:
            label = f"{origin_q or 'Any'} → {dest_q or 'Any'}"
            _db.log_view(user["id"], "flight", label, item_extra=filters.get("dep_date",""))
    today = datetime.date.today().isoformat()
    in5   = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()
    dep_airport = filters.get("dep_airport", "MNL").upper()
    if dep_airport not in DEPARTURE_AIRPORTS.values():
        dep_airport = "MNL"
    trip = filters.get("trip", "domestic")
    if trip not in ("domestic", "international"):
        trip = "domestic"
    origin_q = (filters.get("origin", "") or "").strip().lower()
    dest_q = (filters.get("destination", "") or "").strip().lower()
    dep_date = filters.get("dep_date", today) or today
    ret_date = filters.get("ret_date", in5) or in5

    if trip == "international":
        flights = INTERNATIONAL_FALLBACK[:]
    else:
        flights = fetch_flights(dep_airport)

    if origin_q:
        flights = [f for f in flights if origin_q in f["from"].lower()]
    if dest_q:
        flights = [f for f in flights if dest_q in f["to"].lower()]

    cards = "".join(_card(f, user) for f in flights)
    dep_airport_opts = "".join(
        f'<option value="{v}" {"selected" if v == dep_airport else ""}>{k}</option>'
        for k, v in DEPARTURE_AIRPORTS.items()
    )
    trip_opts = (
        f'<option value="domestic" {"selected" if trip=="domestic" else ""}>Domestic</option>'
        f'<option value="international" {"selected" if trip=="international" else ""}>International</option>'
    )
    safe_origin = html.escape(filters.get("origin", "") or "")
    safe_dest = html.escape(filters.get("destination", "") or "")

    # ── Weather warning for departure city ──
    dep_city = "Manila" if dep_airport == "MNL" else "Pampanga"
    weather_banner = ""
    booking_blocked = False
    try:
        import weather as _wx
        wd = _wx.fetch_weather(dep_city)
        cond = wd.get("cond","").lower()
        SEVERE   = {"thunderstorm","typhoon","tropical storm"}
        MODERATE = {"rain","heavy rain","drizzle","shower"}
        is_severe   = any(s in cond for s in SEVERE)
        is_moderate = any(s in cond for s in MODERATE)
        if is_severe:
            booking_blocked = True
            weather_banner = f"""
            <div style="background:#FEF2F2;border:1px solid #FECACA;border-radius:12px;padding:16px 20px;margin-bottom:20px;display:flex;align-items:flex-start;gap:14px">
              <div style="font-size:28px;flex-shrink:0">&#9928;</div>
              <div>
                <div style="font-weight:800;color:#991B1B;font-size:15px;margin-bottom:4px">Severe Weather — Flight Bookings Unavailable</div>
                <div style="font-size:13px;color:#7F1D1D;line-height:1.6">Current conditions in <strong>{dep_city}</strong>: <strong>{wd["cond"]}</strong> · {wd["wind"]} winds · Visibility {wd["vis"]}.
                Flights may be delayed or cancelled. Booking has been temporarily disabled for your safety.</div>
              </div>
            </div>"""
        elif is_moderate:
            weather_banner = f"""
            <div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:12px;padding:16px 20px;margin-bottom:20px;display:flex;align-items:flex-start;gap:14px">
              <div style="font-size:28px;flex-shrink:0">&#127783;</div>
              <div>
                <div style="font-weight:800;color:#92400E;font-size:15px;margin-bottom:4px">Weather Advisory — {dep_city}</div>
                <div style="font-size:13px;color:#78350F;line-height:1.6">Current conditions: <strong>{wd["cond"]}</strong> · {wd["wind"]} winds. Some flights may experience delays. Check with your airline before travelling.</div>
              </div>
            </div>"""
    except Exception:
        pass

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Flight Search</div>
        <div class="section-sub">Search domestic or international flights</div>
      </div>
      {weather_banner}
      <div class="card" style="margin-bottom:24px">
        <div class="card-hdr" style="background:#0038A8"><span>Search Flights</span></div>
        <div class="card-body">
          <form method="get" onsubmit="return validateDates()">
            <div class="form-row">
              <div><label class="lbl">Trip Type</label>
                <select class="inp" name="trip">{trip_opts}</select></div>
              <div><label class="lbl">Live Feed Departure Airport</label>
                <select class="inp" name="dep_airport">{dep_airport_opts}</select></div>
              <div><label class="lbl">Origin (Any city/airport)</label>
                <input class="inp" name="origin" placeholder="e.g. Manila, Singapore, LAX" value="{safe_origin}"/></div>
              <div><label class="lbl">Destination (Any city/airport)</label>
                <input class="inp" name="destination" placeholder="e.g. Cebu, Tokyo, London" value="{safe_dest}"/></div>
              <div><label class="lbl">Departure Date</label><input class="inp" type="date" id="dep-date" name="dep_date" value="{dep_date}" min="{today}"/></div>
              <div><label class="lbl">Return Date (Optional)</label><input class="inp" type="date" id="ret-date" name="ret_date" value="{ret_date}" min="{today}"/></div>
              <div><label class="lbl">Passengers</label>
                <select class="inp"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5+</option></select></div>
              <div><label class="lbl">Class</label>
                <select class="inp"><option>Economy</option><option>Business</option><option>First Class</option></select></div>
            </div>
            <div style="text-align:right">
              <button class="btn" style="background:#0038A8;color:#fff" type="submit">Search Flights</button>
            </div>
          </form>
        </div>
      </div>
      <div style="font-size:13px;color:#475569;margin-bottom:16px">{len(flights)} live flight(s) found</div>
      <div class="page-grid3">{cards}</div>
    </div>
    <script>
    var dep = document.getElementById('dep-date');
    var ret = document.getElementById('ret-date');
    function syncMinDate() {{
      ret.min = dep.value || '{today}';
      if (ret.value && dep.value && ret.value < dep.value) {{
        ret.value = dep.value;
      }}
    }}
    function validateDates() {{
      if (dep.value < '{today}') {{
        showToast('Departure date cannot be in the past.');
        return false;
      }}
      if (ret.value && ret.value < dep.value) {{
        showToast('Return date must be on or after departure date.');
        return false;
      }}
      return true;
    }}
    dep.addEventListener('change', syncMinDate);
    syncMinDate();
    </script>"""
    return build_shell("Flights", body, "flights", user=user)