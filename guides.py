import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import GUIDES

COLORS = ["#0038A8","#CE1126","#C8930A","#6B21A8","#0077B6","#065F46"]

def _card(g, i):
    col  = COLORS[i % len(COLORS)]
    name = g["name"].replace("'","")
    full = int(round(g["rating"]))
    stars = "&#9733;" * full + "&#9734;" * (5 - full)
    pkgs = "".join(f'<div style="font-size:11px;color:#6B7280;padding:3px 0;border-bottom:1px solid #F3F4F6">{p}</div>' for p in g["pkgs"])
    return (
        '<div class="grid-card">'
        f'<div class="grid-card-top" style="background:linear-gradient(135deg,{col},{col}99)">'
        f'<div style="width:56px;height:56px;border-radius:50%;background:rgba(255,255,255,.25);display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:900;color:#fff;margin:0 auto 10px">{g["name"][0]}</div>'
        f'<div style="font-weight:800;font-size:15px;color:#fff;margin-bottom:3px">{g["name"]}</div>'
        f'<div style="font-size:12px;color:rgba(255,255,255,.8)">{g["spec"]}</div>'
        '</div>'
        '<div class="grid-card-body">'
        f'<div style="color:#F59E0B;font-size:13px;margin-bottom:8px">{stars} <span style="color:#9CA3AF">{g["rating"]} ({g["tours"]} tours)</span></div>'
        f'<div style="font-size:12px;color:#6B7280;margin-bottom:2px">&#128205; {g["city"]}</div>'
        f'<div style="font-size:12px;color:#6B7280;margin-bottom:2px">&#127760; {g["lang"]}</div>'
        f'<div style="font-size:12px;color:#6B7280;margin-bottom:8px">&#128197; {g["avail"]}</div>'
        f'<div style="font-size:16px;font-weight:800;color:{col};margin-bottom:10px">{g["rate"]}</div>'
        f'<div style="margin-bottom:14px">{pkgs}</div>'
        '<div style="display:flex;flex-direction:column;gap:7px">'
        f'<button class="btn" style="background:#CE1126;color:#fff;width:100%;padding:9px" onclick="openBookingModal(\'{name}\')">Book This Guide</button>'
        f'<button class="btn-outline" style="width:100%;padding:8px;color:{col};border-color:{col}" onclick="showToast(\'Viewing profile: {name}\')">View Profile</button>'
        '</div></div></div>'
    )

def render(filter_city="All", filter_lang="All", user=None):
    cities = ["All"] + sorted(set(g["city"] for g in GUIDES))
    city_opts = "".join(f'<option {"selected" if c==filter_city else ""}>{c}</option>' for c in cities)
    lang_opts = "".join(f'<option {"selected" if l==filter_lang else ""}>{l}</option>' for l in ["All","EN","FIL","ES","IL"])
    filtered = [g for g in GUIDES
        if (filter_city=="All" or g["city"]==filter_city)
        and (filter_lang=="All" or filter_lang in g["lang"])]
    guide_html = "".join(_card(g,i) for i,g in enumerate(filtered)) if filtered else '<div class="guide-empty"><div style="font-size:48px;margin-bottom:12px">&#129517;</div><div style="font-weight:700;font-size:18px">No Tour Guides Available Yet</div></div>'
    count = f"{len(filtered)} guide(s) available" if filtered else "0 guides found"

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Tour Guide Booking</div>
        <div class="section-sub">Book a verified local guide for your Luzon trip</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#6B21A8"><span>Search Guides</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div><label class="lbl">City</label><select class="inp" name="city" style="width:180px">{city_opts}</select></div>
            <div><label class="lbl">Language</label><select class="inp" name="lang" style="width:140px">{lang_opts}</select></div>
            <button class="btn" style="background:#6B21A8;color:#fff" type="submit">Find Guides</button>
          </form>
        </div>
      </div>
      <div style="font-size:13px;color:#6B7280;margin-bottom:16px">{count}</div>
      <div class="page-grid3">{guide_html}</div>
    </div>"""
    return build_shell("Tour Guides", body, "guides", user=user)
