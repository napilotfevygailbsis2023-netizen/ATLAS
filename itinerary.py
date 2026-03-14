import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import ITINERARIES, ITINERARIES_EXTRA, SPOTS as STATIC_SPOTS, RESTAURANTS as STATIC_RESTS

ALL_ITINERARIES = {**ITINERARIES, **ITINERARIES_EXTRA}

CITY_HIGHLIGHTS = {
    "Manila":       ["Intramuros walking tour","Rizal Park","National Museum","Manila Ocean Park","Fort Santiago","Binondo Chinatown food trip","BGC art walk","Malate nightlife","San Agustin Church","Manila Bay sunset","Divisoria shopping","Luneta concert"],
    "Baguio":       ["Burnham Park boating","Mines View Park","Strawberry Farm La Trinidad","Tam-awan Village","Baguio Cathedral","Camp John Hay","BenCab Museum","Wright Park horse riding","Botanical Garden","Night market Session Road","Baguio Public Market","Manor Hotel viewpoint"],
    "Tagaytay":     ["Taal Volcano viewpoint","Sky Ranch amusement park","Peoples Park in the Sky","Picnic Grove","Twin Lakes","Tagaytay Highlands","Bulalo lunch at Leslies","Bag of Beans cafe","Mahogany Market","Caleruega Church","Antonio's restaurant","Ridge viewpoint"],
    "Vigan":        ["Calle Crisologo walking tour","Vigan Cathedral","Syquia Mansion Museum","Kalesa ride","Burnay pottery workshop","Mindoro Street antiques","Plaza Salcedo","Plaza Burgos","Bantay Bell Tower","Santa Maria Church","Paoay Lake","Vigan longganisa dinner"],
    "Ilocos Norte": ["Bangui Windmills","Cape Bojeador Lighthouse","Paoay Church UNESCO","Malacañang of the North","La Paz Sand Dunes 4x4","Batac empanada lunch","Marcos Museum","Pagudpud beach","Blue Lagoon Pagudpud","Patapat Viaduct","Kapurpurawan Rock","Adams Village"],
    "Batangas":     ["Taal Heritage Town","Basilica de San Martin","Taal Lake viewpoint","Anilao snorkeling","Del Monte Beach","Laiya white sand beach","Island hopping Mabini","Caleruega Church","Dive at Beatrice Rock","Lipa City tour","San Juan market","Tingloy Island"],
    "Albay":        ["Mayon Volcano viewpoint","Cagsawa Ruins","Sumlang Lake kayak","ATV Mayon Lava Trail","Ligñon Hill viewdeck","Daraga Church","Embarcadero de Legazpi","Misibis Bay","Santo Domingo black sand beach","Quitinday Hills","Tabaco City market","Bicol Express dinner"],
    "Pangasinan":   ["Hundred Islands boat tour","Governor Island snorkel","Lingayen Gulf beach","Bolinao Falls","Cape Bolinao Lighthouse","Patar White Beach","Our Lady of Manaoag Shrine","Bangus festival Dagupan","Calasiao puto factory","San Fabian beach","Urdaneta City tour","Alaminos City market"],
    "Bataan":       ["Mt. Samat National Shrine","Dambana ng Kagitingan","Death March marker sites","Pawikan Conservation Center","Morong Beach","Las Casas Filipinas de Acuzar","Bagac mangrove forest","Corregidor Island tour","Malinta Tunnel","Pacific War Memorial","Battery Way viewpoint","Balanga City tour"],
    "La Union":     ["San Juan Surf Resort","Urbiztondo Beach surfing","Ma-Cho Temple","Poro Point Lighthouse","Tangadan Falls trek","Grape Farm visit","Flotsam and Jetsam cafe","Text Restaurant","Bacnotan Coastal Walk","Surf lesson","Sunset at the beach","San Fernando Cathedral"],
}

