import sys, os, urllib.request, urllib.parse, json, datetime, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
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

def _card(f):
    col = AIRLINE_COLORS.get(f["airline"], "#374151")
    origin = f["from"].split("(")[0].strip()
    dest   = f["to"].split("(")[0].strip()
    airline = f["airline"]
    status = f.get("status","Scheduled")
    gf_q = urllib.parse.quote(f"{origin} to {dest}")
    booking_link = f"https://www.google.com/travel/flights?q={gf_q}"
    return (
        '<div class="grid-card">'
        f'<div class="grid-card-top" style="background:linear-gradient(135deg,{col},{col}99)">'
        f'<div style="font-size:36px;margin-bottom:8px">&#9992;</div>'
        f'<div style="font-weight:800;font-size:13px;color:#fff;margin-bottom:8px">{airline}</div>'
        f'<div style="display:flex;align-items:center;justify-content:center;gap:10px;color:#fff">'
        f'<span style="font-weight:700;font-size:14px">{origin}</span>'
        f'<span style="font-size:18px">&#10132;</span>'
        f'<span style="font-weight:700;font-size:14px">{dest}</span>'
        '</div>'
        f'<div style="margin-top:8px;font-size:11px;background:rgba(255,255,255,.2);border-radius:20px;padding:2px 10px;color:#fff">{status}</div>'
        '</div>'
        '<div class="grid-card-body">'
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px">'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">Departs</div><div style="font-weight:700;font-size:14px">{f["dep"]}</div></div>'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">Arrives</div><div style="font-weight:700;font-size:14px">{f["arr"]}</div></div>'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">Duration</div><div style="font-weight:700;font-size:13px">{f["dur"]}</div></div>'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">Price</div><div style="font-weight:700;font-size:12px;color:#CE1126">{f["price"]}</div></div>'
        '</div>'
        f'<a href="{booking_link}" target="_blank" style="display:block">'
        f'<button class="btn" style="background:{col};color:#fff;width:100%;padding:9px">Book Now</button>'
        '</a>'
        '</div></div>'
    )

def render(filters=None, user=None):
    filters = filters or {}
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

    cards = "".join(_card(f) for f in flights)
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

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Flight Search</div>
        <div class="section-sub">Search domestic or international flights</div>
      </div>
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
      <div style="font-size:13px;color:#6B7280;margin-bottom:16px">{len(flights)} live flight(s) found</div>
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
