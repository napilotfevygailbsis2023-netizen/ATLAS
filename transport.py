#!/usr/bin/env python3
# ── FILE: transport.py ────────────────────────────────────────────────────────
# CHANGES: All routes are Luzon-only.
#          Added all major Luzon departure points to filter.
#          "Check Schedules" button opens booking/info toast.
#          Removed old API text.

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import TRANSPORT

COLORS = {"Bus":"#0038A8","Van":"#CE1126","Ferry":"#065F46","Train":"#6B21A8","Jeepney":"#C8930A"}
ICONS  = {"Bus":"🚌","Van":"🚐","Ferry":"⛴️","Train":"🚆","Jeepney":"🚌"}

def _card(t):
    col  = COLORS.get(t["type"], "#374151")
    icon = ICONS.get(t["type"], "🚗")
    name = t["name"].replace("'","&#39;")
    return (
        '<div class="transport-card">'
        f'<div class="transport-icon" style="background:{col};color:#fff">{icon}</div>'
        '<div style="flex:1">'
        '<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:8px">'
        f'<div><div style="font-weight:800;font-size:15px">{t["name"]}</div>'
        f'<div style="font-size:13px;color:#6B7280">📍 {t["route"]}</div></div>'
        f'<span class="badge" style="background:{col}">{t["type"]}</span>'
        '</div>'
        '<div style="display:flex;gap:18px;flex-wrap:wrap;margin-bottom:12px">'
        f'<div><div style="font-size:11px;color:#9CA3AF">⏱️ Duration</div><div style="font-weight:700;font-size:13px">{t["duration"]}</div></div>'
        f'<div><div style="font-size:11px;color:#9CA3AF">🕐 Schedule</div><div style="font-weight:700;font-size:13px">{t["schedule"]}</div></div>'
        f'<div><div style="font-size:11px;color:#9CA3AF">💺 Class</div><div style="font-weight:700;font-size:13px">{t["class"]}</div></div>'
        f'<div><div style="font-size:11px;color:#9CA3AF">💰 Fare</div><div style="font-weight:700;font-size:13px;color:#CE1126">{t["price"]}</div></div>'
        '</div>'
        f'<button class="btn" style="background:{col};color:#fff" onclick="showToast(\"Departures: "+t["schedule"]+"\")">Check Schedules</button>'
        '</div></div>'
    )

def render(filter_type="All", filter_from="All"):
    filtered = [
        t for t in TRANSPORT
        if (filter_type == "All" or t["type"] == filter_type)
        and (filter_from == "All" or filter_from.lower() in t["route"].lower())
    ]

    # All Luzon departure cities
    all_from = ["All","Manila","Baguio","Ilocos Norte","Vigan","Batangas","Tagaytay","Tuguegarao","Legazpi"]
    type_opts = "".join(f'<option {"selected" if x == filter_type else ""}>{x}</option>'
                        for x in ["All","Bus","Van","Ferry","Train","Jeepney"])
    from_opts = "".join(f'<option {"selected" if x == filter_from else ""}>{x}</option>'
                        for x in all_from)
    cards = "".join(_card(t) for t in filtered)
    no_results = '<div class="guide-empty"><div style="font-size:40px;margin-bottom:10px">🚌</div><div style="font-weight:700;font-size:16px;margin-bottom:6px">No routes found</div><div style="font-size:13px">Try a different transport type or departure point</div></div>' if not filtered else ""

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">🚌 Transportation</div>
        <div class="section-sub">Ground, sea, and rail transport routes across Luzon</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#065F46"><span>Filter Routes</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div><label class="lbl">Transport Type</label>
              <select class="inp" name="type" style="width:160px">{type_opts}</select></div>
            <div><label class="lbl">Departure Point</label>
              <select class="inp" name="from" style="width:180px">{from_opts}</select></div>
            <button class="btn" style="background:#065F46;color:#fff" type="submit">Search Routes</button>
          </form>
        </div>
      </div>
      <div style="font-size:13px;color:#6B7280;margin-bottom:12px">{len(filtered)} route(s) found</div>
      {cards}{no_results}
    </div>"""

    return build_shell("Transportation", body, "transport")

if __name__ == "__main__":
    print(render())
