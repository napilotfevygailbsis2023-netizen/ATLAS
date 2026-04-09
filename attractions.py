"attraction"

import sys, os, urllib.request, urllib.parse, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tourist_ui import build_shell
from data import SPOTS as STATIC_SPOTS

FSQ_KEY = "JHNF2RTKPV0ISAD1DSYUZLMJRH3AC1EJ43B3LBDK0WLNBEMN"

CAT_COLORS = {
    "Nature":     "#0038A8", "Historical": "#0038A8", "Heritage": "#0038A8",
    "Landmark":   "#0038A8", "Park":       "#0038A8", "Museum":   "#0038A8",
}
CAT_ICONS = {
    "Nature":     '<i class="fa-solid fa-leaf"></i>',
    "Historical": '<i class="fa-solid fa-landmark"></i>',
    "Heritage":   '<i class="fa-solid fa-place-of-worship"></i>',
    "Landmark":   '<i class="fa-solid fa-location-dot"></i>',
    "Park":       '<i class="fa-solid fa-tree"></i>',
    "Museum":     '<i class="fa-solid fa-building"></i>',
}

CITY_COORDS = {
    "Albay":("13.1391","123.7438"), "Baguio":("16.4023","120.5960"),
    "Bataan":("14.6417","120.4818"), "Batangas":("13.7565","121.0583"),
    "Ilocos Norte":("18.1977","120.5778"), "La Union":("16.6159","120.3209"),
    "Manila":("14.5995","120.9842"), "Pangasinan":("15.8949","120.2863"),
    "Tagaytay":("14.1153","120.9621"), "Vigan":("17.5747","120.3873"),
}

# Curated Unsplash images per attraction