MEAL_IDEAS = {
    "Manila":       ["Cafe Adriatico","Barbaras Heritage Restaurant","Aristocrat Restaurant","Max's Restaurant","Toyo Eatery","Manam Comfort Filipino"],
    "Baguio":       ["Good Taste Restaurant","Cafe by the Ruins","Vizco's Restaurant","Forest House","Canto Bogchi","Hill Station"],
    "Tagaytay":     ["Leslies Restaurant","Bag of Beans","Antonio's","Josephine Restaurant","Verbena","The Cellar"],
    "Vigan":        ["Cafe Leona","Batchoy House","Cafe Uno","Kusina ni Manang","Florentina Homes","Grandpa's Inn Restaurant"],
    "Ilocos Norte": ["Saramsam Ylocano Restaurant","Fort Ilocandia","La Preciosa","Herencia Cafe","Marco's Restaurant","El Patio"],
    "Batangas":     ["Mang Inasal Lipa","Bulaluhan sa Batangas","Felicidad Restaurant","D'Rough Riders","Gerry's Grill Batangas","Robinsons Lipa food court"],
    "Albay":        ["Legazpi Boulevard restaurants","Bob Marlin Restaurant","Waway's","Bigg's Diner","Old House Cafe","1st Colonial Grill"],
    "Pangasinan":   ["Sizzling Plate Dagupan","Seven Suites Hotel resto","Blackbeard's Seafood","Bonuan Blue Beach resto","Oyster Plaza","Dagupan bangus grills"],
    "Bataan":       ["Balanga food strip","Tatang's Carinderia","Wharton Hotel resto","Mariveles seafood market","Orani local eateries","Bagac Bay restaurants"],
    "La Union":     ["Flotsam and Jetsam","Halo Halo de Iloco","Texto Restaurant","Kusina Salud","Surf and Turf La Union","La Union Farmhouse Cafe"],
}

DAY_COLORS = ["#0038A8","#CE1126","#C8930A","#065F46","#6B21A8","#0077B6","#B45309","#047857","#9D174D"]

def generate_days(dest, num_days):
    highlights = CITY_HIGHLIGHTS.get(dest, CITY_HIGHLIGHTS["Manila"])
    meals = MEAL_IDEAS.get(dest, MEAL_IDEAS["Manila"])
    days = []
    hi_index = 0
    meal_index = 0
    for d in range(num_days):
        color = DAY_COLORS[d % len(DAY_COLORS)]
        acts = []
        if d == 0:
            acts.append(("08:00", f"Arrive in {dest}, check in to hotel"))
        else:
            acts.append(("07:00", "Breakfast at hotel"))
        acts.append(("09:00", highlights[hi_index % len(highlights)])); hi_index += 1
        acts.append(("11:00", highlights[hi_index % len(highlights)])); hi_index += 1
        acts.append(("13:00", f"Lunch at {meals[meal_index % len(meals)]}"))
        meal_index += 1
        acts.append(("15:00", highlights[hi_index % len(highlights)])); hi_index += 1
        acts.append(("17:00", highlights[hi_index % len(highlights)])); hi_index += 1
        if d == num_days - 1:
            acts.append(("19:00", f"Farewell dinner at {meals[meal_index % len(meals)]}"))
            acts.append(("21:00", f"Depart {dest}"))
        else:
            acts.append(("19:00", f"Dinner at {meals[meal_index % len(meals)]}"))
        meal_index += 1
        days.append({"day": f"Day {d+1} - {dest} Adventure", "color": color, "acts": acts})
    return days

