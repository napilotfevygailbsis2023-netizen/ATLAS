import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tourist_ui import build_shell
from data import TRANSPORT

COLORS = {"Bus":"#0038A8","Van":"#0038A8","Ferry":"#0038A8","Train":"#0038A8","Jeepney":"#0038A8"}
ICONS = {
  "Bus":     '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="13" rx="2"/><path d="M3 11h18"/><path d="M8 5V3"/><path d="M16 5V3"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/><path d="M5 18H3v-3"/><path d="M19 18h2v-3"/></svg>',
  "Van":     '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 17H3a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v9a2 2 0 0 1-2 2h-3"/><circle cx="7.5" cy="17.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>',
  "Ferry":   '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20c0 1 1 1 2 1s2 0 2-1 1-1 2-1 2 0 2 1 1 1 2 1 2 0 2-1 1-1 2-1 2 0 2 1"/><path d="M4 15h16l-3-8H7z"/><path d="M12 7V3"/><path d="M10 3h4"/></svg>',
  "Train":   '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="14" rx="2"/><path d="M4 11h16"/><path d="M8 3v8"/><circle cx="8.5" cy="19.5" r="2.5"/><circle cx="15.5" cy="19.5" r="2.5"/><path d="M6.5 22l2-2.5"/><path d="M17.5 22l-2-2.5"/></svg>',
  "Jeepney": '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 9l2-2h18l2 2v5H1z"/><path d="M4 14v3"/><path d="M20 14v3"/><circle cx="6" cy="17" r="2"/><circle cx="18" cy="17" r="2"/><path d="M8 9V7h8v2"/></svg>',
}

def _card(t):
    col   = COLORS.get(t["type"], "#374151")
    icon  = ICONS.get(t["type"], "&#128663;")
    tname = t["name"]
    tsched = t["schedule"]
    toast = f"showToast('Schedule: {tname} departs {tsched}')"
    return (
        '<div class="grid-card">'
        f'<div class="grid-card-top" style="background:linear-gradient(135deg,{col},{col}99)">'
        f'<div style="margin-bottom:10px">{icon}</div>'
        f'<div style="font-weight:800;font-size:15px;color:#fff;margin-bottom:4px">{tname}</div>'
        f'<span class="badge" style="background:rgba(255,255,255,.2);color:#fff">{t["type"]}</span>'
        '</div>'
        '<div class="grid-card-body">'
        f'<div style="font-size:13px;font-weight:700;color:#374151;margin-bottom:10px">&#128205; {t["route"]}</div>'
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px">'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">Duration</div><div style="font-weight:700;font-size:13px">{t["duration"]}</div></div>'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">Schedule</div><div style="font-weight:700;font-size:13px">{tsched}</div></div>'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">Class</div><div style="font-weight:700;font-size:13px">{t["class"]}</div></div>'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">Fare</div><div style="font-weight:700;font-size:13px;color:#CE1126">{t["price"]}</div></div>'
        '</div>'
        f'<button class="btn" style="background:{col};color:#fff;width:100%;padding:9px" onclick="{toast}">Check Schedules</button>'
        '</div></div>'
    )

def render(filter_type="All", filter_from="All", search="", user=None):
    filtered = [t for t in TRANSPORT
        if (filter_type=="All" or t["type"]==filter_type)
        and (filter_from=="All" or filter_from.lower() in t["route"].lower())
        and (not search or search.lower() in t["name"].lower() or search.lower() in t["route"].lower())]
    all_from = ["All","Manila","Baguio","Ilocos Norte","Vigan","Batangas","Tagaytay","Albay","Pangasinan","Bataan","La Union"]
    type_opts = "".join(f'<option {"selected" if x==filter_type else ""}>{x}</option>' for x in ["All","Bus","Van","Ferry","Train","Jeepney"])
    from_opts = "".join(f'<option {"selected" if x==filter_from else ""}>{x}</option>' for x in all_from)
    cards = "".join(_card(t) for t in filtered)
    empty = '<div class="guide-empty"><div style="font-size:40px;margin-bottom:10px">&#128652;</div><div style="font-weight:700;font-size:16px">No routes found</div></div>' if not filtered else ""

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Transportation</div>
        <div class="section-sub">Ground, sea and rail transport routes across Luzon</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8"><span>Search & Filter Routes</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div style="flex:1;min-width:200px"><label class="lbl">Search Routes</label>
              <input class="inp" name="search" placeholder="e.g. Manila to Baguio, Victory Liner..." value="{search}"/></div>
            <div><label class="lbl">Transport Type</label><select class="inp" name="type" style="width:150px">{type_opts}</select></div>
            <div><label class="lbl">Departure From</label><select class="inp" name="from" style="width:160px">{from_opts}</select></div>
            <button class="btn" style="background:#0038A8;color:#fff" type="submit">Search</button>
          </form>
        </div>
      </div>
      <div style="font-size:13px;color:#6B7280;margin-bottom:16px">{len(filtered)} route(s) found</div>
      <div class="page-grid3">{cards}</div>{empty}
    </div>"""
    return build_shell("Transportation", body, "transport", user=user)