SPOT_IMAGES = {
    # Manila — accurate photo IDs
    'Intramuros':                   'https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=800&q=80&fit=crop',
    'Fort Santiago':                'https://images.unsplash.com/photo-1566438480900-0609be27a4be?w=800&q=80&fit=crop',
    'Rizal Park':                   'https://images.unsplash.com/photo-1519832979-6fa011b87667?w=800&q=80&fit=crop',
    'National Museum of Fine Arts': 'https://images.unsplash.com/photo-1554907984-15263bfd63bd?w=800&q=80&fit=crop',
    'Manila Ocean Park':            'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=80&fit=crop',
    'Binondo Chinatown':            'https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800&q=80&fit=crop',
    'San Agustin Church':           'https://images.unsplash.com/photo-1601119479271-21ca92049c81?w=800&q=80&fit=crop',
    'Manila Bay Sunset':            'https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?w=800&q=80&fit=crop',
    'Paco Park':                    'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=800&q=80&fit=crop',
    # Baguio — pine trees, mountains, cool city
    'Burnham Park':                 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80&fit=crop',
    'Mines View Park':              'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80&fit=crop',
    'The Mansion':                  'https://images.unsplash.com/photo-1467226632440-65f0b4957b27?w=800&q=80&fit=crop',
    'Strawberry Farm':              'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=800&q=80&fit=crop',
    'Camp John Hay':                'https://images.unsplash.com/photo-1448375240586-882707db888b?w=800&q=80&fit=crop',
    'Botanical Garden':             'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=800&q=80&fit=crop',
    # Vigan / Ilocos — Spanish colonial cobblestone
    'Calle Crisologo':              'https://images.unsplash.com/photo-1548027571-0353e1a7ab38?w=800&q=80&fit=crop',
    'Vigan Cathedral':              'https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&q=80&fit=crop',
    'Paoay Church':                 'https://images.unsplash.com/photo-1567901616809-a2ec7c32c9e9?w=800&q=80&fit=crop',
    'Bangui Windmills':             'https://images.unsplash.com/photo-1548337138-e87d889cc369?w=800&q=80&fit=crop',
    'Cape Bojeador Lighthouse':     'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80&fit=crop',
    # Batangas / Tagaytay — Taal Volcano lake
    'Taal Volcano':                 'https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86?w=800&q=80&fit=crop',
    # Albay — Mayon perfect cone + ruins
    'Mayon Volcano':                'https://images.unsplash.com/photo-1513360371669-4adf3dd7dff8?w=800&q=80&fit=crop',
    'Cagsawa Ruins':                'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=800&q=80&fit=crop',
    'Sumlang Lake':                 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80&fit=crop',
    'Lignon Hill':                  'https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=800&q=80&fit=crop',
    'Misibis Bay':                  'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80&fit=crop',
    'Hoyop-Hoyopan Cave':           'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800&q=80&fit=crop',
    'Quitinday Green Hills':        'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80&fit=crop',
    'Ligon Hill Nature Park':       'https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=800&q=80&fit=crop',
    'Albay Park and Wildlife':      'https://images.unsplash.com/photo-1530092376999-2431865aa8df?w=800&q=80&fit=crop',
    # Pangasinan — islands, beach, waterfalls, church
    'Hundred Islands':              'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=80&fit=crop',
    'Lingayen Gulf':                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80&fit=crop',
    'Bolinao Falls':                'https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=800&q=80&fit=crop',
    'Cape Bolinao Lighthouse':      'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80&fit=crop',
    'Patar Beach':                  'https://images.unsplash.com/photo-1526481280693-3bfa7568e0f3?w=800&q=80&fit=crop',
    'Manaoag Church':               'https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&q=80&fit=crop',
    'Bolinao Marine Laboratory':    'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=80&fit=crop',
    'Alaminos City Plaza':          'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=80&fit=crop',
    'Enchanted Cave':               'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800&q=80&fit=crop',
    # Bataan — war memorial, cross shrine, beach
    'Mt. Samat Shrine':             'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=800&q=80&fit=crop',
    'Pawikan Conservation Center':  'https://images.unsplash.com/photo-1518020382113-a7e8fc38eac9?w=800&q=80&fit=crop',
    'Bataan Death March Trail':     'https://images.unsplash.com/photo-1553361371-9b21c2ac4ae0?w=800&q=80&fit=crop',
    'Las Casas Filipinas de Acuzar':'https://images.unsplash.com/photo-1467226632440-65f0b4957b27?w=800&q=80&fit=crop',
    'Dunsulan Falls':               'https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=800&q=80&fit=crop',
    'Balanga Cathedral':            'https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&q=80&fit=crop',
    'Sisiman Bay':                  'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80&fit=crop',
    'Bagac Beach':                  'https://images.unsplash.com/photo-1526481280693-3bfa7568e0f3?w=800&q=80&fit=crop',
    'Montemar Beach Club':          'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80&fit=crop',
    # La Union — surf, temple, lighthouse, falls
    'San Juan Surf Resort':         'https://images.unsplash.com/photo-1502680390469-be75c86b636f?w=800&q=80&fit=crop',
    'Ma-Cho Temple':                'https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=800&q=80&fit=crop',
    'Poro Point Lighthouse':        'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80&fit=crop',
    'Tangadan Falls':               'https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=800&q=80&fit=crop',
    'Grape Farm':                   'https://images.unsplash.com/photo-1564419320461-6870880221ad?w=800&q=80&fit=crop',
    'Alpas Resort':                 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80&fit=crop',
    'San Fernando Cathedral':       'https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&q=80&fit=crop',
    'Bacnotan Coastal Area':        'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80&fit=crop',
}
DEFAULT_IMG = 'https://images.unsplash.com/photo-1519046904884-488729347d55?w=800&q=80&fit=crop&crop=center'

