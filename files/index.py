#!/usr/bin/env python3
# ── FILE: index.py ────────────────────────────────────────────────────────────
# CHANGES: "Discover the Beauty of Luzon" hero is directly below navbar/tiles.
#          Removed API credits from subtitle.
#          All buttons working.

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell

HIGHLIGHTS = [
    {"name":"Intramuros",     "city":"Manila",       "color":"#0038A8","cat":"Historical","icon":"🏛️"},
    {"name":"Paoay Church",   "city":"Ilocos Norte", "color":"#C8930A","cat":"Heritage",  "icon":"⛪"},
    {"name":"Taal Volcano",   "city":"Batangas",     "color":"#065F46","cat":"Nature",    "icon":"🌋"},
    {"name":"Calle Crisologo","city":"Vigan",        "color":"#CE1126","cat":"Heritage",  "icon":"🏘️"},
]

OFFERS = [
    {"title":"Book a Tour Guide",    "desc":"Get a certified local guide for your Luzon trip",      "color":"#0038A8","href":"/guides.py",   "icon":"🧭"},
    {"title":"Check Live Weather",   "desc":"Plan safely with real-time forecasts for each city",   "color":"#CE1126","href":"/weather.py",  "icon":"🌤️"},
    {"title":"Search Flights",       "desc":"Find the best domestic fares to Luzon destinations",   "color":"#C8930A","href":"/flights.py",  "icon":"✈️"},
]

def render():
    dest_cards = "".join(f"""
    <div class="dest-card" onclick="location.href='/attractions.py?city={h['city']}'">
      <div class="dest-card-img" style="background:linear-gradient(135deg,{h['color']},{h['color']}88)">
        <span style="font-size:36px">{h['icon']}</span>
      </div>
      <div class="dest-card-body">
        <div style="font-weight:700;font-size:14px;margin-bottom:3px">{h['name']}</div>
        <div style="font-size:12px;color:#6B7280;margin-bottom:10px">{h['city']} · {h['cat']}</div>
        <button class="btn" style="background:{h['color']};color:#fff;padding:6px 14px;font-size:12px"
          onclick="event.stopPropagation();location.href='/attractions.py?city={h['city']}'">Explore →</button>
      </div>
    </div>""" for h in HIGHLIGHTS)

    offer_cards = "".join(f"""
    <div class="offer-card" style="background:linear-gradient(135deg,{o['color']},{o['color']}CC)"
         onclick="location.href='{o['href']}'">
      <div style="font-size:34px;margin-bottom:10px">{o['icon']}</div>
      <div style="font-weight:800;font-size:16px;margin-bottom:6px">{o['title']}</div>
      <div style="font-size:13px;opacity:.85;line-height:1.6">{o['desc']}</div>
    </div>""" for o in OFFERS)

    body = f"""
    <!-- HERO — directly below navbar tiles -->
    <div class="hero">
      <div class="hero-bg"></div>
      <div class="hero-dots">
        <div class="hero-dot" style="background:#0038A8"></div>
        <div class="hero-dot" style="background:#CE1126"></div>
        <div class="hero-dot" style="background:#FCD116"></div>
      </div>
      <h1>Discover the <span class="blue">Beauty</span> of <span class="red">Luzon</span>,<br>Philippines</h1>
      <p class="hero-sub">Your all-in-one travel companion — flights, weather, attractions, tour guides and more.</p>
      <div class="search-box">
        <span style="padding:0 10px 0 16px;display:flex;align-items:center;font-size:18px">🔍</span>
        <input id="hero-search" placeholder="Search destinations, attractions, restaurants..."/>
        <button onclick="doSearch()">Search</button>
      </div>
    </div>

    <div class="page-wrap">
      <div style="margin-bottom:8px">
        <div class="section-title">Top Luzon Destinations</div>
        <div class="section-sub">Hand-picked spots for your next adventure</div>
      </div>
      <div class="dest-grid">{dest_cards}</div>

      <div style="margin-bottom:8px">
        <div class="section-title">Plan Your Trip</div>
        <div class="section-sub">Everything you need in one place</div>
      </div>
      <div class="offer-grid">{offer_cards}</div>
    </div>

    <script>
    function doSearch() {{
      var q = document.getElementById('hero-search').value.trim();
      if (q) location.href = '/attractions.py?kw=' + encodeURIComponent(q);
      else showToast('Please enter a search term');
    }}
    document.getElementById('hero-search').addEventListener('keydown', function(e) {{
      if (e.key === 'Enter') doSearch();
    }});
    </script>"""

    return build_shell("Home", body, "home")

if __name__ == "__main__":
    print(render())
