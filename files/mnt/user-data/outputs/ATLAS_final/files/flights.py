import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import FLIGHTS

def render(filters=None):
    filters = filters or {}
    today = datetime.date.today().isoformat()
    in5   = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()

    rows = "".join(f"""
    <tr>
      <td>{f['from']}</td><td>{f['to']}</td><td>{f['airline']}</td>
      <td>{f['dep']}</td><td>{f['arr']}</td><td>{f['dur']}</td>
      <td class="price-cell">{f['price']}</td>
      <td><span style="color:{'#CE1126' if f['seats']<=5 else '#065F46'};font-weight:700">{f['seats']} left</span></td>
      <td><button class="btn" style="background:#0038A8;color:#fff;padding:6px 14px"
          onclick="showToast('Booking {f['airline']}: {f['from']} to {f['to']}')">Book</button></td>
    </tr>""" for f in FLIGHTS)

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Flight Search</div>
        <div class="section-sub">Available domestic flights to and within Luzon</div>
      </div>
      <div class="card">
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
            <div><label class="lbl">Departure Date</label><input class="inp" type="date" id="dep-date" value="{today}"/></div>
            <div><label class="lbl">Return Date</label><input class="inp" type="date" id="ret-date" value="{in5}"/></div>
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
      <div class="card">
        <div class="card-hdr" style="background:#CE1126"><span>Available Flights - {len(FLIGHTS)} results</span></div>
        <div style="overflow-x:auto">
          <table>
            <thead><tr>
              <th>From</th><th>To</th><th>Airline</th><th>Departs</th>
              <th>Arrives</th><th>Duration</th><th>Price</th><th>Seats</th><th></th>
            </tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
      </div>
    </div>
    <script>
    document.getElementById('dep-date').addEventListener('change', function() {{
      document.getElementById('ret-date').min = this.value;
    }});
    </script>"""
    return build_shell("Flights", body, "flights")
