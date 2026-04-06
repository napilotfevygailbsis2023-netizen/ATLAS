import sys, os, urllib.request, urllib.parse, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tourist_ui import build_shell
from data import WEATHER as FALLBACK

API_KEY = "64a99b2ac477b0d12944d61cd3514ebd"
CITIES  = ["Albay","Baguio","Bataan","Batangas","Ilocos Norte","La Union","Manila","Pangasinan","Tagaytay","Vigan"]
CITY_QUERY = {
    "Manila":"Manila,PH","Baguio":"Baguio,PH","Ilocos Norte":"Laoag,PH",
    "La Union":"San Fernando,PH","Albay":"Legazpi,PH","Pangasinan":"Dagupan,PH",
    "Bataan":"Balanga,PH","Vigan":"Vigan,PH","Batangas":"Batangas,PH","Tagaytay":"Tagaytay,PH",
}
ICONS = {
    "Clear":"&#9728;","Clouds":"&#9925;","Rain":"&#127783;","Drizzle":"&#127783;",
    "Thunderstorm":"&#9928;","Snow":"&#10052;","Mist":"&#127787;","Fog":"&#127787;","Haze":"&#127787;",
}
# Emoji icons for JS (no HTML entities)
ICONS_JS = {
    "Clear":"☀️","Clouds":"⛅","Rain":"🌧️","Drizzle":"🌧️",
    "Thunderstorm":"⛈️","Snow":"❄️","Mist":"🌫️","Fog":"🌫️","Haze":"🌫️",
}
COND_BG = {
    "Clear":"linear-gradient(135deg,#0038A8,#1E88E5)",
    "Clouds":"linear-gradient(135deg,#546E7A,#78909C)",
    "Rain":"linear-gradient(135deg,#1565C0,#0D47A1)",
    "Drizzle":"linear-gradient(135deg,#1565C0,#0D47A1)",
    "Thunderstorm":"linear-gradient(135deg,#1a1a2e,#16213e)",
    "default":"linear-gradient(135deg,#0038A8,#1565C0)",
}
SUN_ICON = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'

# ── SERVER: only fetch ONE city + its forecast ──────────────────────────────
def fetch_weather(city):
    try:
        q   = CITY_QUERY.get(city, city+",PH")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(q)}&appid={API_KEY}&units=metric"
        with urllib.request.urlopen(url, timeout=5) as r:
            d = json.loads(r.read())
        cond = d["weather"][0]["main"]
        desc = d["weather"][0]["description"].title()
        return {
            "temp":  f"{d['main']['temp']:.0f}°C",
            "feel":  f"{d['main']['feels_like']:.0f}°C",
            "cond":  desc,
            "hum":   f"{d['main']['humidity']}%",
            "wind":  f"{d['wind']['speed']*3.6:.0f} km/h",
            "press": f"{d['main']['pressure']} hPa",
            "vis":   f"{d.get('visibility',10000)//1000} km",
            "uv":    "Check app",
            "tip":   f"Current conditions: {desc}. Stay prepared!",
            "icon":  ICONS.get(cond,"&#9728;"),
            "bg":    COND_BG.get(cond, COND_BG["default"]),
        }
    except:
        fb = dict(FALLBACK.get(city, list(FALLBACK.values())[0]))
        fb.setdefault("icon", "&#9728;")
        fb.setdefault("bg",   COND_BG["default"])
        return fb

def fetch_forecast(city):
    try:
        q   = CITY_QUERY.get(city, city+",PH")
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={urllib.parse.quote(q)}&appid={API_KEY}&units=metric&cnt=7"
        with urllib.request.urlopen(url, timeout=5) as r:
            d = json.loads(r.read())
        result = []
        for item in d["list"][:7]:
            cond = item["weather"][0]["main"]
            result.append((f"{item['main']['temp']:.0f}°C", item["weather"][0]["description"].title(), ICONS.get(cond,"&#9728;")))
        return result
    except:
        return [("--","N/A","&#9728;")]*7