def render(dest="Manila", days=None, user=None):
    if dest not in CITY_HIGHLIGHTS:
        dest = "Manila"
    try:
        num_days = max(1, min(int(days), 14))
    except:
        num_days = 3

    generated = generate_days(dest, num_days)

    dest_opts = "".join(
        f'<option {"selected" if d == dest else ""}>{d}</option>'
        for d in sorted(CITY_HIGHLIGHTS.keys())
    )

    day_cards = ""
    for day in generated:
        acts = "".join(
            f'<div class="act-row" style="display:flex;gap:12px;padding:7px 0;border-bottom:1px solid #F3F4F6">'
            f'<div style="font-size:12px;color:#9CA3AF;min-width:50px;font-weight:600;padding-top:1px">{a[0]}</div>'
            f'<div style="font-size:13px;color:#374151">{a[1]}</div>'
            f'</div>'
            for a in day["acts"]
        )
        day_cards += (
            f'<div style="margin-bottom:16px;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08)">'
            f'<div style="background:{day["color"]};padding:12px 18px;color:#fff;font-weight:700;font-size:15px">{day["day"]}</div>'
            f'<div style="padding:4px 18px 10px;background:#fff">{acts}</div>'
            f'</div>'
        )

    # Get all spots/restaurants for the add-item dropdowns
    all_spots = [s["name"] for s in STATIC_SPOTS]
    all_rests = [r["name"] for r in STATIC_RESTS]
    spots_opts = "".join(f'<option value="{s}">{s}</option>' for s in sorted(all_spots))
    rests_opts = "".join(f'<option value="{r}">{r}</option>' for r in sorted(all_rests))

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Itinerary Planner</div>
        <div class="section-sub">Customize your travel plan — choose destination and days, or build your own from saved attractions</div>
      </div>

      <!-- GENERATE FORM -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8"><span>&#128197; Generate Itinerary</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div style="flex:1;min-width:160px">
              <label class="lbl">Destination</label>
              <select class="inp" name="dest">{dest_opts}</select>
            </div>
            <div style="min-width:140px">
              <label class="lbl">Number of Days (1–14)</label>
              <input class="inp" type="number" name="days" min="1" max="14" value="{num_days}" style="width:100%"/>
            </div>
            <button class="btn" style="background:#CE1126;color:#fff;padding:10px 24px" type="submit">Generate</button>
          </form>
        </div>
      </div>

      <!-- MY SAVED ITINERARY (from localStorage) -->
      <div class="card" style="margin-bottom:24px">
        <div class="card-hdr" style="background:#065F46"><span>&#10003; My Saved Attractions &amp; Restaurants</span></div>
        <div class="card-body" style="padding:0">
          <div id="saved-empty" style="padding:24px;text-align:center;color:#9CA3AF;font-size:14px;display:none">
            &#128269; No attractions added yet. Browse <a href="/attractions.py" style="color:#0038A8">Attractions</a> or <a href="/restaurants.py" style="color:#CE1126">Restaurants</a> and click "+ Add to Itinerary".
          </div>
          <div id="saved-list" style="padding:12px 16px"></div>
          <!-- Manual add row -->
          <div style="padding:14px 16px;border-top:1px solid #F3F4F6;background:#F9FAFB">
            <div style="font-size:12px;font-weight:700;color:#374151;margin-bottom:10px;text-transform:uppercase;letter-spacing:.5px">+ Add Manually</div>
            <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end">
              <div>
                <label class="lbl">Type</label>
                <select class="inp" id="add-type" style="width:130px" onchange="toggleAddSelect()">
                  <option value="attraction">Attraction</option>
                  <option value="restaurant">Restaurant</option>
                  <option value="custom">Custom</option>
                </select>
              </div>
              <div id="add-spot-wrap">
                <label class="lbl">Attraction</label>
                <select class="inp" id="add-spot" style="width:220px">
                  <option value="">-- select --</option>
                  {spots_opts}
                </select>
              </div>
              <div id="add-rest-wrap" style="display:none">
                <label class="lbl">Restaurant</label>
                <select class="inp" id="add-rest" style="width:220px">
                  <option value="">-- select --</option>
                  {rests_opts}
                </select>
              </div>
              <div id="add-custom-wrap" style="display:none">
                <label class="lbl">Custom Activity</label>
                <input class="inp" id="add-custom-text" placeholder="e.g. Souvenir shopping" style="width:220px"/>
              </div>
              <div>
                <label class="lbl">City</label>
                <select class="inp" id="add-city" style="width:140px">
                  <option value="">-- city --</option>
                  {dest_opts}
                </select>
              </div>
              <button class="btn" style="background:#065F46;color:#fff;padding:9px 18px" onclick="manualAdd()">Add</button>
            </div>
          </div>
        </div>
      </div>

      <!-- CUSTOM PLANNER (drag & schedule) -->
      <div class="card" style="margin-bottom:24px" id="custom-planner-card">
        <div class="card-hdr" style="background:#6B21A8;cursor:pointer" onclick="togglePlanner()">
          <span>&#9998; Custom Day Planner <span id="planner-toggle-icon" style="float:right;font-size:16px">&#9660;</span></span>
        </div>
        <div id="custom-planner-body" style="padding:16px">
          <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-bottom:16px">
            <div>
              <label class="lbl">Trip Start Date</label>
              <input class="inp" type="date" id="trip-start-date" style="width:160px"/>
            </div>
            <div>
              <label class="lbl">Days</label>
              <input class="inp" type="number" id="planner-days" min="1" max="14" value="3" style="width:80px" onchange="renderPlannerDays()"/>
            </div>
            <button class="btn" style="background:#6B21A8;color:#fff;padding:9px 18px" onclick="renderPlannerDays()">Build Plan</button>
            <button class="btn" style="background:#CE1126;color:#fff;padding:9px 18px" onclick="clearAll()">&#128465; Clear All</button>
          </div>
          <div id="planner-days-container"></div>
          <div style="margin-top:16px">
            <button class="btn" style="background:#0038A8;color:#fff;padding:10px 24px" onclick="printItinerary()">&#128424; Print / Save PDF</button>
          </div>
        </div>
      </div>

      <!-- GENERATED ITINERARY -->
      <div style="margin-bottom:18px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">
        <div>
          <div class="section-title" style="font-size:18px">{dest} — {num_days}-Day Suggested Itinerary</div>
          <div class="section-sub">Auto-generated travel plan</div>
        </div>
        <span style="background:#0038A8;color:#fff;padding:5px 16px;border-radius:20px;font-size:13px;font-weight:700">{num_days} Day{"s" if num_days > 1 else ""}</span>
      </div>
      {day_cards}
    </div>

    <script>
    var STORAGE_KEY = 'atlas_itinerary_items';

    function getItems() {{
      try {{ return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }} catch(e) {{ return []; }}
    }}
    function saveItems(items) {{
      localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    }}

    function renderSaved() {{
      var items = getItems();
      var list = document.getElementById('saved-list');
      var empty = document.getElementById('saved-empty');
      if (!items.length) {{ list.innerHTML=''; empty.style.display='block'; return; }}
      empty.style.display = 'none';
      list.innerHTML = items.map(function(item, i) {{
        var typeColor = item.type === 'restaurant' ? '#C8930A' : item.type === 'custom' ? '#6B21A8' : '#0038A8';
        var typeIcon  = item.type === 'restaurant' ? '&#127869;' : item.type === 'custom' ? '&#128393;' : '&#127981;';
        return (
          '<div style="display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid #F3F4F6">' +
          '<span style="background:' + typeColor + ';color:#fff;border-radius:6px;padding:3px 8px;font-size:11px;font-weight:700;white-space:nowrap">' + typeIcon + ' ' + (item.type||'attraction').toUpperCase() + '</span>' +
          '<div style="flex:1">' +
            '<div style="font-weight:700;font-size:14px;color:#1F2937">' + item.name + '</div>' +
            '<div style="font-size:12px;color:#6B7280">&#128205; ' + (item.city||'') + '</div>' +
          '</div>' +
          '<div style="display:flex;align-items:center;gap:8px">' +
            '<div>' +
              '<label style="font-size:10px;color:#9CA3AF;display:block">Time</label>' +
              '<input type="time" value="' + (item.time||'09:00') + '" style="border:1px solid #E2E8F0;border-radius:6px;padding:4px 6px;font-size:12px;width:90px" onchange="updateItem(' + i + ','time',this.value)"/>' +
            '</div>' +
            '<div>' +
              '<label style="font-size:10px;color:#9CA3AF;display:block">Day #</label>' +
              '<input type="number" value="' + (item.day||1) + '" min="1" max="14" style="border:1px solid #E2E8F0;border-radius:6px;padding:4px 6px;font-size:12px;width:60px" onchange="updateItem(' + i + ','day',parseInt(this.value))"/>' +
            '</div>' +
            '<div style="flex:1;min-width:120px">' +
              '<label style="font-size:10px;color:#9CA3AF;display:block">Note</label>' +
              '<input type="text" value="' + (item.note||'') + '" placeholder="Add a note..." style="border:1px solid #E2E8F0;border-radius:6px;padding:4px 8px;font-size:12px;width:100%;box-sizing:border-box" onchange="updateItem(' + i + ','note',this.value)"/>' +
            '</div>' +
            '<button onclick="removeItem(' + i + ')" style="background:#FEE2E2;color:#DC2626;border:none;border-radius:6px;padding:6px 10px;cursor:pointer;font-size:13px;font-weight:700">&#128465;</button>' +
          '</div></div>'
        );
      }}).join('');
    }}

    function updateItem(i, field, val) {{
      var items = getItems();
      if (items[i]) {{ items[i][field] = val; saveItems(items); }}
    }}

    function removeItem(i) {{
      var items = getItems();
      items.splice(i, 1);
      saveItems(items);
      renderSaved();
      renderPlannerDays();
    }}

    function clearAll() {{
      if (confirm('Clear all saved items?')) {{
        saveItems([]);
        renderSaved();
        renderPlannerDays();
      }}
    }}

    function toggleAddSelect() {{
      var t = document.getElementById('add-type').value;
      document.getElementById('add-spot-wrap').style.display   = t==='attraction' ? '' : 'none';
      document.getElementById('add-rest-wrap').style.display   = t==='restaurant' ? '' : 'none';
      document.getElementById('add-custom-wrap').style.display = t==='custom'     ? '' : 'none';
    }}

    function manualAdd() {{
      var t    = document.getElementById('add-type').value;
      var city = document.getElementById('add-city').value;
      var name = '';
      if (t === 'attraction') name = document.getElementById('add-spot').value;
      else if (t === 'restaurant') name = document.getElementById('add-rest').value;
      else name = document.getElementById('add-custom-text').value.trim();
      if (!name) {{ showToast('Please select or enter an item'); return; }}
      var items = getItems();
      if (!items.some(function(x){{ return x.name===name; }})) {{
        items.push({{ name:name, city:city, type:t, time:'09:00', day:1, note:'', addedAt:new Date().toISOString() }});
        saveItems(items);
        renderSaved();
        renderPlannerDays();
        showToast('Added: ' + name);
      }} else {{ showToast('Already added: ' + name); }}
    }}

    function renderPlannerDays() {{
      var items = getItems();
      var ndays = parseInt(document.getElementById('planner-days').value) || 3;
      var startDate = document.getElementById('trip-start-date').value;
      var container = document.getElementById('planner-days-container');
      if (!items.length) {{
        container.innerHTML = '<div style="text-align:center;color:#9CA3AF;padding:20px">No items saved yet. Add attractions above first.</div>';
        return;
      }}
      var colors = ["#0038A8","#CE1126","#C8930A","#065F46","#6B21A8","#0077B6","#B45309","#047857","#9D174D"];
      var html = '';
      for (var d = 1; d <= ndays; d++) {{
        var dayItems = items.filter(function(x){{ return (x.day||1) == d; }});
        dayItems.sort(function(a,b){{ return (a.time||'00:00').localeCompare(b.time||'00:00'); }});
        var dateLabel = '';
        if (startDate) {{
          var dt = new Date(startDate);
          dt.setDate(dt.getDate() + d - 1);
          dateLabel = ' · ' + dt.toLocaleDateString('en-PH', {{weekday:'short',month:'short',day:'numeric'}});
        }}
        html += '<div style="margin-bottom:14px;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.07)">';
        html += '<div style="background:' + (colors[(d-1)%colors.length]) + ';padding:12px 18px;color:#fff;font-weight:700;font-size:15px">Day ' + d + dateLabel + '</div>';
        html += '<div style="padding:8px 18px 12px;background:#fff">';
        if (!dayItems.length) {{
          html += '<div style="font-size:13px;color:#9CA3AF;padding:8px 0">No items for Day ' + d + ' yet. Set Day # on items above.</div>';
        }} else {{
          dayItems.forEach(function(item) {{
            var ic = item.type==='restaurant' ? '&#127869;' : item.type==='custom' ? '&#128393;' : '&#127981;';
            html += '<div style="display:flex;gap:12px;padding:7px 0;border-bottom:1px solid #F3F4F6;align-items:flex-start">';
            html += '<div style="font-size:12px;color:#9CA3AF;min-width:52px;font-weight:600;padding-top:2px">' + (item.time||'') + '</div>';
            html += '<div style="font-size:13px;color:#374151;flex:1"><span style="margin-right:4px">' + ic + '</span><strong>' + item.name + '</strong>';
            if (item.city) html += ' <span style="font-size:11px;color:#9CA3AF">· ' + item.city + '</span>';
            if (item.note) html += '<div style="font-size:11px;color:#6B7280;margin-top:2px">&#128221; ' + item.note + '</div>';
            html += '</div></div>';
          }});
        }}
        html += '</div></div>';
      }}
      container.innerHTML = html;
    }}

    function togglePlanner() {{
      var body = document.getElementById('custom-planner-body');
      var icon = document.getElementById('planner-toggle-icon');
      if (body.style.display === 'none') {{ body.style.display='block'; icon.innerHTML='&#9660;'; }}
      else {{ body.style.display='none'; icon.innerHTML='&#9654;'; }}
    }}

    function printItinerary() {{
      window.print();
    }}

    // Init
    renderSaved();
    renderPlannerDays();

    // Set today as default start date
    var today = new Date();
    document.getElementById('trip-start-date').value = today.toISOString().split('T')[0];
    </script>"""
    return build_shell("Itinerary", body, "itinerary", user=user)
