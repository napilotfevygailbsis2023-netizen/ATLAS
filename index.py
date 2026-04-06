import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tourist_ui import build_shell

HIGHLIGHTS = [
    {"name":"Intramuros",      "city":"Manila",       "color":"#0038A8","cat":"Historical","icon":"HIST"},
    {"name":"Paoay Church",    "city":"Ilocos Norte", "color":"#0038A8","cat":"Heritage",  "icon":"CHURCH"},
    {"name":"Taal Volcano",    "city":"Batangas",     "color":"#0038A8","cat":"Nature",    "icon":"VOLCANO"},
    {"name":"Calle Crisologo", "city":"Vigan",        "color":"#0038A8","cat":"Heritage",  "icon":"HERITAGE"},
]
OFFERS = [
    {"title":"Book a Tour Guide",  "desc":"Get a certified local guide for your Luzon trip",     "color":"#0038A8","href":"/guides.py",  "icon":"COMPASS"},
    {"title":"Check Live Weather", "desc":"Plan safely with real-time forecasts for each city",  "color":"#0038A8","href":"/weather.py", "icon":"SUN"},
    {"title":"Search Flights",     "desc":"Find the best domestic fares to Luzon destinations",  "color":"#0038A8","href":"/flights.py", "icon":"PLANE"},
]