def render(location="Manila", user=None):
    if location not in CITIES: location = "Manila"

    # Only 2 API calls total (selected city + its forecast)
    wd       = fetch_weather(location)
    forecast = fetch_forecast(location)

    today     = datetime.date.today()
    today_str = today.strftime("%A, %B %d, %Y")
    day_labels = ["Today"]+[(today+datetime.timedelta(days=i)).strftime("%a %b %d") for i in range(1,7)]
    loc_opts   = "".join(f'<option {"selected" if k==location else ""}>{k}</option>' for k in CITIES)

    fc_cells = "".join(f"""
    <div class="fc-day">
      <div style="font-size:11px;color:#6B7280;margin-bottom:4px">{day_labels[i]}</div>
      <div style="font-size:22px;margin-bottom:4px">{fc[2]}</div>
      <div style="font-weight:800;color:#0038A8;font-size:15px;margin-bottom:2px">{fc[0]}</div>
      <div style="font-size:10px;color:#6B7280">{fc[1]}</div>
    </div>""" for i,fc in enumerate(forecast))

    metrics = [("Humidity",wd["hum"],"#0038A8"),("Wind",wd["wind"],"#0038A8"),
               ("UV Index",wd["uv"],"#0038A8"),("Pressure",wd["press"],"#0038A8"),("Visibility",wd["vis"],"#0038A8")]
    metric_cells = "".join(f"""
    <div class="metric-cell">
      <div style="font-size:13px;color:#6B7280;margin-bottom:4px">{lbl}</div>
      <div style="font-weight:800;color:{col};font-size:15px">{val}</div>
    </div>""" for lbl,val,col in metrics)

    # Build JS lookup tables for client-side all-cities fetch
    import json as _json
    city_queries_js = _json.dumps(CITY_QUERY)
    cond_bg_js      = _json.dumps(COND_BG)
    icons_js        = _json.dumps(ICONS_JS)
    js_coords = _json.dumps({
        "Manila":[14.5995,120.9842],"Baguio":[16.4023,120.5960],"Bataan":[14.6417,120.4818],
        "Batangas":[13.7565,121.0583],"Ilocos Norte":[18.1977,120.5778],"La Union":[16.6159,120.3209],
        "Pangasinan":[15.8949,120.2863],"Tagaytay":[14.1153,120.9621],"Vigan":[17.5747,120.3873],
        "Albay":[13.1391,123.7438]
    })

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Weather Forecast</div>
        <div class="section-sub">Live weather across all Luzon provinces &mdash; {today_str}</div>
      </div>

      <!-- Auto-detect banner -->
      <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:12px;padding:14px 20px;margin-bottom:20px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap">
        <div>
          <div style="font-weight:700;font-size:14px;color:#1E40AF;margin-bottom:2px">&#127757; Auto-detect your nearest city</div>
          <div style="font-size:13px;color:#3B82F6">Click to show weather for the Luzon city closest to you.</div>
        </div>
        <button onclick="detectCity()" style="background:#0038A8;color:#fff;border:none;border-radius:8px;padding:9px 20px;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap">
          &#128205; Detect My City
        </button>
      </div>

      <!-- All-cities overview — cards rendered by JS after page loads -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8">
          <span>All Luzon Provinces — Live Weather</span>
          <span id="all-cities-status" style="font-size:12px;opacity:.75;margin-left:10px">Loading...</span>
        </div>
        <div id="all-cities-grid" style="padding:16px;display:flex;flex-wrap:wrap;gap:10px;min-height:80px;align-items:center">
          <!-- skeleton placeholders shown while JS fetches -->
          {''.join(f'<div style="flex:1;min-width:130px;height:100px;background:linear-gradient(135deg,#0038A8,#1565C0);border-radius:12px;opacity:.35;animation:pulse 1.4s ease-in-out infinite"></div>' for _ in CITIES)}
        </div>
      </div>

      <!-- Detailed city selector -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8"><span>Detailed Forecast &mdash; Select City</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;align-items:flex-end">
            <div style="flex:1"><label class="lbl">City / Province</label>
              <select class="inp" name="location">{loc_opts}</select></div>
            <button class="btn" style="background:#0038A8;color:#fff;display:inline-flex;align-items:center;gap:6px" type="submit">
              {SUN_ICON} Get Forecast
            </button>
          </form>
        </div>
      </div>

      <!-- Current city detail -->
      <div class="weather-main" style="background:{wd['bg']}">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:20px">
          <div>
            <div style="font-size:26px;font-weight:800;margin-bottom:2px">{location}</div>
            <div style="font-size:14px;opacity:.75;margin-bottom:8px">{wd['cond']} &mdash; {today_str}</div>
            <div class="weather-temp">{wd['icon']} {wd['temp']}</div>
            <div style="opacity:.65;font-size:13px;margin-top:4px">Feels like {wd['feel']}</div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;min-width:240px">
            <div class="weather-metric"><div style="font-size:11px;opacity:.7;margin-bottom:2px">Humidity</div><div style="font-weight:700;color:#FCD116;font-size:14px">{wd['hum']}</div></div>
            <div class="weather-metric"><div style="font-size:11px;opacity:.7;margin-bottom:2px">Wind</div><div style="font-weight:700;color:#FCD116;font-size:14px">{wd['wind']}</div></div>
            <div class="weather-metric"><div style="font-size:11px;opacity:.7;margin-bottom:2px">Pressure</div><div style="font-weight:700;color:#FCD116;font-size:14px">{wd['press']}</div></div>
            <div class="weather-metric"><div style="font-size:11px;opacity:.7;margin-bottom:2px">Visibility</div><div style="font-weight:700;color:#FCD116;font-size:14px">{wd['vis']}</div></div>
          </div>
        </div>
        <div style="margin-top:14px;background:rgba(252,209,22,.15);border-radius:8px;padding:10px 14px;font-size:13px;color:#FCD116;border-left:3px solid #FCD116">
          &#9888; Travel Advisory: {wd['tip']}
        </div>
      </div>
      <div class="metric-row">{metric_cells}</div>
      <div class="card">
        <div class="card-hdr" style="background:#0038A8"><span>7-Day Forecast &mdash; {location}</span></div>
        <div style="padding:16px 20px;display:flex;gap:8px;flex-wrap:wrap">{fc_cells}</div>
      </div>
    </div>

    <style>
    @keyframes pulse {{
      0%,100%{{opacity:.35}} 50%{{opacity:.6}}
    }}
    </style>

    <script>
    var OWM_KEY   = "{API_KEY}";
    var CITIES    = {_json.dumps(CITIES)};
    var CQ        = {city_queries_js};
    var COND_BG   = {cond_bg_js};
    var ICONS     = {icons_js};
    var LUZON_COORDS = {js_coords};
    var _done = 0;

    // Fetch one city then render its card immediately (no waiting for others)
    function fetchOneCity(city) {{
      var q   = CQ[city] || city + ',PH';
      var url = 'https://api.openweathermap.org/data/2.5/weather?q=' + encodeURIComponent(q) + '&appid=' + OWM_KEY + '&units=metric';
      fetch(url)
        .then(function(r){{ return r.json(); }})
        .then(function(d){{
          var cond = d.weather[0].main;
          var icon = ICONS[cond] || '☀️';
          var bg   = COND_BG[cond] || COND_BG['default'];
          var temp = Math.round(d.main.temp) + '°C';
          var hum  = d.main.humidity + '%';
          var wind = Math.round(d.wind.speed * 3.6) + ' km/h';
          var desc = d.weather[0].description.replace(/\\b\\w/g,function(c){{return c.toUpperCase();}});
          renderCityCard(city, icon, bg, temp, hum, wind, desc);
        }})
        .catch(function(){{
          renderCityCard(city, '☀️', COND_BG['default'], '--', '--', '--', 'N/A');
        }});
    }}

    function renderCityCard(city, icon, bg, temp, hum, wind, desc) {{
      _done++;
      // Find and replace the skeleton for this city's position
      var idx = CITIES.indexOf(city);
      var grid = document.getElementById('all-cities-grid');
      var skeletons = grid.querySelectorAll('div[style*="animation"]');
      if (skeletons[idx]) {{
        skeletons[idx].outerHTML =
          '<div style="background:' + bg + ';border-radius:12px;padding:14px 16px;cursor:pointer;' +
          'transition:transform .2s,box-shadow .2s;min-width:130px;flex:1" ' +
          'onclick="location.href=\'/weather.py?location=' + encodeURIComponent(city) + '\'" ' +
          'onmouseover="this.style.transform=\'translateY(-3px)\';this.style.boxShadow=\'0 8px 24px rgba(0,0,0,.2)\'" ' +
          'onmouseout="this.style.transform=\'\';this.style.boxShadow=\'\'">' +
          '<div style="font-size:22px;margin-bottom:4px">' + icon + '</div>' +
          '<div style="font-weight:800;font-size:13px;color:#fff;margin-bottom:2px">' + city + '</div>' +
          '<div style="font-size:24px;font-weight:900;color:#fff;line-height:1;margin-bottom:4px">' + temp + '</div>' +
          '<div style="font-size:11px;color:rgba(255,255,255,.8);margin-bottom:4px">' + desc + '</div>' +
          '<div style="font-size:10px;color:rgba(255,255,255,.7)">💧' + hum + ' &nbsp; 🌬️' + wind + '</div>' +
          '</div>';
      }}
      var status = document.getElementById('all-cities-status');
      if (status) {{
        if (_done >= CITIES.length) {{
          status.textContent = 'All cities updated ✓';
          setTimeout(function(){{ status.style.opacity='0'; }}, 2000);
        }} else {{
          status.textContent = _done + '/' + CITIES.length + ' loaded...';
        }}
      }}
    }}

    // Fire all city fetches in parallel after page has rendered
    window.addEventListener('load', function() {{
      CITIES.forEach(function(city) {{ fetchOneCity(city); }});
    }});

    function detectCity() {{
      if (!navigator.geolocation) {{ showToast('Geolocation not supported.'); return; }}
      showToast('📍 Detecting your nearest city...');
      navigator.geolocation.getCurrentPosition(function(pos) {{
        var lat = pos.coords.latitude, lng = pos.coords.longitude;
        var nearest = null, minD = Infinity;
        for (var city in LUZON_COORDS) {{
          var c = LUZON_COORDS[city];
          var d = Math.sqrt(Math.pow(lat-c[0],2)+Math.pow(lng-c[1],2));
          if (d < minD) {{ minD = d; nearest = city; }}
        }}
        if (nearest) {{
          showToast('🌡️ Nearest: ' + nearest + ' — loading...');
          setTimeout(function(){{ location.href = '/weather.py?location=' + encodeURIComponent(nearest); }}, 800);
        }}
      }}, function() {{ showToast('Could not detect location. Please allow access.'); }});
    }}
    </script>"""
    return build_shell("Weather", body, "weather", user=user)
