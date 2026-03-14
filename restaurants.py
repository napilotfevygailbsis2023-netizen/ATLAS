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
    "La Union":     ("16.6159","120.3209"),
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
    col   = TYPE_COLORS[i % len(TYPE_COLORS)]
    name  = r["name"]
    city  = r["city"]
    maps  = "https://www.google.com/maps/search/" + urllib.parse.quote(name) + "+" + urllib.parse.quote(city) + "+Philippines"
    img   = r.get("img","") or ("https://source.unsplash.com/900x600/?" + urllib.parse.quote(name+" food"))
    desc  = r.get("desc","") or ("Popular " + r.get("type","Filipino") + " dining in " + city + ".")
    full  = int(round(r["rating"]))
    stars = "&#9733;" * full + "&#9734;" * (5 - full)
    price = r.get("price","Check restaurant")
    rtype = r.get("type","Filipino")
    mid   = "rm" + str(abs(hash(name + city)) % 999999)

    def H(s): return s.replace('"', '&quot;')

    modal = (
        "<div id=\"" + mid + "\" style=\"display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:9000;align-items:center;justify-content:center\">"
        + "<div style=\"background:#fff;border-radius:16px;max-width:500px;width:90%;max-height:88vh;overflow-y:auto;box-shadow:0 8px 40px rgba(0,0,0,.25)\">"
        + "<div style=\"background:linear-gradient(135deg," + col + "," + col + "99);padding:24px 24px 16px;border-radius:16px 16px 0 0;position:relative\">"
        + "<div style=\"font-size:36px;margin-bottom:8px\">&#127869;</div>"
        + "<div style=\"font-weight:800;font-size:18px;color:#fff\">" + H(name) + "</div>"
        + "<div style=\"font-size:13px;color:rgba(255,255,255,.8);margin-top:4px\">&#128205; " + H(city) + " &middot; " + H(rtype) + "</div>"
        + "<button onclick=\"closeModal(&quot;" + mid + "&quot;)\" style=\"position:absolute;top:14px;right:16px;background:rgba(255,255,255,.2);border:none;color:#fff;border-radius:50%;width:30px;height:30px;font-size:18px;cursor:pointer\">&#x2715;</button>"
        + "</div><div style=\"padding:20px 24px\">"
        + "<img src=\"" + H(img) + "\" alt=\"" + H(name) + "\" style=\"width:100%;height:170px;object-fit:cover;border-radius:10px;margin-bottom:16px\" onerror=\"this.style.display='none'\"/>"
        + "<div style=\"color:#F59E0B;font-size:14px;margin-bottom:10px\">" + stars + " <span style=\"color:#9CA3AF\">" + str(r["rating"]) + "</span></div>"
        + "<div style=\"background:#FEF3C7;border-radius:8px;padding:12px;margin-bottom:14px;text-align:center\">"
        + "<div style=\"font-size:10px;color:#9CA3AF;text-transform:uppercase;font-weight:600\">Price Range</div>"
        + "<div style=\"font-weight:800;color:#CE1126;font-size:18px\">" + price + "</div></div>"
        + "<p style=\"font-size:13px;color:#4B5563;line-height:1.7;margin-bottom:18px\">" + desc + "</p>"
        + "<a href=\"" + maps + "\" target=\"_blank\" style=\"display:block\">"
        + "<button class=\"btn\" style=\"background:" + col + ";color:#fff;width:100%;padding:11px;font-size:14px\">&#128205; View on Google Maps</button>"
        + "</a></div></div></div>"
    )
    card = (
        modal
        + "<div class=\"rest-card3\" style=\"cursor:pointer\" onclick=\"document.getElementById(&quot;" + mid + "&quot;).style.display='flex'\">"
        + "<div class=\"rest-card3-top\" style=\"background:linear-gradient(135deg," + col + "," + col + "99)\">"
        + "<div style=\"font-size:36px;margin-bottom:10px\">&#127869;</div>"
        + "<div style=\"font-weight:800;font-size:15px;color:#fff;line-height:1.3;margin-bottom:4px\">" + H(name) + "</div>"
        + "<div style=\"font-size:12px;color:rgba(255,255,255,.75)\">" + H(rtype) + "</div>"
        + "</div><div class=\"rest-card3-body\">"
        + "<img src=\"" + H(img) + "\" alt=\"" + H(name) + "\" style=\"width:100%;height:135px;object-fit:cover;border-radius:10px;margin-bottom:10px\" onerror=\"this.style.display='none'\"/>"
        + "<div style=\"color:#F59E0B;font-size:13px;margin-bottom:6px\">" + stars + " <span style=\"color:#9CA3AF;font-size:12px\">" + str(r["rating"]) + "</span></div>"
        + "<div style=\"font-size:12px;color:#6B7280;margin-bottom:3px\">&#128205; " + H(city) + "</div>"
        + "<div style=\"font-size:12px;color:#6B7280;line-height:1.55;margin:8px 0 10px\">" + desc[:120] + "</div>"
        + "<div style=\"font-size:18px;font-weight:800;color:#CE1126;margin:10px 0 8px\">" + price + "</div>"
        + "<div style=\"font-size:12px;color:#0038A8;font-weight:600;text-align:center;padding:4px 0\">&#128065; Click for details &amp; map</div>"
        + "</div></div>"
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
              <select class="inp" name="city" style="width:160px">{{city_opts}}</select></div>
            <div><label class="lbl">Cuisine Type</label>
              <select class="inp" name="type" style="width:160px">{{type_opts}}</select></div>
            <div style="flex:1;min-width:180px"><label class="lbl">Search via Foursquare API</label>
              <input class="inp" name="kw" placeholder="e.g. bulalo, cafe, seafood..." value="{{keyword}}"/></div>
            <button class="btn" style="background:#C8930A;color:#fff" type="submit">Search</button>
          </form>
        </div>
      </div>
      <div style="margin-bottom:16px;font-size:13px;color:#6B7280">{len(filtered)} restaurant(s) found {loc_note}</div>
      <div class="rest-grid3">{cards}</div>{empty}
    </div>
    <script>
      function closeModal(id) {{
        var el = document.getElementById(id);
        if (el) el.style.display = 'none';
      }}
      document.addEventListener('click', function(e) {{
        if(e.target && e.target.style && e.target.style.position === 'fixed' && e.target.style.inset === '0px') {{
          e.target.style.display = 'none';
        }}
      }});
    </script>"""
    return build_shell("Restaurants", body, "restaurants", user=user)
