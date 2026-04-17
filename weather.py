import sys, os, urllib.request, urllib.parse, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tourist_ui import build_shell
from data import WEATHER as FALLBACK

API_KEY = "64a99b2ac477b0d12944d61cd3514ebd"
# CITIES  = ["Albay","Baguio","Bataan","Batangas","Ilocos Norte","La Union","Manila","Pangasinan","Tagaytay","Vigan"]
# CITY_QUERY = {
#     "Manila":"Manila,PH","Baguio":"Baguio,PH","Ilocos Norte":"Laoag,PH",
#     "La Union":"San Fernando,PH","Albay":"Legazpi,PH","Pangasinan":"Dagupan,PH",
#     "Bataan":"Balanga ,PH","Vigan":"Vigan,PH","Batangas":"Batangas,PH","Tagaytay":"Tagaytay,PH",
# }
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
    loc_opts = "".join(f'<option value="{c}" {"selected" if c==location else ""}>{c}</option>' for c in CITIES)

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

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Weather Forecast</div>
        <div class="section-sub">Live weather across all Luzon provinces &mdash; {today_str}</div>
      </div>

      <!-- ── CITY DROPDOWN ── -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8"><span>Select City / Province</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap">
            <div style="flex:1;min-width:200px">
              <label class="lbl">City / Province</label>
              <select class="inp" name="location" onchange="this.form.submit()">
                {loc_opts}
              </select>
            </div>
            <button class="btn" style="background:#CE1126;color:#fff;
                                       display:inline-flex;align-items:center;gap:6px;
                                       height:42px;padding:0 20px;white-space:nowrap" type="submit">
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

    """
    return build_shell("Weather", body, "weather", user=user)
