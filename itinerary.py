import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import ITINERARIES

def render(dest="Manila", user=None):
    if dest not in ITINERARIES:
        dest = "Manila"
    days = ITINERARIES[dest]

    dest_opts = "".join(f'<option {"selected" if d == dest else ""}>{d}</option>' for d in ITINERARIES)

    day_cards = ""
    for day in days:
        acts = "".join(f'<div class="act-row"><div style="font-size:12px;color:#6B7280;min-width:50px">{a[0]}</div><div style="font-size:13px;color:#374151">{a[1]}</div></div>' for a in day["acts"])
        day_cards += f'<div class="day-card"><div class="day-hdr" style="background:{day["color"]}">{day["day"]}</div>{acts}</div>'

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Itinerary Planner</div>
        <div class="section-sub">Sample travel itineraries for top Luzon destinations</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8"><span>Select Destination</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;align-items:flex-end">
            <div style="flex:1"><label class="lbl">Destination</label>
              <select class="inp" name="dest">{dest_opts}</select></div>
            <button class="btn" style="background:#0038A8;color:#fff" type="submit">View Itinerary</button>
          </form>
        </div>
      </div>
      <div style="margin-bottom:14px">
        <div class="section-title" style="font-size:18px">{dest} Itinerary</div>
        <div class="section-sub">{len(days)}-day suggested travel plan</div>
      </div>
      {day_cards}
      <div class="card" style="margin-top:20px">
        <div class="card-hdr" style="background:#065F46"><span>Saved Attraction Picks</span></div>
        <div class="card-body">
          <div id="saved-itinerary-list" style="display:flex;flex-direction:column;gap:8px;color:#6B7280;font-size:13px">
            No saved attractions yet. Add items from Tourist Attractions.
          </div>
        </div>
      </div>
    </div>"""
    body += """
    <script>
      (function() {
        var key = 'atlas_itinerary_items';
        var host = document.getElementById('saved-itinerary-list');
        if (!host) return;
        var items = [];
        try {
          items = JSON.parse(localStorage.getItem(key) || '[]');
        } catch (e) {
          items = [];
        }
        if (!items.length) return;
        host.innerHTML = items.map(function(x, i) {
          return '<div style="padding:8px 10px;border:1px solid #E5E7EB;border-radius:8px;background:#F9FAFB">'
            + '<strong>' + (i + 1) + '. ' + x.name + '</strong> <span style="color:#9CA3AF">(' + x.city + ')</span></div>';
        }).join('');
      })();
    </script>"""
    return build_shell("Itinerary", body, "itinerary", user=user)
