import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import SPOTS

CAT_COLORS = {"Nature":"#065F46","Historical":"#0038A8","Heritage":"#C8930A"}
CAT_ICONS  = {"Nature":"&#127807;","Historical":"&#127963;","Heritage":"&#9962;"}

def _card(s):
    col  = CAT_COLORS.get(s["cat"], "#0038A8")
    icon = CAT_ICONS.get(s["cat"], "&#127963;")
    name = s["name"].replace("'","")
    city = s["city"]
    maps = f"https://www.google.com/maps/search/{name.replace(' ','+')}+{city}+Philippines"
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
        f'<div style="font-size:12px;color:#6B7280;line-height:1.5;margin-bottom:14px">{s["desc"][:80]}...</div>'
        '<div style="display:flex;flex-direction:column;gap:7px">'
        f'<button class="btn" style="background:{col};color:#fff;width:100%;padding:8px" onclick="showToast(\'Added: {name}\')">+ Add to Itinerary</button>'
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:7px">'
        f'<a href="/restaurants.py?city={city}" style="display:block"><button class="btn" style="background:#CE1126;color:#fff;width:100%;padding:7px;font-size:12px">Nearby Food</button></a>'
        f'<a href="{maps}" target="_blank" style="display:block"><button class="btn" style="background:#C8930A;color:#fff;width:100%;padding:7px;font-size:12px">Directions</button></a>'
        '</div></div></div></div>'
    )

def render(filter_city="All", filter_cat="All", keyword=""):
    results = [s for s in SPOTS
        if (filter_city=="All" or s["city"]==filter_city)
        and (filter_cat=="All" or s["cat"]==filter_cat)
        and (not keyword or keyword.lower() in s["name"].lower() or keyword.lower() in s["desc"].lower())]
    cities = ["All"] + sorted(set(s["city"] for s in SPOTS))
    city_opts = "".join(f'<option {"selected" if c==filter_city else ""}>{c}</option>' for c in cities)
    cat_opts  = "".join(f'<option {"selected" if c==filter_cat else ""}>{c}</option>' for c in ["All","Nature","Historical","Heritage"])
    cards = "".join(_card(s) for s in results)
    empty = '<div class="guide-empty"><div style="font-size:40px;margin-bottom:10px">&#128269;</div><div style="font-weight:700;font-size:16px">No attractions found</div></div>' if not results else ""

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Tourist Attractions</div>
        <div class="section-sub">Discover the best tourist spots across Luzon</div>
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