DEST_ICONS = {'HIST':'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="22" x2="21" y2="22"/><line x1="6" y1="18" x2="6" y2="11"/><line x1="10" y1="18" x2="10" y2="11"/><line x1="14" y1="18" x2="14" y2="11"/><line x1="18" y1="18" x2="18" y2="11"/><polygon points="12 2 20 7 4 7"/></svg>','CHURCH':'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 22V10l-6-8-6 8v12"/><path d="M12 2v4"/><path d="M10 4h4"/><path d="M9 22v-6h6v6"/></svg>','VOLCANO':'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 9l5-7 5 7"/><path d="M2 22l5-7h10l5 7z"/><path d="M12 2v7"/></svg>','HERITAGE':'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="10" r="3"/><path d="M12 21.7C17.3 17 20 13 20 10a8 8 0 1 0-16 0c0 3 2.7 6.9 8 11.7z"/></svg>'}
def render(user=None):
    dest_cards = "".join(f"""
    <div class="dest-card" onclick="location.href='/attractions.py?city={h['city']}'">
      <div class="dest-card-img" style="background:linear-gradient(135deg,{h['color']},{h['color']}88)">
        {DEST_ICONS[h['icon']]}
      </div>
      <div class="dest-card-body">
        <div style="font-weight:700;font-size:14px;margin-bottom:3px">{h['name']}</div>
        <div style="font-size:12px;color:#6B7280;margin-bottom:10px">{h['city']} - {h['cat']}</div>
        <button class="btn" style="background:#0038A8;color:#fff;padding:6px 14px;font-size:12px"
          onclick="event.stopPropagation();location.href='/attractions.py?city={h['city']}'">Explore</button>
      </div>
    </div>""" for h in HIGHLIGHTS)

    OFFER_ICONS = {'COMPASS':'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>','SUN':'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>','PLANE':'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13"/><path d="M22 2L15 22 11 13 2 9l20-7z"/></svg>'}
    offer_cards = "".join(f"""
    <div class="offer-card" style="background:#0038A8;border-radius:16px;cursor:pointer"
         onclick="location.href='{o['href']}'">
      <div style="margin-bottom:14px">{OFFER_ICONS[o['icon']]}</div>
      <div style="font-weight:800;font-size:16px;margin-bottom:6px;color:#fff">{o['title']}</div>
      <div style="font-size:13px;opacity:.85;line-height:1.6;color:#fff">{o['desc']}</div>
    </div>""" for o in OFFERS)

    body = f"""
    <div class="hero">
      <div class="hero-bg"></div>
      <div class="hero-dots">
        <div class="hero-dot" style="background:#0038A8"></div>
        <div class="hero-dot" style="background:#CE1126"></div>
        <div class="hero-dot" style="background:#FCD116"></div>
      </div>
      <h1>Discover the <span class="blue">Beauty</span> of <span class="red">Luzon</span>, Philippines</h1>
      <p class="hero-sub">Your all-in-one travel companion for flights, weather, attractions, tour guides and more.</p>
      <div class="search-box">
        <span style="padding:0 10px 0 16px;display:flex;align-items:center"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></span>
        <input id="hero-search" placeholder="Search destinations, attractions, restaurants..."/>
        <button onclick="doSearch()">Search</button>
      </div>
    </div>
    <div class="page-wrap">
      <div style="margin-bottom:16px">
        <div class="section-title">Top Luzon Destinations</div>
        <div class="section-sub">Hand-picked spots for your next adventure</div>
      </div>
      <!-- CAROUSEL -->
      <div style="position:relative;margin-bottom:36px" id="carousel-wrap">
        <div style="overflow:hidden" id="carousel-outer">
          <div id="carousel-track" style="display:flex;transition:transform .4s ease;gap:20px">
            {dest_cards}
          </div>
        </div>
        <button onclick="carouselMove(-1)" style="position:absolute;top:45%;left:-18px;transform:translateY(-50%);background:rgba(0,0,0,.5);color:#fff;border:none;border-radius:50%;width:38px;height:38px;font-size:20px;cursor:pointer;z-index:10">&#8249;</button>
        <button onclick="carouselMove(1)"  style="position:absolute;top:45%;right:-18px;transform:translateY(-50%);background:rgba(0,0,0,.5);color:#fff;border:none;border-radius:50%;width:38px;height:38px;font-size:20px;cursor:pointer;z-index:10">&#8250;</button>
        <div id="carousel-dots" style="text-align:center;margin-top:12px;display:flex;justify-content:center;gap:6px"></div>
      </div>
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
    // Carousel
    var _ci = 0;
    var _cards = document.querySelectorAll('#carousel-track .dest-card');
    var _total = _cards.length;
    var _dotsEl = document.getElementById('carousel-dots');
    var _vis = 4; // always show 4

    function _setCardWidths() {{
      var outer = document.getElementById('carousel-outer');
      var gap = 20;
      var totalGaps = (_vis - 1) * gap;
      var cardW = (outer.offsetWidth - totalGaps) / _vis;
      _cards.forEach(function(c) {{
        c.style.minWidth = cardW + 'px';
        c.style.width = cardW + 'px';
        c.style.flexShrink = '0';
      }});
      return cardW;
    }}
    function _buildDots() {{
      _dotsEl.innerHTML = '';
      var pages = Math.ceil(_total / _vis);
      for (var i = 0; i < pages; i++) {{
        var d = document.createElement('button');
        d.style.cssText = 'width:10px;height:10px;border-radius:50%;border:none;cursor:pointer;background:' + (_ci === i ? '#CE1126' : '#D1D5DB');
        (function(idx){{ d.onclick = function(){{ _ci = idx; _move(); }}; }})(i);
        _dotsEl.appendChild(d);
      }}
    }}
    function _move() {{
      var pages = Math.ceil(_total / _vis);
      _ci = Math.max(0, Math.min(_ci, pages - 1));
      var cardW = _setCardWidths();
      var step = _vis * (cardW + 20);
      document.getElementById('carousel-track').style.transform = 'translateX(-' + (_ci * step) + 'px)';
      _buildDots();
    }}
    function carouselMove(dir) {{
      var pages = Math.ceil(_total / _vis);
      _ci = (_ci + dir + pages) % pages;
      _move();
    }}
    _setCardWidths();
    _buildDots();
    window.addEventListener('resize', function(){{ _move(); }});
    // Auto-play every 4s
    setInterval(function(){{ carouselMove(1); }}, 4000);
    </script>"""
    return build_shell("Home", body, "home", user=user)