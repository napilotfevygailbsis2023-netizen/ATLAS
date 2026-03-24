import sys, os, urllib.request, urllib.parse, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import SPOTS as STATIC_SPOTS

FSQ_KEY = "JHNF2RTKPV0ISAD1DSYUZLMJRH3AC1EJ43B3LBDK0WLNBEMN"
CAT_COLORS = {"Nature":"#065F46","Historical":"#0038A8","Heritage":"#C8930A","Landmark":"#CE1126","Park":"#065F46","Museum":"#0038A8"}
CAT_ICONS  = {"Nature":"<i class='fa-solid fa-leaf'></i>","Historical":"<i class='fa-solid fa-landmark'></i>","Heritage":"<i class='fa-solid fa-place-of-worship'></i>","Landmark":"<i class='fa-solid fa-building'></i>","Park":"<i class='fa-solid fa-tree'></i>","Museum":"<i class='fa-solid fa-landmark'></i>"}

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

ATTRACTION_CATS = "16000,16020,16032,16034,16035"

def fetch_from_foursquare(city, keyword):
    """Only called when user types a keyword — live search via API."""
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
    """Main data function — static by default, Foursquare only when keyword given."""
    if keyword:
        # Use Foursquare for keyword search
        search_city = city if city != "All" else "Manila"
        fsq = fetch_from_foursquare(search_city, keyword)
        return fsq if fsq else [s for s in STATIC_SPOTS if keyword.lower() in s["name"].lower()]

    # No keyword — use clean static data
    if city == "All":
        return STATIC_SPOTS
    return [s for s in STATIC_SPOTS if s.get("city") == city]

def _card(s):
    col   = CAT_COLORS.get(s["cat"],"#0038A8")
    icon  = CAT_ICONS.get(s["cat"],"<i class='fa-solid fa-landmark'></i>")
    city  = s["city"]
    name  = s["name"]
    img   = s.get("img","") or ("https://source.unsplash.com/800x500/?" + urllib.parse.quote(name+" Philippines"))
    maps  = "https://www.google.com/maps/search/" + urllib.parse.quote(name) + "+" + urllib.parse.quote(city) + "+Philippines"
    desc  = s.get("desc","")
    entry = s.get("entry","Check on-site")
    hours = s.get("hours","Check on-site")
    full  = int(round(s["rating"]))
    stars = "<i class='fa-solid fa-star'></i>" * full + "<i class='fa-regular fa-star'></i>" * (5 - full)
    mid   = "m" + str(abs(hash(name + city)) % 999999)
    ns    = name.replace("'","\\'")
    cs    = city.replace("'","\\'")

    def H(x): return x.replace('"','&quot;')

    modal = (
        "<div id=\"" + mid + "\" style=\"display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:9000;align-items:center;justify-content:center\">"
        + "<div style=\"background:#fff;border-radius:16px;max-width:520px;width:90%;max-height:88vh;overflow-y:auto;box-shadow:0 8px 40px rgba(0,0,0,.25)\">"
        + "<div style=\"background:linear-gradient(135deg," + col + "," + col + "99);padding:24px 24px 16px;border-radius:16px 16px 0 0;position:relative\">"
        + "<div style=\"font-size:28px;margin-bottom:8px\">" + icon + "</div>"
        + "<div style=\"font-weight:800;font-size:18px;color:#fff\">" + H(name) + "</div>"
        + "<div style=\"font-size:13px;color:rgba(255,255,255,.8);margin-top:4px\"><i class='fa-solid fa-location-dot'></i> " + H(city) + "</div>"
        + "<button onclick=\"closeModal(&quot;" + mid + "&quot;)\" style=\"position:absolute;top:14px;right:16px;background:rgba(255,255,255,.2);border:none;color:#fff;border-radius:50%;width:30px;height:30px;font-size:18px;cursor:pointer\"><i class='fa-solid fa-xmark'></i></button>"
        + "</div><div style=\"padding:20px\">"
        + "<img src=\"" + H(img) + "\" style=\"width:100%;height:180px;object-fit:cover;border-radius:10px;margin-bottom:16px\" onerror=\"this.style.display='none'\"/>"
        + "<div style=\"color:#D97706;font-size:14px;margin-bottom:10px\">" + stars + " <span style=\"color:#94A3B8\">" + str(s["rating"]) + "</span></div>"
        + "<div style=\"display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px\">"
        + "<div style=\"background:#F9FAFB;border-radius:8px;padding:10px\"><div style=\"font-size:11px;color:#94A3B8;text-transform:uppercase;font-weight:600;letter-spacing:.3px\">Entry Fee</div><div style=\"font-weight:700;color:#DC2626;font-size:14px\">" + entry + "</div></div>"
        + "<div style=\"background:#F9FAFB;border-radius:8px;padding:10px\"><div style=\"font-size:11px;color:#94A3B8;text-transform:uppercase;font-weight:600;letter-spacing:.3px\">Hours</div><div style=\"font-weight:700;font-size:13px\">" + hours + "</div></div>"
        + "</div>"
        + "<p style=\"font-size:13px;color:#4B5563;line-height:1.7;margin-bottom:18px\">" + desc + "</p>"
        + "<div style=\"display:flex;flex-direction:column;gap:8px\">"
        + "<button class=\"btn\" style=\"background:" + col + ";color:#fff;width:100%;padding:10px;font-size:14px\" onclick=\"addToItinerary('" + ns + "','" + cs + "');closeModal(&quot;" + mid + "&quot;)\">+ Add to Itinerary</button>"
        + "<div style=\"display:grid;grid-template-columns:1fr 1fr;gap:8px\">"
        + "<a href=\"/restaurants.py?city=" + city + "\" style=\"display:block\"><button class=\"btn\" style=\"background:#0038A8;color:#fff;width:100%;padding:9px;font-size:13px\">Nearby Restaurants</button></a>"
        + "<a href=\"" + maps + "\" target=\"_blank\" style=\"display:block\"><button class=\"btn\" style=\"background:#1E3A5F;color:#fff;width:100%;padding:9px;font-size:13px\">Get Directions</button></a>"
        + "</div></div></div></div></div>"
    )
    card = (
        modal
        + "<div class=\"grid-card\" style=\"cursor:pointer\" onclick=\"if(typeof ATLAS_LOGGED_IN!=='undefined'&&!ATLAS_LOGGED_IN){openSigninGate();}else{document.getElementById(&quot;" + mid + "&quot;).style.display='flex';}\">"
        + "<div class=\"grid-card-top\" style=\"background:linear-gradient(135deg," + col + "," + col + "99)\">"
        + "<div style=\"font-size:32px;margin-bottom:10px\">" + icon + "</div>"
        + "<div style=\"font-weight:800;font-size:15px;color:#fff;margin-bottom:4px\">" + H(name) + "</div>"
        + "<span class=\"badge\" style=\"background:rgba(255,255,255,.2);color:#fff\">" + s["cat"] + "</span>"
        + "</div><div class=\"grid-card-body\">"
        + "<img src=\"" + H(img) + "\" alt=\"" + H(name) + "\" style=\"width:100%;height:130px;object-fit:cover;border-radius:10px;margin-bottom:10px\" onerror=\"this.style.display='none'\"/>"
        + "<div style=\"color:#D97706;font-size:13px;margin-bottom:6px\">" + stars + " <span style=\"color:#94A3B8\">" + str(s["rating"]) + "</span></div>"
        + "<div style=\"font-size:12px;color:#475569;margin-bottom:2px\"><i class='fa-solid fa-location-dot'></i> " + H(city) + "</div>"
        + "<div style=\"font-size:12px;color:#475569;margin-bottom:2px\"><i class='fa-regular fa-clock'></i> " + hours + "</div>"
        + "<div style=\"font-size:14px;font-weight:800;color:#DC2626;margin:8px 0 6px\">Entry: " + entry + "</div>"
        + "<div style=\"font-size:12px;color:#475569;line-height:1.5;margin-bottom:14px\">" + desc[:100] + "...</div>"
        + "<div style=\"font-size:12px;color:#0038A8;font-weight:600;text-align:center;padding:6px 0\"><i class='fa-regular fa-eye'></i> Click for details</div>"
        + "</div></div>"
    )
    return card


