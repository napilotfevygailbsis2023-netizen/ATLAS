import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import RESTAURANTS

TYPE_COLORS = {"Filipino":"#0038A8","Heritage Filipino":"#CE1126","Cafe":"#C8930A","Ilocano":"#065F46","Local Heritage":"#6B21A8","Bulalo":"#C8930A"}

def _card(r):
    col  = TYPE_COLORS.get(r["type"], "#0038A8")
    name = r["name"]
    maps = f"https://www.google.com/maps/search/{name.replace(' ','+')}+{r['city']}+Philippines"
    full = int(round(r["rating"]))
    stars = "&#9733;" * full + "&#9734;" * (5 - full)
    return (
        '<div class="rest-card3">'
        f'<div class="rest-card3-top" style="background:linear-gradient(135deg,{col},{col}99)">'
        f'<div style="font-size:36px;margin-bottom:10px">&#127869;</div>'
        f'<div style="font-weight:800;font-size:15px;color:#fff;line-height:1.3;margin-bottom:4px">{name}</div>'
        f'<div style="font-size:12px;color:rgba(255,255,255,.75)">{r["type"]}</div>'
        '</div>'
        '<div class="rest-card3-body">'
        f'<div style="color:#F59E0B;font-size:13px;margin-bottom:6px">{stars} <span style="color:#9CA3AF;font-size:12px">{r["rating"]}</span></div>'
        f'<div style="font-size:12px;color:#6B7280;margin-bottom:3px">&#128205; {r["city"]}</div>'
        f'<div style="font-size:18px;font-weight:800;color:#CE1126;margin:10px 0 14px">{r["price"]}</div>'
        f'<a href="{maps}" target="_blank" style="display:block">'
        f'<button class="btn" style="background:{col};color:#fff;width:100%;padding:9px;font-size:13px">View Restaurant</button>'
        f'</a>'
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
      <div style="margin-bottom:16px;font-size:13px;color:#6B7280">{len(filtered)} restaurant(s) found</div>
      <div class="rest-grid3">{cards}</div>{empty}
    </div>"""
    return build_shell("Restaurants", body, "restaurants")