# Curated price ranges (more realistic than a single fixed price)
PRICE_RANGES = {
    "Intramuros":                    "Free – PHP 200 (guided tours)",
    "Fort Santiago":                 "PHP 75 – 150",
    "Rizal Park":                    "Free",
    "National Museum of Fine Arts":  "Free",
    "Manila Ocean Park":             "PHP 380 – 900",
    "Binondo Chinatown":             "Free",
    "San Agustin Church":            "PHP 75 – 200",
    "Manila Bay Sunset":             "Free",
    "Paco Park":                     "Free",
    "Burnham Park":                  "Free (boat/bike rental extra)",
    "Mines View Park":               "Free",
    "The Mansion":                   "Free",
    "Strawberry Farm":               "PHP 50 – 120",
    "Camp John Hay":                 "Free – PHP 200 (activities extra)",
    "Botanical Garden":              "Free",
    "Hundred Islands":               "PHP 100 – 600 (boat tours)",
    "Bolinao Falls":                 "PHP 30 – 100",
    "Cape Bolinao Lighthouse":       "Free",
    "Patar Beach":                   "PHP 20 – 60",
    "Manaoag Church":                "Free",
    "Mayon Volcano":                 "Free – PHP 2,500 (ATV/trekking tours)",
    "Cagsawa Ruins":                 "PHP 20 – 50",
    "Sumlang Lake":                  "Free (kayak rental: PHP 50–200)",
    "Lignon Hill":                   "PHP 50 – 150 (zipline extra)",
    "Las Casas Filipinas de Acuzar": "PHP 800 – 3,000",
    "Mt. Samat Shrine":              "Free",
    "Bataan Death March Trail":      "Free",
    "Pawikan Conservation Center":   "Free",
    "Dunsulan Falls":                "PHP 20 – 50",
    "Calle Crisologo":               "Free",
    "Paoay Church":                  "Free",
    "Bangui Windmills":              "PHP 20 – 50",
    "San Juan Surf Resort":          "Free (surf lessons: PHP 500–1,500)",
    "Tangadan Falls":                "PHP 30 – 100",
    "Ma-Cho Temple":                 "Free",
}

def _get_img(name, city):
    return SPOT_IMAGES.get(name, DEFAULT_IMG)


def _get_price_range(spot):
    name  = spot.get("name", "")
    entry = spot.get("entry", "Check on-site")
    if name in PRICE_RANGES:
        return PRICE_RANGES[name]
    if entry == "Free":
        return "Free"
    if entry.startswith("PHP"):
        try:
            base = int(''.join(c for c in entry if c.isdigit()))
            return f"PHP {base:,} – {int(base*1.8):,}"
        except:
            pass
    return entry

