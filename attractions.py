import sys, os, urllib.request, urllib.parse, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import SPOTS as STATIC_SPOTS

FSQ_KEY = "JHNF2RTKPV0ISAD1DSYUZLMJRH3AC1EJ43B3LBDK0WLNBEMN"

CAT_COLORS = {
    "Nature":     "#0038A8",
    "Historical": "#0038A8",
    "Heritage":   "#0038A8",
    "Landmark":   "#0038A8",
    "Park":       "#0038A8",
    "Museum":     "#0038A8",
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
    "Albay":        ("13.1391","123.7438"),
    "Baguio":       ("16.4023","120.5960"),
    "Bataan":       ("14.6417","120.4818"),
    "Batangas":     ("13.7565","121.0583"),
    "Ilocos Norte": ("18.1977","120.5778"),
    "La Union":     ("16.6159","120.3209"),
    "Manila":       ("14.5995","120.9842"),
    "Pangasinan":   ("15.8949","120.2863"),
    "Tagaytay":     ("14.1153","120.9621"),
    "Vigan":        ("17.5747","120.3873"),
}

def fetch_from_foursquare(city, keyword):
    try:
        lat, lng = CITY_COORDS.get(city, ("14.5995","120.9842"))
        url = (
            "https://api.foursquare.com/v3/places/search"
            f"?query={urllib.parse.quote(keyword+' '+city)}&ll={lat},{lng}&radius=20000&limit=9"
        )
        req = urllib.request.Request(url, headers={"Authorization": FSQ_KEY, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=6) as r:
            d = json.loads(r.read())
        results = []
        for p in d.get("results", []):
            cats = p.get("categories", [{}])
            cat_name = cats[0].get("name","Attraction") if cats else "Attraction"
            cat_l = cat_name.lower()
            cat_short = (
                "Nature"  if any(x in cat_l for x in ["park","garden","nature","mountain","volcano","beach","lake"])
                else "Heritage" if any(x in cat_l for x in ["heritage","church","historic","monument","shrine"])
                else "Museum"   if "museum" in cat_l
                else "Landmark"
            )
            name = p.get("name","Unknown")
            results.append({
                "name":   name, "city": city, "cat": cat_short,
                "rating": round(p.get("rating",8.0)/2,1) if p.get("rating") else 4.0,
                "entry":  "Check on-site", "hours": "Check on-site",
                "desc":   f"{name} is a notable spot in {city} worth visiting.",
                "img":    f"https://source.unsplash.com/800x500/?{urllib.parse.quote(name+' '+city)}",
            })
        return results
    except:
        return []

def get_spots(city="All", keyword=""):
    if keyword:
        search_city = city if city != "All" else "Manila"
        fsq = fetch_from_foursquare(search_city, keyword)
        return fsq if fsq else [s for s in STATIC_SPOTS if keyword.lower() in s["name"].lower()]
    if city == "All":
        return STATIC_SPOTS
    return [s for s in STATIC_SPOTS if s.get("city") == city]

def _card(s):
    col   = CAT_COLORS.get(s["cat"], "#1E3A5F")
    icon  = CAT_ICONS.get(s["cat"], '<i class="fa-solid fa-landmark"></i>')
    city  = s["city"]
    name  = s["name"]
    img   = s.get("img","") or ("https://source.unsplash.com/800x500/?" + urllib.parse.quote(name+" Philippines"))
    maps  = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(name+' '+city+' Philippines')}"
    desc  = s.get("desc","")
    entry = s.get("entry","Check on-site")
    hours = s.get("hours","Check on-site")
    full  = int(round(s["rating"]))
    stars = '<i class="fa-solid fa-star" style="color:#D97706"></i>' * full + '<i class="fa-regular fa-star" style="color:#D97706"></i>' * (5 - full)
    mid   = "m" + str(abs(hash(name + city)) % 999999)
    ns    = name.replace("'","\\'")
    cs    = city.replace("'","\\'")

    def H(x): return x.replace('"','&quot;')

    modal = f"""
    <div id="{mid}" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9000;align-items:center;justify-content:center;backdrop-filter:blur(2px)">
      <div style="background:#fff;border-radius:14px;max-width:520px;width:90%;max-height:88vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,.2)">
        <div style="background:{col};padding:24px 24px 16px;border-radius:14px 14px 0 0;position:relative">
          <div style="font-size:28px;margin-bottom:8px;color:#fff">{icon}</div>
          <div style="font-weight:800;font-size:18px;color:#fff">{H(name)}</div>
          <div style="font-size:13px;color:rgba(255,255,255,.8);margin-top:4px"><i class="fa-solid fa-location-dot"></i> {H(city)}</div>
          <button onclick="closeModal('{mid}')" style="position:absolute;top:14px;right:16px;background:rgba(255,255,255,.2);border:none;color:#fff;border-radius:50%;width:30px;height:30px;font-size:16px;cursor:pointer"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div style="padding:20px 24px">
          <img src="{H(img)}" style="width:100%;height:180px;object-fit:cover;border-radius:10px;margin-bottom:16px" onerror="this.style.display='none'"/>
          <div style="font-size:14px;margin-bottom:10px">{stars} <span style="color:#94A3B8;font-size:13px">{s['rating']}</span></div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px">
            <div style="background:#F8FAFC;border-radius:8px;padding:10px;border:1px solid #E2E8F0">
              <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;font-weight:600;letter-spacing:.3px">Entry Fee</div>
              <div style="font-weight:700;color:#0038A8;font-size:14px;margin-top:2px">{entry}</div>
            </div>
            <div style="background:#F8FAFC;border-radius:8px;padding:10px;border:1px solid #E2E8F0">
              <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;font-weight:600;letter-spacing:.3px">Hours</div>
              <div style="font-weight:700;font-size:13px;margin-top:2px">{hours}</div>
            </div>
          </div>
          <p style="font-size:13px;color:#475569;line-height:1.7;margin-bottom:18px">{desc}</p>
          <div style="display:flex;flex-direction:column;gap:8px">
            <button class="btn" style="background:{col};color:#fff;width:100%;padding:10px;font-size:13px" onclick="addToItinerary('{ns}','{cs}');closeModal('{mid}')"><i class="fa-regular fa-calendar"></i> Add to Itinerary</button>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
              <a href="/restaurants.py?city={city}" style="display:block"><button class="btn" style="background:#0038A8;color:#fff;width:100%;padding:9px;font-size:13px"><i class="fa-solid fa-utensils"></i> Nearby Food</button></a>
              <a href="{maps}" target="_blank" style="display:block"><button class="btn" style="background:#0038A8;color:#fff;width:100%;padding:9px;font-size:13px"><i class="fa-solid fa-location-dot"></i> Directions</button></a>
            </div>
          </div>
        </div>
      </div>
    </div>"""

    card = f"""
    {modal}
    <div class="grid-card" style="cursor:pointer" onclick="if(typeof ATLAS_LOGGED_IN!=='undefined'&&!ATLAS_LOGGED_IN){{openSigninGate();}}else{{document.getElementById('{mid}').style.display='flex';}}">
      <div class="grid-card-top" style="background:{col}">
        <div style="font-size:28px;margin-bottom:10px;color:#fff">{icon}</div>
        <div style="font-weight:700;font-size:14px;color:#fff;margin-bottom:6px">{H(name)}</div>
        <span style="background:rgba(255,255,255,.2);color:#fff;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600">{s['cat']}</span>
      </div>
      <div class="grid-card-body">
        <img src="{H(img)}" alt="{H(name)}" style="width:100%;height:130px;object-fit:cover;border-radius:8px;margin-bottom:10px" onerror="this.style.display='none'"/>
        <div style="font-size:12px;margin-bottom:6px">{stars} <span style="color:#94A3B8;font-size:12px">{s['rating']}</span></div>
        <div style="font-size:12px;color:#475569;margin-bottom:2px"><i class="fa-solid fa-location-dot" style="color:#0038A8"></i> {H(city)}</div>
        <div style="font-size:12px;color:#475569;margin-bottom:8px"><i class="fa-regular fa-clock" style="color:#0038A8"></i> {hours}</div>
        <div style="font-size:13px;font-weight:700;color:#0038A8;margin-bottom:6px">Entry: {entry}</div>
        <div style="font-size:12px;color:#475569;line-height:1.5;margin-bottom:12px">{desc[:80]}...</div>
        <div style="font-size:12px;color:#0038A8;font-weight:600;text-align:center;padding:5px 0"><i class="fa-regular fa-eye"></i> View Details</div>
      </div>
    </div>"""
    return card


