import sys, os, urllib.request, urllib.parse, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tourist_ui import build_shell
from data import RESTAURANTS as STATIC_RESTS

FSQ_KEY   = "JHNF2RTKPV0ISAD1DSYUZLMJRH3AC1EJ43B3LBDK0WLNBEMN"
FOOD_CATS = "13000,13065,13002,13003,13004,13005"

CITY_COORDS = {
    "Albay":("13.1391","123.7438"), "Baguio":("16.4023","120.5960"),
    "Bataan":("14.6417","120.4818"), "Batangas":("13.7565","121.0583"),
    "Ilocos Norte":("18.1977","120.5778"), "La Union":("16.6159","120.3209"),
    "Manila":("14.5995","120.9842"), "Pangasinan":("15.8949","120.2863"),
    "Tagaytay":("14.1153","120.9621"), "Vigan":("17.5747","120.3873"),
}



REST_IMAGES = {
    # Manila — Filipino heritage / buffet / fine dining
    'Cafe Adriatico':               'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&q=80&fit=crop',
    'Barbaras Heritage Restaurant': 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80&fit=crop',
    'Aristocrat Restaurant':        'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&q=80&fit=crop',
    "Max's Restaurant":             'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80&fit=crop',
    'Toyo Eatery':                  'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80&fit=crop',
    'Manam Comfort Filipino':       'https://images.unsplash.com/photo-1565299507177-4cb3b4b986f2?w=800&q=80&fit=crop',
    'Ilustrado Restaurant':         'https://images.unsplash.com/photo-1424847651672-bf20a4b0982b?w=800&q=80&fit=crop',
    # Baguio — cozy mountain cafe ambiance
    'Good Taste Restaurant':        'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80&fit=crop',
    'Cafe by the Ruins':            'https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=800&q=80&fit=crop',
    "Vizco's Restaurant":           'https://images.unsplash.com/photo-1493857671505-72967e2e2760?w=800&q=80&fit=crop',
    'Forest House':                 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&q=80&fit=crop',
    'Hill Station':                 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80&fit=crop',
    'Canto Bogchi':                 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&q=80&fit=crop',
    # Tagaytay — taal view, bulalo, cozy
    'Leslies Restaurant':           'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&q=80&fit=crop',
    'Bag of Beans':                 'https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=800&q=80&fit=crop',
    "Antonio's":                    'https://images.unsplash.com/photo-1424847651672-bf20a4b0982b?w=800&q=80&fit=crop',
    'Josephine Restaurant':         'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80&fit=crop',
    # Vigan — Ilocano / heritage dining
    'Verbena':                      'https://images.unsplash.com/photo-1493857671505-72967e2e2760?w=800&q=80&fit=crop',
    'The Cellar':                   'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80&fit=crop',
    'Cafe Leona':                   'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&q=80&fit=crop',
    # Ilocos Norte
    'Batchoy House':                'https://images.unsplash.com/photo-1565299507177-4cb3b4b986f2?w=800&q=80&fit=crop',
    'Cafe Uno':                     'https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=800&q=80&fit=crop',
    'Kusina ni Manang':             'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80&fit=crop',
    'Saramsam Ylocano Restaurant':  'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&q=80&fit=crop',
    # Albay — Bicolano / spicy dishes
    'Bob Marlin Restaurant':        'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80&fit=crop',
    "Waway's":                      'https://images.unsplash.com/photo-1565299507177-4cb3b4b986f2?w=800&q=80&fit=crop',
    "Bigg's Diner":                 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&q=80&fit=crop',
    '1st Colonial Grill':           'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80&fit=crop',
    # Pangasinan — bangus, seafood
    'Old House Cafe':               'https://images.unsplash.com/photo-1493857671505-72967e2e2760?w=800&q=80&fit=crop',
    'Flotsam and Jetsam':           'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800&q=80&fit=crop',
    'Halo Halo de Iloco':           'https://images.unsplash.com/photo-1565299507177-4cb3b4b986f2?w=800&q=80&fit=crop',
    'Texto Restaurant':             'https://images.unsplash.com/photo-1417325384643-53415f58e074?w=800&q=80&fit=crop',
    # Batangas — bulalo capital
    'Bulaluhan sa Batangas':        'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&q=80&fit=crop',
    "Blackbeard's Seafood":         'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80&fit=crop',
    # Pangasinan — milkfish / dagupan
    'Sizzling Plate Dagupan':       'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&q=80&fit=crop',
    'Felicidad Restaurant':         'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80&fit=crop',
    "D'Rough Riders":               'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80&fit=crop',
    "Gerry's Grill Batangas":       'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80&fit=crop',
    'Seven Suites Hotel resto':     'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80&fit=crop',
    'Oyster Plaza':                 'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80&fit=crop',
    'Kusina Salud':                 'https://images.unsplash.com/photo-1565299507177-4cb3b4b986f2?w=800&q=80&fit=crop',
    # La Union — surf town, beach cafe
    'Surf and Turf La Union':       'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800&q=80&fit=crop',
    'La Union Farmhouse Cafe':      'https://images.unsplash.com/photo-1493857671505-72967e2e2760?w=800&q=80&fit=crop',
}
DEFAULT_IMG = 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80&fit=crop'