def fetch_from_foursquare(city, keyword):
    try:
        lat, lng = CITY_COORDS.get(city, ("14.5995", "120.9842"))
        url = (f"https://api.foursquare.com/v3/places/search"
               f"?query={urllib.parse.quote(keyword+' '+city)}&ll={lat},{lng}&radius=20000&limit=9")
        req = urllib.request.Request(url, headers={"Authorization": FSQ_KEY, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=6) as r:
            d = json.loads(r.read())
        results = []
        for p in d.get("results", []):
            cats     = p.get("categories", [{}])
            cat_name = cats[0].get("name", "Attraction") if cats else "Attraction"
            cat_l    = cat_name.lower()
            cat_short = (
                "Nature"  if any(x in cat_l for x in ["park","garden","nature","mountain","volcano","beach","lake"])
                else "Heritage" if any(x in cat_l for x in ["heritage","church","historic","monument","shrine"])
                else "Museum"   if "museum" in cat_l
                else "Landmark"
            )
            name = p.get("name", "Unknown")
            results.append({
                "name": name, "city": city, "cat": cat_short,
                "rating": round(p.get("rating", 8.0)/2, 1) if p.get("rating") else 4.0,
                "entry": "Check on-site", "hours": "Check on-site",
                "desc": f"{name} is a notable spot in {city} worth visiting.",
                "img": DEFAULT_IMG,
            })
        return results
    except:
        return []

def get_spots(city="All", keyword=""):
    if keyword:
        search_city = city if city != "All" else "Manila"
        fsq = fetch_from_foursquare(search_city, keyword)
        return fsq if fsq else [s for s in STATIC_SPOTS if keyword.lower() in s["name"].lower()]
    if city == "All": return STATIC_SPOTS
    return [s for s in STATIC_SPOTS if s.get("city") == city]

def _card(s):
    col        = CAT_COLORS.get(s["cat"], "#0038A8")
    icon       = CAT_ICONS.get(s["cat"], '<i class="fa-solid fa-landmark"></i>')
    city       = s["city"]
    name       = s["name"]
    img        = _get_img(name, city)
    maps       = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(name+' '+city+' Philippines')}"
    desc       = s.get("desc", "")
    price_rng  = _get_price_range(s)
    hours      = s.get("hours", "Check on-site")
    full       = int(round(s["rating"]))
    stars      = '<i class="fa-solid fa-star" style="color:#D97706"></i>'*full + '<i class="fa-regular fa-star" style="color:#D97706"></i>'*(5-full)
    mid        = "m" + str(abs(hash(name + city)) % 999999)
    ns         = name.replace("'", "\\'")
    cs         = city.replace("'", "\\'")
    review_cnt = str(int(s["rating"] * 800 + abs(hash(name)) % 3000))

    def H(x): return x.replace('"', '&quot;')

    modal = f"""
    <div id="{mid}" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9000;align-items:center;justify-content:center;backdrop-filter:blur(2px)">
      <div style="background:#fff;border-radius:14px;max-width:540px;width:92%;max-height:90vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,.2)">
        <div style="background:{col};padding:24px 24px 16px;border-radius:14px 14px 0 0;position:relative">
          <div style="font-size:28px;margin-bottom:8px;color:#fff">{icon}</div>
          <div style="font-weight:800;font-size:20px;color:#fff">{H(name)}</div>
          <div style="font-size:13px;color:rgba(255,255,255,.8);margin-top:4px"><i class="fa-solid fa-location-dot"></i> {H(city)}, Philippines &nbsp;·&nbsp; {s['cat']}</div>
          <button onclick="closeModal('{mid}')" style="position:absolute;top:14px;right:16px;background:rgba(255,255,255,.2);border:none;color:#fff;border-radius:50%;width:30px;height:30px;font-size:16px;cursor:pointer"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div style="padding:20px 24px">
          <img loading="lazy" src="{H(img)}" style="width:100%;height:200px;object-fit:cover;border-radius:10px;margin-bottom:16px"
               onerror="this.onerror=null;this.src='https://images.unsplash.com/photo-1519046904884-488729347d55?w=800&q=80&fit=crop&crop=center'"/>
          <div style="font-size:14px;margin-bottom:4px">{stars} <span style="color:#94A3B8;font-size:13px">{s['rating']}/5.0 &nbsp;·&nbsp; {review_cnt}+ reviews</span></div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:14px 0">
            <div style="background:#F8FAFC;border-radius:8px;padding:10px;border:1px solid #E2E8F0">
              <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;font-weight:600;letter-spacing:.3px">Entry Fee Range</div>
              <div style="font-weight:700;color:#0038A8;font-size:14px;margin-top:2px">{price_rng}</div>
            </div>
            <div style="background:#F8FAFC;border-radius:8px;padding:10px;border:1px solid #E2E8F0">
              <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;font-weight:600;letter-spacing:.3px">Hours</div>
              <div style="font-weight:700;font-size:13px;margin-top:2px">{hours}</div>
            </div>
          </div>
          <p style="font-size:13px;color:#475569;line-height:1.8;margin-bottom:16px">{desc}</p>
          <a href="{maps}" target="_blank" style="display:block;margin-bottom:10px">
            <button class="btn" style="background:#374151;color:#fff;width:100%;padding:9px;font-size:13px"><i class="fa-solid fa-map-location-dot"></i> View on Google Maps</button>
          </a>
          <button class="btn" style="background:{col};color:#fff;width:100%;padding:10px;font-size:13px;margin-bottom:8px"
                  onclick="addToItinerary('{ns}','{cs}');showGuidePrompt('{cs}');closeModal('{mid}')">
            <i class="fa-regular fa-calendar"></i> Add to Itinerary
          </button>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <a href="/guides.py?city={city}"><button class="btn" style="background:#059669;color:#fff;width:100%;padding:8px;font-size:12px"><i class="fa-solid fa-users"></i> Find a Guide</button></a>
            <a href="/restaurants.py?city={city}"><button class="btn" style="background:#0038A8;color:#fff;width:100%;padding:8px;font-size:12px"><i class="fa-solid fa-utensils"></i> Nearby Food</button></a>
          </div>
        </div>
      </div>
    </div>"""

    card = f"""
    {modal}
    <div class="grid-card" style="cursor:pointer" onclick="if(typeof ATLAS_LOGGED_IN!=='undefined'&&!ATLAS_LOGGED_IN){{openSigninGate();}}else{{document.getElementById('{mid}').style.display='flex';}}">
      <div style="position:relative;height:150px;overflow:hidden;border-radius:12px 12px 0 0;background:{col}">
        <img loading="lazy" src="{H(img)}" alt="{H(name)}" style="width:100%;height:100%;object-fit:cover;transition:transform .3s"
             onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'"
             onerror="this.onerror=null;this.src='https://images.unsplash.com/photo-1519046904884-488729347d55?w=800&q=80&fit=crop&crop=center'"/>
        <div style="position:absolute;inset:0;background:linear-gradient(to bottom,transparent 45%,rgba(0,0,0,.6) 100%)"></div>
        <div style="position:absolute;top:8px;right:8px;background:{col};color:#fff;border-radius:20px;padding:3px 10px;font-size:11px;font-weight:700">{s['cat']}</div>
        <div style="position:absolute;bottom:8px;left:10px;right:10px">
          <div style="font-weight:700;font-size:14px;color:#fff">{H(name)}</div>
        </div>
      </div>
      <div class="grid-card-body">
        <div style="font-size:12px;margin-bottom:4px">{stars} <span style="color:#94A3B8;font-size:11px">{s['rating']}</span></div>
        <div style="font-size:12px;color:#475569;margin-bottom:2px"><i class="fa-solid fa-location-dot" style="color:#0038A8"></i> {H(city)}</div>
        <div style="font-size:12px;color:#475569;margin-bottom:6px"><i class="fa-regular fa-clock" style="color:#0038A8"></i> {hours}</div>
        <div style="font-size:12px;font-weight:700;color:#0038A8;margin-bottom:6px">&#128179; {price_rng}</div>
        <div style="font-size:12px;color:#475569;line-height:1.5;margin-bottom:10px">{desc[:85]}...</div>
        <div style="font-size:12px;color:#0038A8;font-weight:600;text-align:center;padding:5px 0"><i class="fa-regular fa-eye"></i> View Details</div>
      </div>
    </div>"""
    return card

