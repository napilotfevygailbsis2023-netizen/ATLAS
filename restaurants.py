import sys, os, urllib.request, urllib.parse, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import RESTAURANTS as STATIC_RESTS

FSQ_KEY = "JHNF2RTKPV0ISAD1DSYUZLMJRH3AC1EJ43B3LBDK0WLNBEMN"
FOOD_CATS = "13000,13065,13002,13003,13004,13005"

CITY_COORDS = {
    "Albay":        ("13.1391","123.7438"),
    "Baguio":       ("16.4023","120.5960"),
    "Bataan":       ("14.6417","120.4818"),
    "Batangas":     ("13.7565","121.0583"),
    "Ilocos Norte": ("18.1977","120.5778"),
    "Manila":       ("14.5995","120.9842"),
    "Pangasinan":   ("15.8949","120.2863"),
    "Tagaytay":     ("14.1153","120.9621"),
    "Vigan":        ("17.5747","120.3873"),
}

TYPE_COLORS = ["#0038A8","#CE1126","#C8930A","#065F46","#6B21A8","#0077B6"]

def fetch_from_foursquare(city, keyword):
    """Only called when user types a keyword."""
    try:
        lat, lng = CITY_COORDS.get(city, ("14.5995","120.9842"))
        url = (f"https://api.foursquare.com/v3/places/search"
               f"?query={urllib.parse.quote(keyword+' '+city)}&ll={lat},{lng}&radius=8000&limit=9&categories={FOOD_CATS}")
        req = urllib.request.Request(url, headers={"Authorization": FSQ_KEY, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=6) as r:
            d = json.loads(r.read())
        results = []
        for p in d.get("results",[]):
            cats = p.get("categories",[{}])
            cuisine = cats[0].get("name","Restaurant") if cats else "Restaurant"
            name = p.get("name","Unknown")
            results.append({
                "name":   name, "city": city, "type": cuisine,
                "price":  "Check restaurant",
                "rating": round(p.get("rating",8.0)/2,1) if p.get("rating") else 4.0,
                "desc":   f"{name} serves {cuisine.lower()} in {city}.",
                "img":    f"https://source.unsplash.com/900x600/?{urllib.parse.quote(name+' food')}",
            })
        return results
    except:
        return []

def get_restaurants(city="All", keyword=""):
    """Static data by default, Foursquare only for keyword search."""
    if keyword:
        search_city = city if city != "All" else "Manila"
        fsq = fetch_from_foursquare(search_city, keyword)
        return fsq if fsq else [r for r in STATIC_RESTS if keyword.lower() in r["name"].lower()]

    if city == "All":
        return STATIC_RESTS
    return [r for r in STATIC_RESTS if r.get("city") == city]

def _card(r, i):
    col  = TYPE_COLORS[i % len(TYPE_COLORS)]
    name = r["name"]
    city = r["city"]
    maps = f"https://www.google.com/maps/search/{urllib.parse.quote(name)}+{urllib.parse.quote(city)}+Philippines"
    img  = r.get("img","") or f"https://source.unsplash.com/900x600/?{urllib.parse.quote(name+' food')}"
    desc = r.get("desc","") or f"Popular {r.get('type','Filipino')} dining in {city}."
    full = int(round(r["rating"]))
    stars = "&#9733;"*full + "&#9734;"*(5-full)
    return (
        '<div class="rest-card3">'
        f'<div class="rest-card3-top" style="background:linear-gradient(135deg,{col},{col}99)">'
        f'<div style="font-size:36px;margin-bottom:10px">&#127869;</div>'
        f'<div style="font-weight:800;font-size:15px;color:#fff;line-height:1.3;margin-bottom:4px">{name}</div>'
        f'<div style="font-size:12px;color:rgba(255,255,255,.75)">{r.get("type","Filipino")}</div>'
        '</div>'
        '<div class="rest-card3-body">'
        f'<img src="{img}" alt="{name}" style="width:100%;height:135px;object-fit:cover;border-radius:10px;margin-bottom:10px" onerror="this.style.display=\'none\'"/>'
        f'<div style="color:#F59E0B;font-size:13px;margin-bottom:6px">{stars} <span style="color:#9CA3AF;font-size:12px">{r["rating"]}</span></div>'
        f'<div style="font-size:12px;color:#6B7280;margin-bottom:3px">&#128205; {city}</div>'
        f'<div style="font-size:12px;color:#6B7280;line-height:1.55;margin:8px 0 10px">{desc[:140]}</div>'
        f'<div style="font-size:18px;font-weight:800;color:#CE1126;margin:10px 0 14px">{r.get("price","Check restaurant")}</div>'
        f'<a href="{maps}" target="_blank" style="display:block">'
        f'<button class="btn" style="background:{col};color:#fff;width:100%;padding:9px;font-size:13px">View Restaurant</button>'
        '</a></div></div>'
    )

def render(filter_city="All", keyword="", user=None):
    filtered  = get_restaurants(filter_city, keyword)
    cities    = ["All"] + sorted(CITY_COORDS.keys())
    city_opts = "".join(f'<option {"selected" if c==filter_city else ""}>{c}</option>' for c in cities)
    cards = "".join(_card(r,i) for i,r in enumerate(filtered))
    empty = (
        '<div class="guide-empty"><div style="font-size:40px;margin-bottom:10px">&#127869;</div>'
        '<div style="font-weight:700;font-size:16px">No restaurants found</div></div>'
        if not filtered else ""
    )
    src_note = "Live Foursquare search results" if keyword else "Curated Luzon restaurants"
    loc_note = "across all cities" if filter_city=="All" else f"in {filter_city}"

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Restaurants</div>
        <div class="section-sub">{src_note} · Search by keyword to discover more via Foursquare API</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#C8930A"><span>Search Restaurants</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div><label class="lbl">City</label>
              <select class="inp" name="city" style="width:180px">{city_opts}</select></div>
            <div style="flex:1;min-width:200px"><label class="lbl">Search via Foursquare API</label>
              <input class="inp" name="kw" placeholder="e.g. bulalo, cafe, seafood..." value="{keyword}"/></div>
            <button class="btn" style="background:#C8930A;color:#fff" type="submit">Search</button>
          </form>
        </div>
      </div>
      <div style="margin-bottom:16px;font-size:13px;color:#6B7280">{len(filtered)} restaurant(s) found {loc_note}</div>
      <div class="rest-grid3">{cards}</div>{empty}
    </div>"""
    return build_shell("Restaurants", body, "restaurants", user=user)
