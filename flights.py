import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import FLIGHTS

AIRLINE_COLORS = {"Philippine Airlines":"#0038A8","Cebu Pacific":"#C8930A","AirAsia":"#CE1126"}

def _card(f):
    col = AIRLINE_COLORS.get(f["airline"], "#374151")
    seats_color = "#CE1126" if f["seats"] <= 5 else "#065F46"
    origin = f["from"].split("(")[0].strip()
    dest   = f["to"].split("(")[0].strip()
    airline = f["airline"]
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
        '</div>'
        '<div class="grid-card-body">'
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px">'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">Departs</div><div style="font-weight:700;font-size:14px">{f["dep"]}</div></div>'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">Arrives</div><div style="font-weight:700;font-size:14px">{f["arr"]}</div></div>'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">Duration</div><div style="font-weight:700;font-size:13px">{f["dur"]}</div></div>'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">Seats Left</div><div style="font-weight:700;font-size:13px;color:{seats_color}">{f["seats"]}</div></div>'
        '</div>'
        f'<div style="font-size:22px;font-weight:900;color:#CE1126;margin-bottom:14px">{f["price"]}</div>'
        f'<button class="btn" style="background:{col};color:#fff;width:100%;padding:9px" onclick="{toast}">Book Now</button>'
        '</div></div>'
    )

def render(filters=None):
    filters = filters or {}
    today = datetime.date.today().isoformat()
    in5   = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()
    cards = "".join(_card(f) for f in FLIGHTS)

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Flight Search</div>
        <div class="section-sub">Available domestic flights to and within Luzon</div>
      </div>
      <div class="card" style="margin-bottom:24px">
        <div class="card-hdr" style="background:#0038A8"><span>Search Flights</span></div>
        <div class="card-body">
          <div class="form-row">
            <div><label class="lbl">Origin</label>
              <select class="inp"><option>Manila (MNL)</option><option>Cebu (CEB)</option></select></div>
            <div><label class="lbl">Destination</label>
              <select class="inp">
                <option>Laoag (LAO)</option><option>Baguio (BAG)</option>
                <option>Puerto Princesa (PPS)</option><option>Legazpi (LGP)</option>
                <option>Tuguegarao (TUG)</option><option>Vigan (VGN)</option>
              </select></div>
            <div><label class="lbl">Departure</label><input class="inp" type="date" id="dep-date" value="{today}"/></div>
            <div><label class="lbl">Return</label><input class="inp" type="date" id="ret-date" value="{in5}"/></div>
            <div><label class="lbl">Passengers</label>
              <select class="inp"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5+</option></select></div>
            <div><label class="lbl">Class</label>
              <select class="inp"><option>Economy</option><option>Business</option><option>First Class</option></select></div>
          </div>
          <div style="text-align:right">
            <button class="btn" style="background:#0038A8;color:#fff" onclick="showToast('Showing available flights...')">Search Flights</button>
          </div>
        </div>
      </div>
      <div style="font-size:13px;color:#6B7280;margin-bottom:16px">{len(FLIGHTS)} flights available</div>
      <div class="page-grid3">{cards}</div>
    </div>
    <script>
    document.getElementById('dep-date').addEventListener('change', function() {{
      document.getElementById('ret-date').min = this.value;
    }});
    </script>"""
    return build_shell("Flights", body, "flights")