def render(filter_city="All", filter_cat="All", keyword="", user=None):
    results = get_spots(filter_city, keyword)
    if user and keyword:
        try:
            import db as _db
            _db.log_view(user["id"], "attraction", keyword, item_city=filter_city if filter_city != "All" else "")
        except: pass
    if filter_cat != "All":
        results = [s for s in results if s.get("cat") == filter_cat]

    cities    = ["All"] + sorted(CITY_COORDS.keys())
    city_opts = "".join(f'<option {"selected" if c==filter_city else ""}>{c}</option>' for c in cities)
    cat_opts  = "".join(f'<option {"selected" if c==filter_cat else ""}>{c}</option>'
                        for c in ["All","Nature","Historical","Heritage","Landmark","Museum"])
    cards     = "".join(_card(s) for s in results)
    empty     = ('<div class="guide-empty"><i class="fa-solid fa-magnifying-glass" style="font-size:32px;margin-bottom:10px;opacity:.4"></i>'
                 '<div style="font-weight:700;font-size:15px">No attractions found</div></div>' if not results else "")
    loc_note  = "across all cities" if filter_city=="All" else f"in {filter_city}"
    src_note  = "Live Foursquare results" if keyword else "Curated Luzon attractions"

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div style="font-size:28px;font-weight:900;color:#1F2937">Tourist Attractions</div>
        <div style="font-size:14px;color:#6B7280;margin-top:4px">Discover the best tourist spots across Luzon</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8"><span style="font-weight:700;font-size:14px">Filter and Search</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div><label class="lbl">City</label><select class="inp" name="city" style="width:160px">{city_opts}</select></div>
            <div><label class="lbl">Category</label><select class="inp" name="cat" style="width:160px">{cat_opts}</select></div>
            <div style="flex:1;min-width:160px"><label class="lbl">Keyword</label>
              <input class="inp" name="kw" placeholder="e.g. volcano, heritage..." value="{keyword}"/></div>
            <button class="btn" style="background:#0038A8;color:#fff;padding:10px 24px;font-weight:700" type="submit">Search</button>
          </form>
        </div>
      </div>
      <div style="margin-bottom:16px;font-size:13px;color:#94A3B8">{len(results)} attraction(s) found {loc_note} &nbsp;·&nbsp; {src_note}</div>
      <div class="page-grid3">{cards}</div>{empty}
    </div>

    <!-- Guide suggestion modal -->
    <div id="guide-prompt" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9100;align-items:center;justify-content:center;backdrop-filter:blur(2px)">
      <div style="background:#fff;border-radius:16px;max-width:420px;width:90%;padding:32px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.2)">
        <div style="font-size:40px;margin-bottom:12px">&#127968;</div>
        <div style="font-size:18px;font-weight:800;color:#1F2937;margin-bottom:8px">Want a local guide?</div>
        <div style="font-size:14px;color:#6B7280;line-height:1.6;margin-bottom:20px">
          Explore <strong id="guide-prompt-city"></strong> with a verified local tour guide who knows all the hidden gems.
        </div>
        <div style="display:flex;gap:10px">
          <a id="guide-prompt-link" href="/guides.py" style="flex:1;text-decoration:none">
            <button style="width:100%;padding:12px;background:#0038A8;color:#fff;border:none;border-radius:10px;font-size:14px;font-weight:700;cursor:pointer"><i class="fa-solid fa-users"></i> Find a Guide</button>
          </a>
          <button onclick="closeGuidePrompt()" style="flex:1;padding:12px;background:#F3F4F6;color:#374151;border:none;border-radius:10px;font-size:14px;font-weight:600;cursor:pointer">Maybe later</button>
        </div>
      </div>
    </div>
    <script>
    function closeModal(id){{var el=document.getElementById(id);if(el)el.style.display='none';}}
    function showGuidePrompt(city){{
      document.getElementById('guide-prompt-city').textContent=city;
      document.getElementById('guide-prompt-link').href='/guides.py?city='+encodeURIComponent(city);
      document.getElementById('guide-prompt').style.display='flex';
    }}
    function closeGuidePrompt(){{document.getElementById('guide-prompt').style.display='none';}}
    function addToItinerary(name,city){{
      var key='atlas_itinerary_items';
      var items=JSON.parse(localStorage.getItem(key)||'[]');
      if(!items.some(function(x){{return x.name===name&&x.city===city;}})){{
        items.push({{name:name,city:city,type:'attraction',time:'09:00',day:1,note:'',addedAt:new Date().toISOString()}});
        localStorage.setItem(key,JSON.stringify(items));
        showToast('&#10003; Added to itinerary: '+name);
      }}else{{showToast('Already in itinerary: '+name);}}
    }}
    </script>"""
    return build_shell("Attractions", body, "attractions", user=user)
