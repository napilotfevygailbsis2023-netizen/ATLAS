#!/usr/bin/env python3
# ── FILE: guides.py ──────────────────────────────────────────────────────────
# CHANGES: Shows proper empty state when no guides registered yet.
#          Removed API credit text.
#          Book button opens booking modal correctly.
#          "View Profile" shows toast with guide info.

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
from data import GUIDES

AVATAR_COLORS = ["#0038A8","#CE1126","#C8930A","#6B21A8","#0077B6","#065F46"]

def _guide_card(g, i):
    col  = AVATAR_COLORS[i % len(AVATAR_COLORS)]
    name = g["name"].replace("'","&#39;")
    pkg_items = "".join(
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:5px">'
        f'<div style="width:4px;height:16px;background:{col};border-radius:2px;flex-shrink:0"></div>'
        f'<span style="font-size:13px;color:#374151">{p}</span></div>'
        for p in g["pkgs"]
    )
    return (
        '<div class="guide-card">'
        f'<div class="guide-top" style="background:{col}">'
        f'<div class="guide-avatar" style="color:{col}">{g["name"][0]}</div>'
        '<div style="flex:1">'
        f'<div style="font-weight:800;font-size:16px;color:#fff">{g["name"]}</div>'
        f'<div style="font-size:13px;color:rgba(255,255,255,.8)">{g["city"]} · {g["spec"]}</div>'
        '</div>'
        '<div style="text-align:right">'
        f'<div style="color:#FCD116;font-weight:800;font-size:18px">★ {g["rating"]}</div>'
        f'<div style="font-size:12px;color:rgba(255,255,255,.7)">{g["tours"]} tours completed</div>'
        '</div></div>'
        '<div style="padding:16px 22px">'
        f'<div style="font-size:13px;color:#6B7280;margin-bottom:14px;line-height:1.6">{g["bio"]}</div>'
        '<div class="info-cols">'
        f'<div class="info-col"><div style="font-size:11px;color:#6B7280">🌐 Languages</div><div style="font-weight:700;font-size:13px">{g["lang"]}</div></div>'
        f'<div class="info-col"><div style="font-size:11px;color:#6B7280">💰 Day Rate</div><div style="font-weight:700;font-size:13px">{g["rate"]}</div></div>'
        f'<div class="info-col"><div style="font-size:11px;color:#6B7280">📅 Availability</div><div style="font-weight:700;font-size:13px">{g["avail"]}</div></div>'
        '</div>'
        '<div style="margin-bottom:14px">'
        '<div style="font-weight:700;font-size:13px;color:#0038A8;margin-bottom:8px">Tour Packages:</div>'
        f'{pkg_items}'
        '</div>'
        '<div style="display:flex;gap:10px">'
        f'<button class="btn" style="background:#CE1126;color:#fff" onclick="openBookingModal(\'{name}\')">📅 Book This Guide</button>'
        f'<button class="btn-outline" style="color:#0038A8;border-color:#0038A8" onclick="showToast(\'Viewing profile: {name}\')">👤 View Profile</button>'
        '</div></div></div>'
    )

def render(filter_city="All", filter_lang="All"):
    cities    = ["All"] + sorted(set(g["city"] for g in GUIDES))
    city_opts = "".join(f'<option {"selected" if c == filter_city else ""}>{c}</option>' for c in cities)
    lang_opts = "".join(f'<option {"selected" if l == filter_lang else ""}>{l}</option>'
                        for l in ["All","EN","FIL","ES","ZH","IL"])
    filtered  = [g for g in GUIDES
                 if (filter_city == "All" or g["city"] == filter_city)
                 and (filter_lang == "All" or filter_lang in g["lang"])]

    if filtered:
        guide_html = "".join(_guide_card(g, i) for i, g in enumerate(filtered))
        count_text = f'{len(filtered)} guide(s) available'
    else:
        guide_html = """
        <div class="guide-empty">
          <div style="font-size:48px;margin-bottom:12px">🧭</div>
          <div style="font-weight:700;font-size:18px;margin-bottom:8px;color:#374151">No Tour Guides Available Yet</div>
          <div style="font-size:14px;color:#9CA3AF;max-width:340px;margin:0 auto;line-height:1.7">
            We are currently onboarding verified local guides.<br>
            Check back soon or try a different city filter.
          </div>
        </div>"""
        count_text = "0 guides found"

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">🧭 Tour Guide Booking</div>
        <div class="section-sub">Book a verified local guide for your Luzon trip</div>
      </div>
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#6B21A8"><span>Search Guides</span></div>
        <div class="card-body">
          <form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">
            <div><label class="lbl">City / Province</label>
              <select class="inp" name="city" style="width:180px">{city_opts}</select></div>
            <div><label class="lbl">Language</label>
              <select class="inp" name="lang" style="width:140px">{lang_opts}</select></div>
            <button class="btn" style="background:#6B21A8;color:#fff" type="submit">Find Guides</button>
          </form>
        </div>
      </div>
      <div style="font-size:13px;color:#6B7280;margin-bottom:14px">{count_text}</div>
      {guide_html}
    </div>"""

    return build_shell("Tour Guides", body, "guides")

if __name__ == "__main__":
    print(render())
