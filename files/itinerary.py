#!/usr/bin/env python3
# ── ATLAS ITINERARY PAGE ──────────────────────────────────────────────────────
# itinerary.py — Automated itinerary generation and trip planner

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from template import build_shell
from data import ITINERARIES

def render(destination: str = "Manila"):
    if destination not in ITINERARIES:
        destination = "Manila"
    itin = ITINERARIES[destination]

    dest_opts = "".join(
        f'<option {"selected" if k == destination else ""}>{k}</option>'
        for k in ITINERARIES
    )

    day_cards = "".join(f"""
    <div class="day-card">
      <div class="day-hdr" style="background:{d['color']}">{d['day']}</div>
      {"".join(f'''
      <div class="act-row">
        <span style="color:{d['color']};font-weight:700;font-size:13px;width:60px;flex-shrink:0">{t}</span>
        <span style="font-size:14px;color:#374151">{act}</span>
      </div>''' for t, act in d['acts'])}
    </div>""" for d in itin)

    total_acts = sum(len(d["acts"]) for d in itin)

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">📅 Itinerary Planner</div>
        <div class="section-sub">Automated Itinerary Generation and Travel Planning System</div>
      </div>
      <div class="card" style="margin-bottom:24px">
        <div class="card-hdr" style="background:#065F46"><span>⚙️ Trip Configuration</span></div>
        <div class="card-body">
          <form method="get">
            <div class="form-row">
              <div><label class="lbl">Destination</label>
                <select class="inp" name="dest">{dest_opts}</select></div>
              <div><label class="lbl">Start Date</label>
                <input class="inp" type="date" value="2026-03-20"/></div>
              <div><label class="lbl">Trip Duration</label>
                <select class="inp"><option>2 days</option><option selected>3 days</option><option>5 days</option></select></div>
              <div><label class="lbl">Budget (PHP)</label>
                <input class="inp" value="15,000"/></div>
              <div><label class="lbl">Travel Style</label>
                <select class="inp"><option>Leisure</option><option>Adventure</option><option>Heritage</option><option>Family</option></select></div>
              <div><label class="lbl">No. of Travelers</label>
                <select class="inp"><option>1</option><option selected>2</option><option>3–5</option><option>6+</option></select></div>
            </div>
            <div style="display:flex;gap:10px">
              <button class="btn" style="background:#065F46;color:#fff" type="submit">📅 Generate Itinerary</button>
              <button class="btn" style="background:#CE1126;color:#fff" type="button"
                onclick="showToast('Itinerary saved! ✓')">💾 Save Itinerary</button>
            </div>
          </form>
        </div>
      </div>
      {day_cards}
      <div class="summary-bar">
        <div class="summary-item">
          <div style="font-weight:800;color:#FCD116;font-size:15px">{total_acts} Activities</div>
          <div style="font-size:12px;color:#BFCFEE">Total Stops</div>
        </div>
        <div class="summary-item">
          <div style="font-weight:800;color:#FCD116;font-size:15px">{len(itin)} Days</div>
          <div style="font-size:12px;color:#BFCFEE">Duration</div>
        </div>
        <div class="summary-item">
          <div style="font-weight:800;color:#FCD116;font-size:15px">₱15,000</div>
          <div style="font-size:12px;color:#BFCFEE">Budget</div>
        </div>
        <div class="summary-item">
          <div style="font-weight:800;color:#FCD116;font-size:15px">{destination}</div>
          <div style="font-size:12px;color:#BFCFEE">Destination</div>
        </div>
      </div>
    </div>"""

    return build_shell("Itinerary", body)


if __name__ == "__main__":
    dest = sys.argv[1] if len(sys.argv) > 1 else "Manila"
    print(render(dest))