TYPE_COLORS = ["#0038A8"]*10

def _get_img(name, city):
    return REST_IMAGES.get(name, DEFAULT_IMG)

def fetch_from_foursquare(city, keyword):
    try:
        lat, lng = CITY_COORDS.get(city, ("14.5995","120.9842"))
        url = (f"https://api.foursquare.com/v3/places/search"
               f"?query={urllib.parse.quote(keyword+' '+city)}&ll={lat},{lng}&radius=8000&limit=9&categories={FOOD_CATS}")
        req = urllib.request.Request(url, headers={"Authorization": FSQ_KEY, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=6) as r:
            d = json.loads(r.read())
        results = []
        for p in d.get("results", []):
            cats    = p.get("categories", [{}])
            cuisine = cats[0].get("name","Restaurant") if cats else "Restaurant"
            name    = p.get("name","Unknown")
            results.append({
                "name": name, "city": city, "type": cuisine,
                "price": "Check restaurant",
                "rating": round(p.get("rating",8.0)/2,1) if p.get("rating") else 4.0,
                "desc": f"{name} serves {cuisine.lower()} in {city}.",
                "img": DEFAULT_IMG,
            })
        return results
    except:
        return []

def fetch_city_restaurants(city):
    """Fetch all restaurants for a city from Foursquare (no keyword needed)."""
    try:
        lat, lng = CITY_COORDS.get(city, ("14.5995", "120.9842"))
        url = (f"https://api.foursquare.com/v3/places/search"
               f"?ll={lat},{lng}&radius=8000&limit=15&categories={FOOD_CATS}")
        req = urllib.request.Request(url, headers={"Authorization": FSQ_KEY, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=6) as r:
            d = json.loads(r.read())
        results = []
        for p in d.get("results", []):
            cats    = p.get("categories", [{}])
            cuisine = cats[0].get("name", "Restaurant") if cats else "Restaurant"
            name    = p.get("name", "Unknown")
            results.append({
                "name": name, "city": city, "type": cuisine,
                "price": "Check restaurant",
                "rating": round(p.get("rating", 8.0) / 2, 1) if p.get("rating") else 4.0,
                "desc": f"{name} serves {cuisine.lower()} cuisine in {city}.",
                "img": REST_IMAGES.get(name, DEFAULT_IMG),
            })
        return results
    except Exception:
        return []

def get_restaurants(city="All", keyword=""):
    if keyword:
        search_city = city if city != "All" else "Manila"
        fsq = fetch_from_foursquare(search_city, keyword)
        if fsq:
            return fsq
        return [r for r in STATIC_RESTS if keyword.lower() in r["name"].lower()]
    if city == "All":
        # Fetch from Foursquare for all cities
        all_rests = []
        seen = set()
        for c in CITY_COORDS:
            for r in fetch_city_restaurants(c):
                if r["name"].lower() not in seen:
                    seen.add(r["name"].lower())
                    all_rests.append(r)
        return all_rests if all_rests else STATIC_RESTS
    # Single city — try Foursquare first
    fsq = fetch_city_restaurants(city)
    return fsq if fsq else [r for r in STATIC_RESTS if r.get("city") == city]

def _card(r, i):
    col   = TYPE_COLORS[i % len(TYPE_COLORS)]
    name  = r["name"]
    city  = r["city"]
    maps  = "https://www.google.com/maps/search/" + urllib.parse.quote(name) + "+" + urllib.parse.quote(city) + "+Philippines"
    img   = _get_img(name, city)
    desc  = r.get("desc","") or (f"Popular {r.get('type','Filipino')} dining in {city}.")
    full  = int(round(r["rating"]))
    stars = "&#9733;"*full + "&#9734;"*(5-full)
    price = r.get("price","Check restaurant")
    rtype = r.get("type","Filipino")
    mid   = "rm" + str(abs(hash(name + city)) % 999999)
    ns    = name.replace("'","\\'")
    cs    = city.replace("'","\\'")

    def H(s): return s.replace('"','&quot;')

    modal = (
        f'<div id="{mid}" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:9000;align-items:center;justify-content:center">'
        f'<div style="background:#fff;border-radius:16px;max-width:500px;width:92%;max-height:90vh;overflow-y:auto;box-shadow:0 8px 40px rgba(0,0,0,.25)">'
        f'<div style="background:linear-gradient(135deg,{col},{col}99);padding:24px;border-radius:16px 16px 0 0;position:relative">'
        f'<div style="font-size:36px;margin-bottom:8px">&#127869;</div>'
        f'<div style="font-weight:800;font-size:18px;color:#fff">{H(name)}</div>'
        f'<div style="font-size:13px;color:rgba(255,255,255,.8);margin-top:4px">&#128205; {H(city)} &middot; {H(rtype)}</div>'
        f'<button onclick="closeRestModal(&quot;{mid}&quot;)" style="position:absolute;top:14px;right:16px;background:rgba(255,255,255,.2);border:none;color:#fff;border-radius:50%;width:30px;height:30px;font-size:18px;cursor:pointer">&#x2715;</button>'
        f'</div><div style="padding:20px 24px">'
        f'<img loading="lazy" src="{H(img)}" alt="{H(name)}" style="width:100%;height:170px;object-fit:cover;border-radius:10px;margin-bottom:16px" onerror="this.onerror=null;this.src=\'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80&fit=crop\'"/>'
        f'<div style="color:#F59E0B;font-size:14px;margin-bottom:10px">{stars} <span style="color:#9CA3AF">{r["rating"]}</span></div>'
        f'<div style="background:#FEF3C7;border-radius:8px;padding:12px;margin-bottom:14px;text-align:center">'
        f'<div style="font-size:10px;color:#9CA3AF;text-transform:uppercase;font-weight:600">Price Range</div>'
        f'<div style="font-weight:800;color:#CE1126;font-size:18px">{price}</div></div>'
        f'<p style="font-size:13px;color:#4B5563;line-height:1.7;margin-bottom:16px">{desc}</p>'
        f'<button class="btn" style="background:#059669;color:#fff;width:100%;padding:10px;font-size:13px;margin-bottom:8px" '
        f'onclick="addRestToItinerary(\'{ns}\',\'{cs}\');closeRestModal(\'{mid}\')">&#128197; Add to Itinerary</button>'
        f'<a href="{maps}" target="_blank" style="display:block">'
        f'<button class="btn" style="background:{col};color:#fff;width:100%;padding:10px;font-size:14px">&#128205; View on Google Maps</button>'
        f'</a></div></div></div>'
    )

    card = (
        modal
        + f'<div class="rest-card3" style="cursor:pointer" onclick="if(typeof ATLAS_LOGGED_IN!==\'undefined\'&&!ATLAS_LOGGED_IN){{openSigninGate();}}else{{document.getElementById(&quot;{mid}&quot;).style.display=\'flex\';}}">'
        + f'<div style="position:relative;height:145px;overflow:hidden;border-radius:12px 12px 0 0;background:{col}">'
        + f'<img loading="lazy" src="{H(img)}" alt="{H(name)}" style="width:100%;height:100%;object-fit:cover;transition:transform .3s" onmouseover="this.style.transform=\'scale(1.05)\'" onmouseout="this.style.transform=\'scale(1)\'" onerror="this.src=\'{DEFAULT_IMG}\'"/>'
        + f'<div style="position:absolute;inset:0;background:linear-gradient(to bottom,transparent 40%,rgba(0,0,0,.55) 100%)"></div>'
        + f'<div style="position:absolute;top:8px;right:8px;background:{col};color:#fff;border-radius:20px;padding:3px 8px;font-size:10px;font-weight:700">{H(rtype)[:20]}</div>'
        + f'<div style="position:absolute;bottom:8px;left:10px"><div style="font-weight:700;font-size:14px;color:#fff">{H(name)}</div></div>'
        + f'</div>'
        + f'<div class="rest-card3-body">'
        + f'<div style="color:#F59E0B;font-size:13px;margin-bottom:4px">{stars} <span style="color:#9CA3AF;font-size:11px">{r["rating"]}</span></div>'
        + f'<div style="font-size:12px;color:#6B7280;margin-bottom:3px">&#128205; {H(city)}</div>'
        + f'<div style="font-size:12px;color:#6B7280;line-height:1.5;margin:6px 0 8px">{desc[:100]}</div>'
        + f'<div style="font-size:16px;font-weight:800;color:#CE1126;margin:8px 0">{price}</div>'
        + f'<div style="display:flex;gap:6px">'
        + f'<button onclick="event.stopPropagation();addRestToItinerary(\'{ns}\',\'{cs}\')" style="flex:1;background:#059669;color:#fff;border:none;border-radius:8px;padding:7px;font-size:11px;font-weight:700;cursor:pointer">&#128197; Itinerary</button>'
        + f'<div style="flex:1;font-size:11px;color:#0038A8;font-weight:600;text-align:center;padding:7px 0;border:1.5px solid #0038A8;border-radius:8px">&#128065; View</div>'
        + f'</div></div></div>'
    )
    return card

def render(filter_city="All", keyword="", filter_type="All", user=None):
    filtered  = get_restaurants(filter_city, keyword)
    if filter_type != "All":
        filtered = [r for r in filtered if filter_type.lower() in r.get("type","").lower()]
    cities    = ["All"] + sorted(CITY_COORDS.keys())
    city_opts = "".join(f'<option {"selected" if c==filter_city else ""}>{c}</option>' for c in cities)
    all_types = ["All","Filipino","Seafood","Cafe","Grill","Heritage","Ilocano","Bicolano","Fine Dining","Street Food","Buffet","International"]
    type_opts = "".join(f'<option {"selected" if t==filter_type else ""}>{t}</option>' for t in all_types)
    cards     = "".join(_card(r,i) for i,r in enumerate(filtered))
    empty     = ('<div class="guide-empty"><div style="font-size:40px;margin-bottom:10px">&#127869;</div>'
                 '<div style="font-weight:700;font-size:16px">No restaurants found</div></div>' if not filtered else "")
    src_note  = "Live Foursquare search results" if keyword else "Live Foursquare data · Search by keyword to discover more"
    loc_note  = "across all cities" if filter_city=="All" else f"in {filter_city}"

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Restaurants</div>
        <div class="section-sub">{src_note} · Search by keyword to discover more via Foursquare API</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8"><span>Search Restaurants</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div><label class="lbl">City</label><select class="inp" name="city" style="width:160px">{city_opts}</select></div>
            <div><label class="lbl">Cuisine Type</label><select class="inp" name="type" style="width:160px">{type_opts}</select></div>
            <div style="flex:1;min-width:180px"><label class="lbl">Search via Foursquare API</label>
              <input class="inp" name="kw" placeholder="e.g. bulalo, cafe, seafood..." value="{keyword}"/></div>
            <button class="btn" style="background:#0038A8;color:#fff" type="submit">Search</button>
          </form>
        </div>
      </div>
      <div style="margin-bottom:16px;font-size:13px;color:#6B7280">{len(filtered)} restaurant(s) found {loc_note}</div>
      <div class="rest-grid3">{cards}</div>{empty}
    </div>
    <script>
    function closeRestModal(id){{var el=document.getElementById(id);if(el)el.style.display='none';}}
    function addRestToItinerary(name,city){{
      var key='atlas_itinerary_items';
      var items=JSON.parse(localStorage.getItem(key)||'[]');
      if(!items.some(function(x){{return x.name===name&&x.city===city;}})){{
        items.push({{name:name,city:city,type:'restaurant',time:'12:00',day:1,note:'',addedAt:new Date().toISOString()}});
        localStorage.setItem(key,JSON.stringify(items));
        showToast('&#10003; Added to itinerary: '+name);
      }}else{{showToast('Already in itinerary: '+name);}}
    }}
    </script>"""
    return build_shell("Restaurants", body, "restaurants", user=user)
