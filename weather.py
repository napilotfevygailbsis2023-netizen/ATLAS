import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import WEATHER

ICONS = {"Sunny":"&#9728;","Partly Cloudy":"&#9925;","Cloudy":"&#9729;","Rainy":"&#127783;","Thunder":"&#9928;","Foggy":"&#127787;","Clear Sky":"&#127769;","Hot & Humid":"&#129397;","Breezy & Cool":"&#127788;"}

FORECASTS = {
    "Manila":       [("33C","Partly Cloudy","#C8930A"),("32C","Sunny","#CE1126"),("30C","Cloudy","#6B7280"),("28C","Rainy","#0038A8"),("31C","Sunny","#CE1126"),("29C","Partly Cloudy","#C8930A"),("27C","Rainy","#0038A8")],
    "Baguio":       [("18C","Foggy","#6B7280"),("17C","Cloudy","#6B7280"),("19C","Partly Cloudy","#C8930A"),("16C","Rainy","#0038A8"),("20C","Sunny","#CE1126"),("18C","Foggy","#6B7280"),("17C","Cloudy","#6B7280")],
    "Ilocos Norte": [("29C","Sunny","#CE1126"),("30C","Sunny","#CE1126"),("28C","Partly Cloudy","#C8930A"),("27C","Cloudy","#6B7280"),("29C","Sunny","#CE1126"),("30C","Sunny","#CE1126"),("28C","Partly Cloudy","#C8930A")],
    "Vigan":        [("28C","Clear Sky","#0038A8"),("29C","Sunny","#CE1126"),("27C","Partly Cloudy","#C8930A"),("26C","Cloudy","#6B7280"),("28C","Sunny","#CE1126"),("27C","Clear Sky","#0038A8"),("26C","Rainy","#0038A8")],
    "Batangas":     [("31C","Hot & Humid","#CE1126"),("32C","Sunny","#CE1126"),("30C","Partly Cloudy","#C8930A"),("28C","Rainy","#0038A8"),("31C","Sunny","#CE1126"),("30C","Hot & Humid","#CE1126"),("29C","Cloudy","#6B7280")],
    "Tagaytay":     [("23C","Breezy & Cool","#0077B6"),("22C","Partly Cloudy","#C8930A"),("24C","Sunny","#CE1126"),("21C","Cloudy","#6B7280"),("23C","Breezy & Cool","#0077B6"),("22C","Rainy","#0038A8"),("24C","Sunny","#CE1126")],
}

def render(location="Manila"):
    if location not in WEATHER:
        location = "Manila"
    wd = WEATHER[location]
    today = datetime.date.today()
    day_labels = ["Today"] + [(today + datetime.timedelta(days=i)).strftime("%a %b %d") for i in range(1, 7)]
    forecast = FORECASTS.get(location, FORECASTS["Manila"])
    today_str = today.strftime("%A, %B %d, %Y")

    loc_opts = "".join(f'<option {"selected" if k == location else ""}>{k}</option>' for k in WEATHER)

    fc_cells = "".join(f"""
    <div class="fc-day">
      <div style="font-size:11px;color:#6B7280;margin-bottom:4px">{day_labels[i]}</div>
      <div style="font-size:22px;margin-bottom:4px">{ICONS.get(fc[1], "&#9728;")}</div>
      <div style="font-weight:800;color:{fc[2]};font-size:15px;margin-bottom:2px">{fc[0]}</div>
      <div style="font-size:10px;color:#6B7280">{fc[1]}</div>
    </div>""" for i, fc in enumerate(forecast))

    metrics = [("Humidity",wd["hum"],"#0038A8"),("Wind",wd["wind"],"#CE1126"),("UV Index",wd["uv"],"#C8930A"),("Pressure",wd["press"],"#0077B6"),("Visibility",wd["vis"],"#6B21A8")]
    metric_cells = "".join(f"""
    <div class="metric-cell">
      <div style="font-size:13px;color:#6B7280;margin-bottom:4px">{lbl}</div>
      <div style="font-weight:800;color:{col};font-size:15px">{val}</div>
    </div>""" for lbl, val, col in metrics)

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Weather Forecast</div>
        <div class="section-sub">Real-time weather conditions across Luzon - {today_str}</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0077B6"><span>Select Destination</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;align-items:flex-end">
            <div style="flex:1"><label class="lbl">City / Province</label>
              <select class="inp" name="location">{loc_opts}</select></div>
            <button class="btn" style="background:#0077B6;color:#fff" type="submit">Get Forecast</button>
          </form>
        </div>
      </div>
      <div class="weather-main">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:20px">
          <div>
            <div style="font-size:26px;font-weight:800;margin-bottom:2px">{location}</div>
            <div style="font-size:14px;opacity:.75;margin-bottom:8px">{wd['cond']} - {today_str}</div>
            <div class="weather-temp">{wd['temp']}</div>
            <div style="opacity:.65;font-size:13px;margin-top:4px">Feels like {wd['feel']}</div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;min-width:240px">
            <div class="weather-metric"><div style="font-size:11px;opacity:.7;margin-bottom:2px">Humidity</div><div style="font-weight:700;color:#FCD116;font-size:14px">{wd['hum']}</div></div>
            <div class="weather-metric"><div style="font-size:11px;opacity:.7;margin-bottom:2px">Wind</div><div style="font-weight:700;color:#FCD116;font-size:14px">{wd['wind']}</div></div>
            <div class="weather-metric"><div style="font-size:11px;opacity:.7;margin-bottom:2px">UV Index</div><div style="font-weight:700;color:#FCD116;font-size:14px">{wd['uv']}</div></div>
            <div class="weather-metric"><div style="font-size:11px;opacity:.7;margin-bottom:2px">Visibility</div><div style="font-weight:700;color:#FCD116;font-size:14px">{wd['vis']}</div></div>
          </div>
        </div>
        <div style="margin-top:14px;background:rgba(252,209,22,.15);border-radius:8px;padding:10px 14px;font-size:13px;color:#FCD116;border-left:3px solid #FCD116">
          Travel Advisory: {wd['tip']}
        </div>
      </div>
      <div class="metric-row">{metric_cells}</div>
      <div class="card">
        <div class="card-hdr" style="background:#0038A8"><span>7-Day Forecast</span></div>
        <div style="padding:16px 20px;display:flex;gap:8px;flex-wrap:wrap">{fc_cells}</div>
      </div>
    </div>"""
    return build_shell("Weather", body, "weather")
