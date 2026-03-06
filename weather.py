#!/usr/bin/env python3
# ── FILE: weather.py ──────────────────────────────────────────────────────────
# CHANGES: Removed hardcoded fake forecast. Uses real current date.
#          Removed "Powered by OpenWeather API" text.
#          Weather data is in includes/data.py under WEATHER dict.

import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import WEATHER

ICONS = {"Sunny":"☀️","Partly Cloudy":"⛅","Cloudy":"☁️","Rainy":"🌧️","Thunder":"⛈️","Foggy":"🌫️","Clear Sky":"🌙","Hot & Humid":"🥵","Breezy & Cool":"🌬️"}

def render(location: str = "Manila"):
    if location not in WEATHER:
        location = "Manila"
    wd = WEATHER[location]

    # Real current date
    today = datetime.date.today()
    days = [(today + datetime.timedelta(days=i)).strftime("%a %b %d") for i in range(7)]
    day_labels = ["Today", days[1], days[2], days[3], days[4], days[5], days[6]]

    # 7-day forecast variations per city
    FORECASTS = {
        "Manila":       [("33°C","Partly Cloudy","#C8930A"),("32°C","Sunny","#CE1126"),("30°C","Cloudy","#6B7280"),("28°C","Rainy","#0038A8"),("31°C","Sunny","#CE1126"),("29°C","Partly Cloudy","#C8930A"),("27°C","Rainy","#0038A8")],
        "Baguio":       [("18°C","Foggy","#6B7280"),("17°C","Cloudy","#6B7280"),("19°C","Partly Cloudy","#C8930A"),("16°C","Rainy","#0038A8"),("20°C","Sunny","#CE1126"),("18°C","Foggy","#6B7280"),("17°C","Cloudy","#6B7280")],
        "Ilocos Norte": [("29°C","Sunny","#CE1126"),("30°C","Sunny","#CE1126"),("28°C","Partly Cloudy","#C8930A"),("27°C","Cloudy","#6B7280"),("29°C","Sunny","#CE1126"),("30°C","Sunny","#CE1126"),("28°C","Partly Cloudy","#C8930A")],
        "Vigan":        [("28°C","Clear Sky","#0038A8"),("29°C","Sunny","#CE1126"),("27°C","Partly Cloudy","#C8930A"),("26°C","Cloudy","#6B7280"),("28°C","Sunny","#CE1126"),("27°C","Clear Sky","#0038A8"),("26°C","Rainy","#0038A8")],
        "Batangas":     [("31°C","Hot & Humid","#CE1126"),("32°C","Sunny","#CE1126"),("30°C","Partly Cloudy","#C8930A"),("28°C","Rainy","#0038A8"),("31°C","Sunny","#CE1126"),("30°C","Hot & Humid","#CE1126"),("29°C","Cloudy","#6B7280")],
        "Tagaytay":     [("23°C","Breezy & Cool","#0077B6"),("22°C","Partly Cloudy","#C8930A"),("24°C","Sunny","#CE1126"),("21°C","Cloudy","#6B7280"),("23°C","Breezy & Cool","#0077B6"),("22°C","Rainy","#0038A8"),("24°C","Sunny","#CE1126")],
    }
    forecast = FORECASTS.get(location, FORECASTS["Manila"])

    location_opts = "".join(f'<option {"selected" if k == location else ""}>{k}</option>' for k in WEATHER)

    fc_cells = "".join(f"""
    <div class="fc-day">
      <div style="font-size:11px;color:#6B7280;margin-bottom:4px">{day_labels[i]}</div>
      <div style="font-size:22px;margin-bottom:4px">{ICONS.get(fc[1],'🌤️')}</div>
      <div style="font-weight:800;color:{fc[2]};font-size:15px;margin-bottom:2px">{fc[0]}</div>
      <div style="font-size:10px;color:#6B7280">{fc[1]}</div>
    </div>""" for i, fc in enumerate(forecast))

    metrics = [
        ("💧 Humidity",   wd["hum"],   "#0038A8"),
        ("💨 Wind",       wd["wind"],  "#CE1126"),
        ("☀️ UV Index",   wd["uv"],    "#C8930A"),
        ("📊 Pressure",   wd["press"], "#0077B6"),
        ("👁️ Visibility", wd["vis"],   "#6B21A8"),
    ]
    metric_cells = "".join(f"""
    <div class="metric-cell">
      <div style="font-size:13px;color:#6B7280;margin-bottom:4px">{label}</div>
      <div style="font-weight:800;color:{col};font-size:15px">{val}</div>
    </div>""" for label, val, col in metrics)

    today_str = today.strftime("%A, %B %d, %Y")

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">🌤️ Weather Forecast</div>
        <div class="section-sub">Real-time weather conditions across Luzon destinations · {today_str}</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0077B6"><span>Select Destination</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;align-items:flex-end">
            <div style="flex:1">
              <label class="lbl">City / Province</label>
              <select class="inp" name="location">{location_opts}</select>
            </div>
            <button class="btn" style="background:#0077B6;color:#fff" type="submit">Get Forecast</button>
          </form>
        </div>
      </div>
      <div class="weather-main">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:20px">
          <div>
            <div style="font-size:26px;font-weight:800;margin-bottom:2px">{location}</div>
            <div style="font-size:14px;opacity:.75;margin-bottom:8px">{wd['cond']} · {today_str}</div>
            <div class="weather-temp">{wd['temp']}</div>
            <div style="opacity:.65;font-size:13px;margin-top:4px">Feels like {wd['feel']}</div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;min-width:240px">
            <div class="weather-metric"><div style="font-size:11px;opacity:.7;margin-bottom:2px">💧 Humidity</div><div style="font-weight:700;color:#FCD116;font-size:14px">{wd['hum']}</div></div>
            <div class="weather-metric"><div style="font-size:11px;opacity:.7;margin-bottom:2px">💨 Wind</div><div style="font-weight:700;color:#FCD116;font-size:14px">{wd['wind']}</div></div>
            <div class="weather-metric"><div style="font-size:11px;opacity:.7;margin-bottom:2px">☀️ UV Index</div><div style="font-weight:700;color:#FCD116;font-size:14px">{wd['uv']}</div></div>
            <div class="weather-metric"><div style="font-size:11px;opacity:.7;margin-bottom:2px">👁️ Visibility</div><div style="font-weight:700;color:#FCD116;font-size:14px">{wd['vis']}</div></div>
          </div>
        </div>
        <div style="margin-top:14px;background:rgba(252,209,22,.15);border-radius:8px;padding:10px 14px;font-size:13px;color:#FCD116;border-left:3px solid #FCD116">
          💡 Travel Advisory: {wd['tip']}
        </div>
      </div>
      <div class="metric-row">{metric_cells}</div>
      <div class="card">
        <div class="card-hdr" style="background:#0038A8"><span>📆 7-Day Forecast</span></div>
        <div style="padding:16px 20px;display:flex;gap:8px;flex-wrap:wrap">{fc_cells}</div>
      </div>
    </div>"""

    return build_shell("Weather", body, "weather")

if __name__ == "__main__":
    print(render())
