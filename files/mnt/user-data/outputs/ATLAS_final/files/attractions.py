import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import SPOTS

CAT_COLORS = {"Nature":"#065F46","Historical":"#0038A8","Heritage":"#C8930A"}

def _card(s):
    col = CAT_COLORS.get(s["cat"], "#0038A8")
    name = s["name"].replace("'", "")
    city = s["city"]
    maps = f"https://www.google.com/maps/search/{name.replace(' ','+')}+{city}+Philippines"
    return (
        '<div class="spot-card">'
        f'<div class="spot-bar" style="background:{col}"></div>'
        '<div class="spot-body">'
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:8px">'
        f'<div style="display:flex;align-items:center;gap:12px">'
        f'<span style="font-weight:800;font-size:15px">{s["name"]}</span>'
        f'<span class="star">&#9733; {s["rating"]}</span>'
        f'<span style="font-size:12px;color:#9CA3AF">{s["visits"]}</span>'
        '</div>'
        f'<span class="badge" style="background:{col}">{s["cat"]}</span>'
        '</div>'
        f'<div style="font-size:12px;color:#6B7280;margin-bottom:8px">&#128205; {city} &nbsp;-&nbsp; Entry: <b style="color:#CE1126">{s["entry"]}</b> &nbsp;-&nbsp; {s["hours"]}</div>'
        f'<div style="font-size:13px;color:#374151;line-height:1.6;margin-bottom:14px">{s["desc"]}</div>'
        '<div style="display:flex;gap:8px;flex-wrap:wrap">'
        f'<button class="btn" style="background:{col};color:#fff" onclick="showToast(\'Added to itinerary: {name}\')">+ Add to Itinerary</button>'
        f'<a href="/restaurants.py?city={city}"><button class="btn" style="background:#CE1126;color:#fff">Nearby Restaurants</button></a>'
        f'<a href="{maps}" target="_blank"><button class="btn" style="background:#C8930A;color:#fff">Get Directions</button></a>'
        '</div></div></div>'
    )

def render(filter_city="All", filter_cat="All", keyword=""):
    results = [s for s in SPOTS
        if (filter_city == "All" or s["city"] == filter_city)
        and (filter_cat == "All" or s["cat"] == filter_cat)
        and (not keyword or keyword.lower() in s["name"].lower() or keyword.lower() in s["desc"].lower())]
    cities = ["All"] + sorted(set(s["city"] for s in SPOTS))
    city_opts = "".join(f'<option {"selected" if c == filter_city else ""}>{c}</option>' for c in cities)
    cat_opts  = "".join(f'<option {"selected" if c == filter_cat else ""}>{c}</option>' for c in ["All","Nature","Historical","Heritage"])
    cards = "".join(_card(s) for s in results)
    empty = '<div class="guide-empty"><div style="font-size:40px;margin-bottom:10px">&#128269;</div><div style="font-weight:700;font-size:16px">No attractions found</div><div style="font-size:13px;margin-top:6px">Try a different city or category</div></div>' if not results else ""

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
            <div><label class="lbl">City / Province</label>
              <select class="inp" name="city" style="width:180px">{city_opts}</select></div>
            <div><label class="lbl">Category</label>
              <select class="inp" name="cat" style="width:150px">{cat_opts}</select></div>
            <div style="flex:1;min-width:180px"><label class="lbl">Keyword</label>
              <input class="inp" name="kw" placeholder="e.g. volcano, heritage..." value="{keyword}"/></div>
            <button class="btn" style="background:#CE1126;color:#fff" type="submit">Search</button>
          </form>
        </div>
      </div>
      <div style="margin-bottom:10px;font-size:13px;color:#6B7280">{len(results)} attraction(s) found</div>
      {cards}{empty}
    </div>"""
    return build_shell("Attractions", body, "attractions")
