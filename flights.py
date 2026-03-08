import sys, os, urllib.request, urllib.parse, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import FLIGHTS as FALLBACK

API_KEY = "eff886bb35240c10f8071ebbcbd235c5"
PH_AIRPORTS = {"Manila":"MNL","Laoag":"LAO","Baguio":"BAG","Puerto Princesa":"PPS",
                "Legazpi":"LGP","Tuguegarao":"TUG","Vigan":"VGN","Cebu":"CEB","Davao":"DVO"}

AIRLINE_COLORS = {"Philippine Airlines":"#0038A8","Cebu Pacific":"#C8930A",
                  "AirAsia":"#CE1126","PAL Express":"#0038A8"}

def fetch_flights(dep_iata="MNL"):
    try:
        url = f"https://api.aviationstack.com/v1/flights?access_key={API_KEY}&dep_iata={dep_iata}&limit=6"
        with urllib.request.urlopen(url, timeout=6) as r:
            d = json.loads(r.read())
        results = []
        for f in (d.get("data") or [])[:6]:
            dep = f.get("departure",{})
            arr = f.get("arrival",{})
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
        return results if results else FALLBACK
    except:
        return FALLBACK

def _card(f):
    col = AIRLINE_COLORS.get(f["airline"], "#374151")
    origin = f["from"].split("(")[0].strip()
    dest   = f["to"].split("(")[0].strip()
    airline = f["airline"]
    seats_color = "#CE1126" if f.get("seats",10) <= 5 else "#065F46"
    status = f.get("status","Scheduled")
    toast = f"showToast('Booking {airline}: {origin} to {dest}')"
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
        f'<button class="btn" style="background:{col};color:#fff;width:100%;padding:9px" onclick="{toast}">Book Now</button>'
        '</div></div>'
    )

def render(filters=None):
    filters = filters or {}
    today = datetime.date.today().isoformat()
    in5   = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()
    flights = fetch_flights("MNL")
    cards = "".join(_card(f) for f in flights)
    airport_opts = "".join(f'<option>{k} ({v})</option>' for k,v in PH_AIRPORTS.items())

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Flight Search</div>
        <div class="section-sub">Live domestic flights departing from Manila</div>
      </div>
      <div class="card" style="margin-bottom:24px">
        <div class="card-hdr" style="background:#0038A8"><span>Search Flights</span></div>
        <div class="card-body">
          <div class="form-row">
            <div><label class="lbl">Origin</label>
              <select class="inp"><option>Manila (MNL)</option><option>Cebu (CEB)</option></select></div>
            <div><label class="lbl">Destination</label>
              <select class="inp">{airport_opts}</select></div>
            <div><label class="lbl">Departure</label><input class="inp" type="date" id="dep-date" value="{today}"/></div>
            <div><label class="lbl">Return</label><input class="inp" type="date" id="ret-date" value="{in5}"/></div>
            <div><label class="lbl">Passengers</label>
              <select class="inp"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5+</option></select></div>
            <div><label class="lbl">Class</label>
              <select class="inp"><option>Economy</option><option>Business</option><option>First Class</option></select></div>
          </div>
          <div style="text-align:right">
            <button class="btn" style="background:#0038A8;color:#fff" onclick="showToast('Showing live flights from Manila...')">Search Flights</button>
          </div>
        </div>
      </div>
      <div style="font-size:13px;color:#6B7280;margin-bottom:16px">{len(flights)} live flight(s) found</div>
      <div class="page-grid3">{cards}</div>
    </div>
    <script>
    document.getElementById('dep-date').addEventListener('change', function() {{
      document.getElementById('ret-date').min = this.value;
    }});
    </script>"""
    return build_shell("Flights", body, "flights")