def render(filter_city="All", filter_cat="All", keyword="", user=None):
    results = get_spots(filter_city, keyword)
    if filter_cat != "All":
        results = [s for s in results if s.get("cat") == filter_cat]

    cities    = ["All"] + sorted(CITY_COORDS.keys())
    city_opts = "".join(f'<option {"selected" if c==filter_city else ""}>{c}</option>' for c in cities)
    cat_opts  = "".join(
        f'<option {"selected" if c==filter_cat else ""}>{c}</option>'
        for c in ["All","Nature","Historical","Heritage","Landmark","Museum"]
    )
    cards = "".join(_card(s) for s in results)
    empty = (
        '<div class="guide-empty"><i class="fa-solid fa-magnifying-glass" style="font-size:32px;margin-bottom:10px;opacity:.4"></i>'
        '<div style="font-weight:700;font-size:15px">No attractions found</div></div>'
        if not results else ""
    )
    src_note = "Live Foursquare results" if keyword else "Curated Luzon attractions"
    loc_note = "across all cities" if filter_city=="All" else f"in {filter_city}"

    body = f"""
    <div class="page-wrap">
      <div class="page-header">
        <div class="page-header-title">Tourist Attractions</div>
        <div class="page-header-sub">{src_note} &middot; Search by keyword to discover more</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr"><span><i class="fa-solid fa-filter"></i> Filter and Search</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div><label class="lbl">City</label><select class="inp" name="city" style="width:160px">{city_opts}</select></div>
            <div><label class="lbl">Category</label><select class="inp" name="cat" style="width:160px">{cat_opts}</select></div>
            <div style="flex:1;min-width:160px"><label class="lbl">Search via Foursquare</label>
              <input class="inp" name="kw" placeholder="e.g. volcano, heritage, waterfall..." value="{keyword}"/></div>
            <button class="btn" style="background:#0038A8;color:#fff" type="submit"><i class="fa-solid fa-magnifying-glass"></i> Search</button>
          </form>
        </div>
      </div>
      <div style="margin-bottom:16px;font-size:13px;color:#94A3B8">{len(results)} attraction(s) found {loc_note}</div>
      <div class="page-grid3">{cards}</div>{empty}
    </div>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
    <script>
      function closeModal(id) {{
        var el = document.getElementById(id);
        if (el) el.style.display = 'none';
      }}
      function addToItinerary(name, city) {{
        var key='atlas_itinerary_items';
        var items=JSON.parse(localStorage.getItem(key)||'[]');
        if(!items.some(function(x){{return x.name===name&&x.city===city;}})){{
          items.push({{name:name,city:city,type:'attraction',time:'09:00',day:1,note:'',addedAt:new Date().toISOString()}});
          localStorage.setItem(key,JSON.stringify(items));
          showToast('Added to itinerary: '+name);
        }} else {{
          showToast('Already in itinerary: '+name);
        }}
      }}
      document.addEventListener('click', function(e) {{
        if(e.target.id && e.target.style && e.target.style.position === 'fixed') {{
          e.target.style.display = 'none';
        }}
      }});
    </script>"""
    return build_shell("Attractions", body, "attractions", user=user)
