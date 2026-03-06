import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import RESTAURANTS

TYPE_COLORS = {"Filipino":"#0038A8","Heritage Filipino":"#CE1126","Cafe":"#C8930A","Ilocano":"#065F46","Local Heritage":"#6B21A8","Bulalo":"#C8930A"}

def _card(r):
    col  = TYPE_COLORS.get(r["type"], "#0038A8")
    name = r["name"]
    maps = f"https://www.google.com/maps/search/{name.replace(' ','+')}+{r['city']}+Philippines"
    return (
        '<div class="card">'
        f'<div style="background:linear-gradient(135deg,{col},{col}CC);padding:14px 18px;display:flex;justify-content:space-between;align-items:center">'
        f'<span style="font-weight:800;font-size:16px;color:#fff">{name}</span>'
        f'<span style="color:#FCD116;font-weight:700">&#9733; {r["rating"]}</span>'
        '</div>'
        '<div style="padding:14px 18px">'
        f'<div style="font-size:13px;color:#6B7280;margin-bottom:4px">&#128205; {r["city"]}</div>'
        f'<div style="font-size:12px;color:#9CA3AF;margin-bottom:6px">{r["type"]}</div>'
        f'<div style="font-size:15px;font-weight:700;color:#CE1126;margin-bottom:14px">{r["price"]}</div>'
        f'<a href="{maps}" target="_blank"><button class="btn" style="background:{col};color:#fff">View Restaurant</button></a>'
        '</div></div>'
    )

def render(filter_city="All", keyword=""):
    filtered = [r for r in RESTAURANTS
        if (filter_city == "All" or r["city"] == filter_city)
        and (not keyword or keyword.lower() in r["name"].lower() or keyword.lower() in r["type"].lower() or keyword.lower() in r["city"].lower())]
    cities = ["All"] + sorted(set(r["city"] for r in RESTAURANTS))
    city_opts = "".join(f'<option {"selected" if c == filter_city else ""}>{c}</option>' for c in cities)
    cards = "".join(_card(r) for r in filtered)
    empty = '<div class="guide-empty"><div style="font-size:40px;margin-bottom:10px">&#127869;</div><div style="font-weight:700;font-size:16px">No restaurants found</div><div style="font-size:13px;margin-top:6px">Try a different city or keyword</div></div>' if not filtered else ""

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Restaurants</div>
        <div class="section-sub">Discover the best dining spots across Luzon</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#C8930A"><span>Search Restaurants</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div><label class="lbl">City</label>
              <select class="inp" name="city" style="width:180px">{city_opts}</select></div>
            <div style="flex:1;min-width:200px"><label class="lbl">Search by Name or Cuisine</label>
              <input class="inp" name="kw" placeholder="e.g. bulalo, cafe, Filipino..." value="{keyword}"/></div>
            <button class="btn" style="background:#C8930A;color:#fff" type="submit">Search</button>
          </form>
        </div>
      </div>
      <div style="margin-bottom:10px;font-size:13px;color:#6B7280">{len(filtered)} restaurant(s) found</div>
      <div class="rest-grid">{cards}</div>{empty}
    </div>"""
    return build_shell("Restaurants", body, "restaurants")
