import sys, os, urllib.request, urllib.parse, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import WEATHER as FALLBACK

API_KEY = "64a99b2ac477b0d12944d61cd3514ebd"
CITIES  = ["Manila","Baguio","Ilocos Norte","Vigan","Batangas","Tagaytay"]
CITY_QUERY = {
    "Manila":"Manila,PH","Baguio":"Baguio,PH","Ilocos Norte":"Laoag,PH",
    "Vigan":"Vigan,PH","Batangas":"Batangas,PH","Tagaytay":"Tagaytay,PH"
}
ICONS = {"Clear":"&#9728;","Clouds":"&#9925;","Rain":"&#127783;","Drizzle":"&#127783;",
         "Thunderstorm":"&#9928;","Snow":"&#10052;","Mist":"&#127787;","Fog":"&#127787;","Haze":"&#127787;"}

def fetch_weather(city):
    try:
        q = CITY_QUERY.get(city, city + ",PH")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(q)}&appid={API_KEY}&units=metric"
        with urllib.request.urlopen(url, timeout=5) as r:
            d = json.loads(r.read())
        cond = d["weather"][0]["main"]
        desc = d["weather"][0]["description"].title()
        temp = f"{d['main']['temp']:.0f}°C"
        feel = f"{d['main']['feels_like']:.0f}°C"
        hum  = f"{d['main']['humidity']}%"
        wind = f"{d['wind']['speed']*3.6:.0f} km/h"
        press= f"{d['main']['pressure']} hPa"
        vis  = f"{d.get('visibility',10000)//1000} km"
        uv   = "Check app"
        tip  = f"Current conditions: {desc}. Stay prepared!"
        return {"temp":temp,"feel":feel,"cond":desc,"hum":hum,"wind":wind,"uv":uv,"press":press,"vis":vis,"tip":tip,"icon":ICONS.get(cond,"&#9728;")}
    except:
        fb = FALLBACK.get(city, list(FALLBACK.values())[0])
        fb["icon"] = "&#9728;"
        return fb

def fetch_forecast(city):
    try:
        q = CITY_QUERY.get(city, city + ",PH")
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={urllib.parse.quote(q)}&appid={API_KEY}&units=metric&cnt=7"
        with urllib.request.urlopen(url, timeout=5) as r:
            d = json.loads(r.read())
        result = []
        for item in d["list"][:7]:
            cond = item["weather"][0]["main"]
            result.append((f"{item['main']['temp']:.0f}C", item["weather"][0]["description"].title(), ICONS.get(cond,"&#9728;")))
        return result
    except:
        return [("--","N/A","&#9728;")] * 7

def render(location="Manila"):
    if location not in CITIES:
        location = "Manila"
    wd = fetch_weather(location)
    forecast = fetch_forecast(location)
    today = datetime.date.today()
    today_str = today.strftime("%A, %B %d, %Y")
    day_labels = ["Today"] + [(today + datetime.timedelta(days=i)).strftime("%a %b %d") for i in range(1,7)]
    loc_opts = "".join(f'<option {"selected" if k==location else ""}>{k}</option>' for k in CITIES)

    fc_cells = "".join(f"""
    <div class="fc-day">
      <div style="font-size:11px;color:#6B7280;margin-bottom:4px">{day_labels[i]}</div>
      <div style="font-size:22px;margin-bottom:4px">{fc[2]}</div>
      <div style="font-weight:800;color:#0038A8;font-size:15px;margin-bottom:2px">{fc[0]}</div>
      <div style="font-size:10px;color:#6B7280">{fc[1]}</div>
    </div>""" for i,fc in enumerate(forecast))

    metrics = [("Humidity",wd["hum"],"#0038A8"),("Wind",wd["wind"],"#CE1126"),
               ("UV Index",wd["uv"],"#C8930A"),("Pressure",wd["press"],"#0077B6"),("Visibility",wd["vis"],"#6B21A8")]
    metric_cells = "".join(f"""
    <div class="metric-cell">
      <div style="font-size:13px;color:#6B7280;margin-bottom:4px">{lbl}</div>
      <div style="font-weight:800;color:{col};font-size:15px">{val}</div>
    </div>""" for lbl,val,col in metrics)

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Weather Forecast</div>
        <div class="section-sub">Live weather conditions across Luzon - {today_str}</div>
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
        <div class="card-hdr" style="background:#0038A8"><span>7-Day Forecast</span></div>
        <div style="padding:16px 20px;display:flex;gap:8px;flex-wrap:wrap">{fc_cells}</div>
      </div>
    </div>"""
    return build_shell("Weather", body, "weather")