def render(filter_city="All", filter_cat="All", keyword="", user=None):
    results = get_spots(filter_city, keyword)
    if filter_cat != "All":
        results = [s for s in results if s.get("cat")==filter_cat]

    cities    = ["All"] + sorted(CITY_COORDS.keys())
    city_opts = "".join(f'<option {"selected" if c==filter_city else ""}>{c}</option>' for c in cities)
    cat_opts  = "".join(
        f'<option {"selected" if c==filter_cat else ""}>{c}</option>'
        for c in ["All","Nature","Historical","Heritage","Landmark","Museum","Park"]
    )
    cards = "".join(_card(s) for s in results)
    empty = (
        '<div class="guide-empty"><div style="font-size:32px;margin-bottom:10px"><i class=\'fa-solid fa-magnifying-glass\'></i></div>'
        '<div style="font-weight:700;font-size:16px">No attractions found</div></div>'
        if not results else ""
    )
    src_note = "Live Foursquare search results" if keyword else "Curated Luzon attractions"
    loc_note = "across all cities" if filter_city=="All" else f"in {filter_city}"

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Tourist Attractions</div>
        <div class="section-sub">{src_note} · Search by keyword to discover more via Foursquare API</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#1E3A5F"><span>Filter and Search</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div><label class="lbl">City</label><select class="inp" name="city" style="width:170px">{city_opts}</select></div>
            <div><label class="lbl">Category</label><select class="inp" name="cat" style="width:170px">{cat_opts}</select></div>
            <div style="flex:1;min-width:160px"><label class="lbl">Search via Foursquare API</label>
              <input class="inp" name="kw" placeholder="e.g. volcano, heritage, waterfall..." value="{keyword}"/></div>
            <button class="btn" style="background:#0038A8;color:#fff" type="submit">Search</button>
          </form>
        </div>
      </div>
      <div style="margin-bottom:16px;font-size:13px;color:#475569">{len(results)} attraction(s) found {loc_note}</div>
      <div class="page-grid3">{cards}</div>{empty}
    </div>
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
          showToast('✓ Added to itinerary: '+name);
        }} else {{
          showToast('Already in itinerary: '+name);
        }}
      }}
      // Close modals on backdrop click
      document.addEventListener('click', function(e) {{
        if(e.target.style && e.target.style.position === 'fixed' && e.target.style.inset === '0px') {{
          e.target.style.display = 'none';
        }}
      }});
    </script>"""
    return build_shell("Attractions", body, "attractions", user=user)
