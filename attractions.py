import sys, os, urllib.request, urllib.parse, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import SPOTS as FALLBACK

FSQ_KEY = "JHNF2RTKPV0ISAD1DSYUZLMJRH3AC1EJ43B3LBDK0WLNBEMN"
CAT_COLORS = {"Nature":"#065F46","Historical":"#0038A8","Heritage":"#C8930A","Landmark":"#CE1126","Park":"#065F46","Museum":"#0038A8"}
CAT_ICONS  = {"Nature":"&#127807;","Historical":"&#127963;","Heritage":"&#9962;","Landmark":"&#127981;","Park":"&#127795;","Museum":"&#127963;"}

CITY_COORDS = {
    "Albay": ("13.1391", "123.7438"),
    "Baguio": ("16.4023", "120.5960"),
    "Bataan": ("14.6417", "120.4818"),
    "Batangas": ("13.7565", "121.0583"),
    "Benguet": ("16.6167", "120.5667"),
    "Cebu": ("10.3157", "123.8854"),
    "Clark": ("15.1800", "120.5600"),
    "Davao": ("7.1907", "125.4553"),
    "Ilocos Norte": ("18.1977", "120.5778"),
    "Manila": ("14.5995", "120.9842"),
    "Pangasinan": ("15.8949", "120.2863"),
    "Puerto Princesa": ("9.7392", "118.7353"),
    "Tagaytay": ("14.1153", "120.9621"),
    "Vigan": ("17.5747", "120.3873"),
}

ATTRACTION_CATS = "16000,16020,16032,16034,16035"  # landmarks, historic, parks, museums


def fetch_spots(city="Manila", keyword=""):
    try:
        lat, lng = CITY_COORDS.get(city, ("14.5995", "120.9842"))
        q = keyword if keyword else "tourist attraction"
        url = (
            "https://api.foursquare.com/v3/places/search"
            f"?query={urllib.parse.quote(q)}&ll={lat},{lng}&radius=15000&limit=9&categories={ATTRACTION_CATS}"
        )
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": FSQ_KEY,
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=6) as r:
            d = json.loads(r.read())
        results = []
        for p in d.get("results", []):
            cats = p.get("categories", [{}])
            cat_name = cats[0].get("name", "Attraction") if cats else "Attraction"
            cat_l = cat_name.lower()
            cat_short = (
                "Nature" if any(x in cat_l for x in ["park", "garden", "nature", "mountain", "volcano", "beach"])
                else "Heritage" if any(x in cat_l for x in ["heritage", "church", "historic", "monument"])
                else "Museum" if "museum" in cat_l
                else "Landmark"
            )
            name = p.get("name", "Unknown")
            results.append(
                {
                    "name": name,
                    "city": city,
                    "cat": cat_short,
                    "rating": round(p.get("rating", 8.0) / 2, 1) if p.get("rating") else 4.0,
                    "visits": "N/A",
                    "entry": "Check on-site",
                    "hours": "Check on-site",
                    "desc": f"{name} in {p.get('location', {}).get('locality', city)} offers culture, scenery, and local history for travelers.",
                    "img": f"https://source.unsplash.com/800x500/?{urllib.parse.quote(name + ' Philippines attraction')}",
                    "fsq_id": p.get("fsq_id", ""),
                }
            )
        return results if results else FALLBACK
    except Exception:
        return FALLBACK


def _card(s):
    col = CAT_COLORS.get(s["cat"], "#0038A8")
    icon = CAT_ICONS.get(s["cat"], "&#127963;")
    name = s["name"].replace("'", "")
    js_name = s["name"].replace("\\", "\\\\").replace("'", "\\'")
    js_city = s["city"].replace("\\", "\\\\").replace("'", "\\'")
    city = s["city"]
    img = s.get("img") or f"https://source.unsplash.com/800x500/?{urllib.parse.quote(name + ' Philippines attraction')}"
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
        f'<img src="{img}" alt="{s["name"]}" style="width:100%;height:130px;object-fit:cover;border-radius:10px;margin-bottom:10px"/>'
        f'<div style="color:#F59E0B;font-size:13px;margin-bottom:6px">{stars} <span style="color:#9CA3AF">{s["rating"]}</span></div>'
        f'<div style="font-size:12px;color:#6B7280;margin-bottom:2px">&#128205; {city}</div>'
        f'<div style="font-size:12px;color:#6B7280;margin-bottom:2px">&#128336; {s["hours"]}</div>'
        f'<div style="font-size:14px;font-weight:800;color:#CE1126;margin:8px 0 6px">Entry: {s["entry"]}</div>'
        f'<div style="font-size:12px;color:#6B7280;line-height:1.5;margin-bottom:14px">{s["desc"][:120]}...</div>'
        '<div style="display:flex;flex-direction:column;gap:7px">'
        f'<button class="btn" style="background:{col};color:#fff;width:100%;padding:8px" onclick="addToItinerary(\'{js_name}\', \'{js_city}\')">+ Add to Itinerary</button>'
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:7px">'
        f'<a href="/restaurants.py?city={city}" style="display:block"><button class="btn" style="background:#CE1126;color:#fff;width:100%;padding:7px;font-size:12px">Nearby Restaurants</button></a>'
        f'<a href="{maps}" target="_blank" style="display:block"><button class="btn" style="background:#C8930A;color:#fff;width:100%;padding:7px;font-size:12px">Directions</button></a>'
        '</div></div></div></div>'
    )


def render(filter_city="All", filter_cat="All", keyword="", user=None):
    city = filter_city if filter_city != "All" else "Manila"
    results = fetch_spots(city, keyword)
    if filter_cat != "All":
        results = [s for s in results if s["cat"] == filter_cat]

    cities = ["All"] + sorted(CITY_COORDS.keys())
    city_opts = "".join(f'<option {"selected" if c==filter_city else ""}>{c}</option>' for c in cities)
    cat_opts = "".join(
        f'<option {"selected" if c==filter_cat else ""}>{c}</option>'
        for c in ["All", "Nature", "Historical", "Heritage", "Landmark", "Museum", "Park"]
    )
    cards = "".join(_card(s) for s in results)
    empty = (
        '<div class="guide-empty"><div style="font-size:40px;margin-bottom:10px">&#128269;</div><div style="font-weight:700;font-size:16px">No attractions found</div></div>'
        if not results
        else ""
    )

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
            <div><label class="lbl">Category</label><select class="inp" name="cat" style="width:170px">{cat_opts}</select></div>
            <div style="flex:1;min-width:160px"><label class="lbl">Keyword</label>
              <input class="inp" name="kw" placeholder="e.g. volcano, heritage..." value="{keyword}"/></div>
            <button class="btn" style="background:#CE1126;color:#fff" type="submit">Search</button>
          </form>
        </div>
      </div>
      <div style="margin-bottom:16px;font-size:13px;color:#6B7280">{len(results)} attraction(s) found</div>
      <div class="page-grid3">{cards}</div>{empty}
    </div>
    <script>
      function addToItinerary(name, city) {{
        var key = 'atlas_itinerary_items';
        var raw = localStorage.getItem(key);
        var items = raw ? JSON.parse(raw) : [];
        var exists = items.some(function(x) {{ return x.name === name && x.city === city; }});
        if (!exists) {{
          items.push({{name: name, city: city, addedAt: new Date().toISOString()}});
          localStorage.setItem(key, JSON.stringify(items));
        }}
        showToast('Added to itinerary: ' + name);
      }}
    </script>"""
    return build_shell("Attractions", body, "attractions", user=user)
