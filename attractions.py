import sys, os, urllib.request, urllib.parse, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import SPOTS as FALLBACK

FSQ_KEY = "JHNF2RTKPV0ISAD1DSYUZLMJRH3AC1EJ43B3LBDK0WLNBEMN"
CAT_COLORS = {"Nature":"#065F46","Historical":"#0038A8","Heritage":"#C8930A","Landmark":"#CE1126","Park":"#065F46","Museum":"#0038A8"}
CAT_ICONS  = {"Nature":"&#127807;","Historical":"&#127963;","Heritage":"&#9962;","Landmark":"&#127981;","Park":"&#127795;","Museum":"&#127963;"}

CITY_COORDS = {
    "Manila":       ("14.5995","120.9842"),
    "Baguio":       ("16.4023","120.5960"),
    "Ilocos Norte": ("18.1977","120.5778"),
    "Vigan":        ("17.5747","120.3873"),
    "Batangas":     ("13.7565","121.0583"),
    "Tagaytay":     ("14.1153","120.9621"),
}

ATTRACTION_CATS = "16000,16020,16032,16034,16035"  # landmarks, historic, parks, museums

def fetch_spots(city="Manila", keyword=""):
    try:
        lat, lng = CITY_COORDS.get(city, ("14.5995","120.9842"))
        q = keyword if keyword else "tourist attraction"
        url = (f"https://api.foursquare.com/v3/places/search"
               f"?query={urllib.parse.quote(q)}&ll={lat},{lng}&radius=15000&limit=9&categories={ATTRACTION_CATS}")
        req = urllib.request.Request(url, headers={
            "Authorization": FSQ_KEY,
            "Accept": "application/json"
        })
        with urllib.request.urlopen(req, timeout=6) as r:
            d = json.loads(r.read())
        results = []
        for p in d.get("results", []):
            cats = p.get("categories", [{}])
            cat_name = cats[0].get("name","Attraction") if cats else "Attraction"
            cat_short = "Nature" if any(x in cat_name.lower() for x in ["park","garden","nature","mountain"]) else \
                        "Heritage" if any(x in cat_name.lower() for x in ["heritage","church","historic"]) else "Historical"
            results.append({
                "name": p.get("name","Unknown"),
                "city": city,
                "cat":  cat_short,
                "rating": round(p.get("rating", 8.0)/2, 1) if p.get("rating") else 4.0,
                "visits": "N/A",
                "entry": "Check on-site",
                "hours": "Check on-site",
                "desc":  f"{p.get('name','')} — located in {p.get('location',{}).get('locality', city)}, Philippines.",
                "fsq_id": p.get("fsq_id","")
            })
        return results if results else FALLBACK
    except Exception as e:
        return FALLBACK

def _card(s):
    col  = CAT_COLORS.get(s["cat"], "#0038A8")
    icon = CAT_ICONS.get(s["cat"], "&#127963;")
    name = s["name"].replace("'","")
    city = s["city"]
    maps = f"https://www.google.com/maps/search/{urllib.parse.quote(name)}+{urllib.parse.quote(city)}+Philippines"
    full = int(round(s["rating"]))
    stars = "&#9733;" * full + "&#9734;" * (5 - full)
    return (
        '<div class="grid-card">'
        f'<div class="grid-card-top" style="background:linear-gradient(135deg,{col},{col}99)">'
        f'<div style="font-size:40px;margin-bottom:10px">{icon}</div>'
        f'<div style="font-weight:800;font-size:15px;color:#fff;margin-bottom:4px">{s["name"]}</div>'
        f'<span class="badge" style="background:rgba(255,255,255,.2);color:#fff">{s["cat"]}</span>'
        '</div>'
        '<div class="grid-card-body">'
        f'<div style="color:#F59E0B;font-size:13px;margin-bottom:6px">{stars} <span style="color:#9CA3AF">{s["rating"]}</span></div>'
        f'<div style="font-size:12px;color:#6B7280;margin-bottom:2px">&#128205; {city}</div>'
        f'<div style="font-size:12px;color:#6B7280;margin-bottom:2px">&#128336; {s["hours"]}</div>'
        f'<div style="font-size:14px;font-weight:800;color:#CE1126;margin:8px 0 6px">Entry: {s["entry"]}</div>'
        f'<div style="font-size:12px;color:#6B7280;line-height:1.5;margin-bottom:14px">{s["desc"][:90]}...</div>'
        '<div style="display:flex;flex-direction:column;gap:7px">'
        f'<button class="btn" style="background:{col};color:#fff;width:100%;padding:8px" onclick="showToast(\'Added: {name}\')">+ Add to Itinerary</button>'
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:7px">'
        f'<a href="/restaurants.py?city={city}" style="display:block"><button class="btn" style="background:#CE1126;color:#fff;width:100%;padding:7px;font-size:12px">Nearby Food</button></a>'
        f'<a href="{maps}" target="_blank" style="display:block"><button class="btn" style="background:#C8930A;color:#fff;width:100%;padding:7px;font-size:12px">Directions</button></a>'
        '</div></div></div></div>'
    )

def render(filter_city="All", filter_cat="All", keyword=""):
    city = filter_city if filter_city != "All" else "Manila"
    results = fetch_spots(city, keyword)
    if filter_cat != "All":
        results = [s for s in results if s["cat"] == filter_cat]
    cities = ["All"] + sorted(CITY_COORDS.keys())
    city_opts = "".join(f'<option {"selected" if c==filter_city else ""}>{c}</option>' for c in cities)
    cat_opts  = "".join(f'<option {"selected" if c==filter_cat else ""}>{c}</option>' for c in ["All","Nature","Historical","Heritage"])
    cards = "".join(_card(s) for s in results)
    empty = '<div class="guide-empty"><div style="font-size:40px;margin-bottom:10px">&#128269;</div><div style="font-weight:700;font-size:16px">No attractions found</div></div>' if not results else ""

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Tourist Attractions</div>
        <div class="section-sub">Real places powered by Foursquare Places</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#CE1126"><span>Filter and Search</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div><label class="lbl">City</label><select class="inp" name="city" style="width:170px">{city_opts}</select></div>
            <div><label class="lbl">Category</label><select class="inp" name="cat" style="width:150px">{cat_opts}</select></div>
            <div style="flex:1;min-width:160px"><label class="lbl">Keyword</label>
              <input class="inp" name="kw" placeholder="e.g. volcano, heritage..." value="{keyword}"/></div>
            <button class="btn" style="background:#CE1126;color:#fff" type="submit">Search</button>
          </form>
        </div>
      </div>
      <div style="margin-bottom:16px;font-size:13px;color:#6B7280">{len(results)} attraction(s) found</div>
      <div class="page-grid3">{cards}</div>{empty}
    </div>"""
    return build_shell("Attractions", body, "attractions")
