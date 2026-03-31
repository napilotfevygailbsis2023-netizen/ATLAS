import sys, os, json
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

DAY_COLORS = ["#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8"]

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
            f'<div style="display:flex;gap:12px;padding:8px 0;border-bottom:1px solid #F3F4F6">'
            f'<div style="font-size:12px;color:#9CA3AF;min-width:54px;font-weight:600;padding-top:1px">{a[0]}</div>'
            f'<div style="font-size:13px;color:#374151">{a[1]}</div>'
            f'</div>'
            for a in day["acts"]
        )
        day_cards += (
            f'<div style="margin-bottom:14px;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08)">'
            f'<div style="background:{day["color"]};padding:12px 18px;color:#fff;font-weight:700;font-size:15px">{day["day"]}</div>'
            f'<div style="padding:4px 18px 10px;background:#fff">{acts}</div>'
            f'</div>'
        )

    # Build city-grouped spots and restaurants for JS dropdowns
    spots_by_city = {}
    for s in STATIC_SPOTS:
        c = s.get("city", "")
        spots_by_city.setdefault(c, []).append(s["name"])

    rests_by_city = {}
    for r in STATIC_RESTS:
        c = r.get("city", "")
        rests_by_city.setdefault(c, []).append(r["name"])

    all_cities = sorted(CITY_HIGHLIGHTS.keys())
    city_opts_html = "".join(f'<option value="{c}">{c}</option>' for c in all_cities)

    spots_js = json.dumps(spots_by_city)
    rests_js = json.dumps(rests_by_city)

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">My Itinerary Planner</div>
        <div class="section-sub">Add places while browsing, then build your day-by-day plan here</div>
      </div>

      <!-- STEP 1: ADD PLACES -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8"><span>&#10133; Add Places to Your Trip</span></div>
        <div class="card-body">
          <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end">
            <div>
              <label class="lbl">Type</label>
              <select class="inp" id="add-type" style="width:140px" onchange="onTypeOrCityChange()">
                <option value="attraction">Attraction</option>
                <option value="restaurant">Restaurant</option>
                <option value="custom">Custom</option>
              </select>
            </div>
            <div>
              <label class="lbl">City</label>
              <select class="inp" id="add-city" style="width:150px" onchange="onTypeOrCityChange()">
                <option value="">-- select city --</option>
                {city_opts_html}
              </select>
            </div>
            <div id="add-name-wrap" style="display:none">
              <label class="lbl" id="add-name-lbl">Place</label>
              <select class="inp" id="add-name-select" style="width:240px">
                <option value="">-- select --</option>
              </select>
            </div>
            <div id="add-custom-wrap" style="display:none">
              <label class="lbl">Custom Activity</label>
              <input class="inp" id="add-custom-text" placeholder="e.g. Souvenir shopping" style="width:240px"/>
            </div>
            <button class="btn" style="background:#0038A8;color:#fff;padding:10px 22px;font-size:14px" onclick="manualAdd()">&#43; Add</button>
          </div>
          <div style="margin-top:12px;font-size:13px;color:#6B7280">
            &#128161; You can also add places directly from
            <a href="/attractions.py" style="color:#0038A8;font-weight:600">Attractions</a> or
            <a href="/restaurants.py" style="color:#0038A8;font-weight:600">Restaurants</a> pages — they save here automatically.
          </div>
        </div>
      </div>

      <!-- STEP 2: SAVED PLACES -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8;display:flex;justify-content:space-between;align-items:center">
          <span>&#128205; My Saved Places</span>
          <button id="clear-all-btn" onclick="clearAll()" style="display:none;background:rgba(255,255,255,.2);border:none;color:#fff;border-radius:8px;padding:5px 14px;font-size:12px;font-weight:700;cursor:pointer">&#128465; Clear All</button>
        </div>
        <div class="card-body" style="padding:0">
          <div id="saved-empty" style="padding:32px;text-align:center;color:#9CA3AF;font-size:14px">
            <div style="font-size:36px;margin-bottom:10px">&#128197;</div>
            Nothing added yet. Browse <a href="/attractions.py" style="color:#0038A8;font-weight:600">Attractions</a> and click <strong>"+ Add to Itinerary"</strong>, or use the form above.
          </div>
          <div id="saved-list" style="padding:0 16px"></div>
        </div>
      </div>

      <!-- STEP 3: DAY PLANNER -->
      <div class="card" style="margin-bottom:24px">
        <div class="card-hdr" style="background:#0038A8"><span>&#128197; My Day Plan</span></div>
        <div class="card-body">
          <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end;margin-bottom:8px">
            <div>
              <label class="lbl">Trip Start Date</label>
              <input class="inp" type="date" id="trip-start-date" style="width:170px"/>
            </div>
            <div>
              <label class="lbl">Number of Days</label>
              <input class="inp" type="number" id="planner-days" min="1" max="14" value="3" style="width:90px"/>
            </div>
            <button class="btn" style="background:#0038A8;color:#fff;padding:10px 22px" onclick="buildPlan()">&#9998; Build Plan</button>
            <button id="print-btn" class="btn" onclick="printPlan()" disabled style="background:#9CA3AF;color:#fff;padding:10px 22px;cursor:not-allowed" title="Build your plan first">&#128424; Print / Save PDF</button>
          </div>
          <div style="font-size:13px;color:#6B7280;margin-bottom:16px">Set the <strong>Day #</strong> on each saved place above, then click Build Plan.</div>
          <div id="planner-container">
            <div style="text-align:center;color:#9CA3AF;font-size:14px;padding:20px">Add places above and click <strong>Build Plan</strong> to see your itinerary.</div>
          </div>
        </div>
      </div>

      <!-- AUTO-GENERATE -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8"><span>&#9889; Auto-Generate a Suggested Itinerary</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div style="flex:1;min-width:160px">
              <label class="lbl">Destination</label>
              <select class="inp" name="dest">{dest_opts}</select>
            </div>
            <div>
              <label class="lbl">Number of Days (1–14)</label>
              <input class="inp" type="number" name="days" min="1" max="14" value="{num_days}" style="width:110px"/>
            </div>
            <button class="btn" style="background:#0038A8;color:#fff;padding:10px 24px" type="submit">Generate</button>
          </form>
          <div style="margin-top:20px">
            <div style="font-weight:700;font-size:15px;margin-bottom:4px;color:#1F2937">
              {dest} &mdash; {num_days}-Day Suggested Itinerary
              <span style="background:#0038A8;color:#fff;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:700;margin-left:8px">{num_days} Day{"s" if num_days > 1 else ""}</span>
            </div>
            <div style="font-size:13px;color:#9CA3AF;margin-bottom:14px">Auto-generated travel plan — use as inspiration!</div>
            {day_cards}
          </div>
        </div>
      </div>

    </div>

    <script>
    var KEY = 'atlas_itinerary_items';
    var SPOTS = {spots_js};
    var RESTS = {rests_js};
    var COLORS = ["#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8","#0038A8"];

    function load() {{
      try {{ return JSON.parse(localStorage.getItem(KEY) || '[]'); }} catch(e) {{ return []; }}
    }}
    function save(items) {{ localStorage.setItem(KEY, JSON.stringify(items)); }}

    // When type or city changes → populate place dropdown
    function onTypeOrCityChange() {{
      var t    = document.getElementById('add-type').value;
      var city = document.getElementById('add-city').value;
      var nameWrap   = document.getElementById('add-name-wrap');
      var customWrap = document.getElementById('add-custom-wrap');

      if (t === 'custom') {{
        nameWrap.style.display   = 'none';
        customWrap.style.display = '';
        return;
      }}
      customWrap.style.display = 'none';

      if (!city) {{ nameWrap.style.display = 'none'; return; }}

      var list = (t === 'restaurant' ? RESTS[city] : SPOTS[city]) || [];
      document.getElementById('add-name-lbl').textContent = t === 'restaurant' ? 'Restaurant' : 'Attraction';

      var sel = document.getElementById('add-name-select');
      sel.innerHTML = '<option value="">-- select --</option>';
      list.slice().sort().forEach(function(n) {{
        var o = document.createElement('option');
        o.value = n; o.textContent = n;
        sel.appendChild(o);
      }});
      nameWrap.style.display = '';
    }}

    function manualAdd() {{
      var t    = document.getElementById('add-type').value;
      var city = document.getElementById('add-city').value || '';
      var name = t === 'custom'
        ? document.getElementById('add-custom-text').value.trim()
        : document.getElementById('add-name-select').value;

      if (!name) {{ showToast('Please select a place first'); return; }}

      var items = load();
      if (items.some(function(x) {{ return x.name === name; }})) {{
        showToast('Already in your itinerary: ' + name); return;
      }}
      items.push({{ name:name, city:city, type:t, time:'09:00', day:1, note:'' }});
      save(items);
      renderSaved();
      showToast('&#10003; Added: ' + name);
    }}

    function renderSaved() {{
      var items  = load();
      var list   = document.getElementById('saved-list');
      var empty  = document.getElementById('saved-empty');
      var clearBtn = document.getElementById('clear-all-btn');

      if (!items.length) {{
        list.innerHTML = '';
        empty.style.display = 'block';
        clearBtn.style.display = 'none';
        return;
      }}
      empty.style.display  = 'none';
      clearBtn.style.display = 'block';

      list.innerHTML = items.map(function(item, i) {{
        var tc = item.type==='restaurant' ? '#0038A8' : item.type==='custom' ? '#0038A8' : '#0038A8';
        var ti = item.type==='restaurant' ? '&#127869;' : item.type==='custom' ? '&#128393;' : '&#127981;';
        return (
          '<div style="display:flex;align-items:center;gap:10px;padding:12px 0;border-bottom:1px solid #F3F4F6;flex-wrap:wrap">' +
            '<span style="background:' + tc + ';color:#fff;border-radius:6px;padding:3px 9px;font-size:11px;font-weight:700;white-space:nowrap">' + ti + ' ' + (item.type||'attraction').toUpperCase() + '</span>' +
            '<div style="flex:1;min-width:120px">' +
              '<div style="font-weight:700;font-size:14px;color:#1F2937">' + item.name + '</div>' +
              (item.city ? '<div style="font-size:12px;color:#6B7280">&#128205; ' + item.city + '</div>' : '') +
            '</div>' +
            '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">' +
              '<div><label style="font-size:10px;color:#9CA3AF;display:block;margin-bottom:2px">Day #</label>' +
              '<input type="number" value="' + (item.day||1) + '" min="1" max="14" data-i="' + i + '" data-f="day" onchange="updateField(this)" style="border:1.5px solid #E2E8F0;border-radius:8px;padding:5px 6px;font-size:14px;width:60px;text-align:center;font-weight:700"/></div>' +
              '<div><label style="font-size:10px;color:#9CA3AF;display:block;margin-bottom:2px">Time</label>' +
              '<input type="time" value="' + (item.time||'09:00') + '" data-i="' + i + '" data-f="time" onchange="updateField(this)" style="border:1.5px solid #E2E8F0;border-radius:8px;padding:5px 6px;font-size:13px;width:106px"/></div>' +
              '<div style="flex:1;min-width:130px"><label style="font-size:10px;color:#9CA3AF;display:block;margin-bottom:2px">Note (optional)</label>' +
              '<input type="text" value="' + (item.note||'').replace(/"/g,"&quot;") + '" placeholder="Add a note..." data-i="' + i + '" data-f="note" onchange="updateField(this)" style="border:1.5px solid #E2E8F0;border-radius:8px;padding:5px 8px;font-size:13px;width:100%;box-sizing:border-box"/></div>' +
              '<button onclick="removeItem(' + i + ')" style="background:rgba(0,56,168,0.12);color:#0038A8;border:none;border-radius:8px;padding:7px 12px;cursor:pointer;font-size:15px;font-weight:700" title="Remove">&#128465;</button>' +
            '</div>' +
          '</div>'
        );
      }}).join('');
    }}

    function updateField(el) {{
      var i = parseInt(el.getAttribute('data-i'));
      var f = el.getAttribute('data-f');
      var items = load();
      if (items[i]) {{
        items[i][f] = f === 'day' ? parseInt(el.value)||1 : el.value;
        save(items);
      }}
    }}

    function removeItem(i) {{
      var items = load();
      items.splice(i, 1);
      save(items);
      renderSaved();
    }}

    function clearAll() {{
      if (confirm('Remove all saved places from your itinerary?')) {{
        save([]);
        renderSaved();
        document.getElementById('planner-container').innerHTML =
          '<div style="text-align:center;color:#9CA3AF;font-size:14px;padding:20px">Add places above and click <strong>Build Plan</strong> to see your itinerary.</div>';
      }}
    }}

    // Init on page load
    renderSaved();

    function buildPlan() {{
      var items  = load();
      var ndays  = parseInt(document.getElementById('planner-days').value) || 3;
      var startD = document.getElementById('trip-start-date').value;
      var container = document.getElementById('planner-container');
      var printBtn  = document.getElementById('print-btn');

      if (!items.length) {{
        container.innerHTML = '<div style="text-align:center;color:#9CA3AF;padding:24px;font-size:14px">&#128197; No places saved yet. Add some places first!</div>';
        printBtn.disabled = true;
        printBtn.style.background = '#9CA3AF';
        printBtn.style.cursor = 'not-allowed';
        return;
      }}

      var html = '';
      for (var d = 1; d <= ndays; d++) {{
        var dayItems = items.filter(function(x) {{ return (parseInt(x.day)||1) === d; }});
        dayItems.sort(function(a,b) {{ return (a.time||'00:00') > (b.time||'00:00') ? 1 : -1; }});
        var dateLabel = '';
        if (startD) {{
          var dt = new Date(startD);
          dt.setDate(dt.getDate() + d - 1);
          dateLabel = ' &middot; ' + dt.toLocaleDateString('en-PH', {{weekday:'short', month:'short', day:'numeric'}});
        }}
        html += '<div style="margin-bottom:14px;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08)">';
        html += '<div style="background:' + COLORS[(d-1) % COLORS.length] + ';padding:12px 18px;color:#fff;font-weight:700;font-size:15px">Day ' + d + dateLabel + '</div>';
        html += '<div style="padding:6px 18px 12px;background:#fff">';
        if (!dayItems.length) {{
          html += '<div style="font-size:13px;color:#9CA3AF;padding:10px 0">No places for Day ' + d + '. Set Day # to ' + d + ' on a saved place above.</div>';
        }} else {{
          dayItems.forEach(function(item) {{
            var ic = item.type==='restaurant' ? '&#127869;' : item.type==='custom' ? '&#128393;' : '&#127981;';
            html += '<div style="display:flex;gap:14px;padding:9px 0;border-bottom:1px solid #F3F4F6;align-items:flex-start">';
            html += '<div style="font-size:12px;color:#9CA3AF;min-width:52px;font-weight:700;padding-top:2px">' + (item.time||'') + '</div>';
            html += '<div style="font-size:14px;color:#1F2937;flex:1">' + ic + ' <strong>' + item.name + '</strong>';
            if (item.city) html += ' <span style="font-size:12px;color:#9CA3AF">&middot; ' + item.city + '</span>';
            if (item.note) html += '<div style="font-size:12px;color:#6B7280;margin-top:3px">&#128221; ' + item.note + '</div>';
            html += '</div></div>';
          }});
        }}
        html += '</div></div>';
      }}
      container.innerHTML = html;

      // Enable print button
      printBtn.disabled = false;
      printBtn.style.background = '#0038A8';
      printBtn.style.cursor = 'pointer';
    }}

    function printPlan() {{
      var container = document.getElementById('planner-container');
      var startD = document.getElementById('trip-start-date').value;
      var ndays  = document.getElementById('planner-days').value;
      var title  = 'My ATLAS Itinerary' + (startD ? ' — Starting ' + startD : '') + ' (' + ndays + ' days)';

      var win = window.open('', '_blank');
      win.document.write(`
        <!DOCTYPE html><html><head>
        <meta charset="UTF-8"/>
        <title>${{title}}</title>
        <style>
          body {{ font-family: 'Segoe UI', sans-serif; padding: 32px; color: #1F2937; }}
          h1 {{ font-size: 22px; font-weight: 900; margin-bottom: 4px; color: #0038A8; }}
          .sub {{ font-size: 13px; color: #6B7280; margin-bottom: 24px; }}
          .day-hdr {{ padding: 10px 16px; color: #fff; font-weight: 700; font-size: 14px; border-radius: 8px 8px 0 0; }}
          .day-body {{ border: 1px solid #E5E7EB; border-top: none; border-radius: 0 0 8px 8px; padding: 4px 16px 10px; margin-bottom: 16px; }}
          .act-row {{ display: flex; gap: 14px; padding: 8px 0; border-bottom: 1px solid #F3F4F6; }}
          .act-time {{ font-size: 12px; color: #9CA3AF; min-width: 52px; font-weight: 700; padding-top: 2px; }}
          .act-name {{ font-size: 13px; color: #1F2937; }}
          .act-city {{ font-size: 11px; color: #9CA3AF; }}
          .act-note {{ font-size: 11px; color: #6B7280; margin-top: 2px; }}
          .empty {{ font-size: 13px; color: #9CA3AF; padding: 8px 0; }}
          @media print {{ body {{ padding: 16px; }} }}
        </style>
        </head><body>
        <h1>&#128197; ${{title}}</h1>
        <div class="sub">Generated from ATLAS &mdash; Luzon Travel Companion</div>
        ${{container.innerHTML}}
        <scr'+'ipt>window.onload=function(){{window.print();window.close();}}</scr'+'ipt>
        </body></html>
      `);
      win.document.close();
    }}

    // Set today as default start date
    document.getElementById('trip-start-date').value = new Date().toISOString().split('T')[0];
    </script>"""
    return build_shell("Itinerary", body, "itinerary", user=user)