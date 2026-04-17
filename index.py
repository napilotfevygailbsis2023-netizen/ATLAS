import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tourist_ui import build_shell

HIGHLIGHTS = [
    {
        "name": "Intramuros", "city": "Manila", "color": "#0038A8", "cat": "Historical", "icon": "HIST",
        "rating": 4.7,
        "images": [
            "https://commons.wikimedia.org/wiki/Special:FilePath/Intramuros,_The_Walled_City.jpg?width=800",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Fort_Santiago_Gate.jpg?width=800",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Manila_Cathedral_facade.jpg?width=800",
        ],
        "desc": "The Walled City of Manila — a 16th-century Spanish fortress packed with heritage houses, Fort Santiago, and Manila Cathedral. A must-see slice of Philippine colonial history.",
    },
    {
        "name": "Paoay Church", "city": "Ilocos Norte", "color": "#7C3A00", "cat": "Heritage", "icon": "CHURCH",
        "rating": 4.9,
        "images": [
            "https://commons.wikimedia.org/wiki/Special:FilePath/Paoay_Church_2.jpg?width=800",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Paoay_Church_of_Ilocos_Norte,_Philippines.JPG?width=800",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Paoay_church_buttress.jpg?width=800",
        ],
        "desc": "A UNESCO World Heritage baroque church built in 1704 with massive coral-stone buttresses. One of the most photogenic and historically significant churches in Asia.",
    },
    {
        "name": "Taal Volcano", "city": "Batangas", "color": "#065F46", "cat": "Nature", "icon": "VOLCANO",
        "rating": 4.6,
        "images": [
            "https://commons.wikimedia.org/wiki/Special:FilePath/Taal_Volcano_Island.jpg?width=800",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Taal_Lake_and_Taal_Volcano_Island_from_Tagaytay.jpg?width=800",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Taal_volcano_2020_eruption.jpg?width=800",
        ],
        "desc": "A volcano within a lake within a volcano — one of the world's most unique geological wonders. Breathtaking views from the Tagaytay ridge make this Luzon's top natural landmark.",
    },
    {
        "name": "Calle Crisologo", "city": "Vigan", "color": "#7C2D12", "cat": "Heritage", "icon": "HERITAGE",
        "rating": 4.8,
        "images": [
            "https://commons.wikimedia.org/wiki/Special:FilePath/Calle_Crisologo_Vigan.jpg?width=800",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Vigan_Calle_Crisologo_2.jpg?width=800",
            "https://commons.wikimedia.org/wiki/Special:FilePath/Kalesa_Vigan.jpg?width=800",
        ],
        "desc": "A cobblestone street lined with 16th-century Spanish colonial mansions preserved in near-original condition. Kalesa rides and heritage shops make it the heart of UNESCO-listed Vigan.",
    },
]
OFFERS = [
    {"title":"Book a Tour Guide",  "desc":"Get a certified local guide for your Luzon trip",     "color":"#0038A8","href":"/guides.py",  "icon":"COMPASS"},
    {"title":"Check Live Weather", "desc":"Plan safely with real-time forecasts for each city",  "color":"#0038A8","href":"/weather.py", "icon":"SUN"},
    {"title":"Search Flights",     "desc":"Find the best domestic fares to Luzon destinations",  "color":"#0038A8","href":"/flights.py", "icon":"PLANE"},
]

DEST_ICONS = {'HIST':'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="22" x2="21" y2="22"/><line x1="6" y1="18" x2="6" y2="11"/><line x1="10" y1="18" x2="10" y2="11"/><line x1="14" y1="18" x2="14" y2="11"/><line x1="18" y1="18" x2="18" y2="11"/><polygon points="12 2 20 7 4 7"/></svg>','CHURCH':'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 22V10l-6-8-6 8v12"/><path d="M12 2v4"/><path d="M10 4h4"/><path d="M9 22v-6h6v6"/></svg>','VOLCANO':'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 9l5-7 5 7"/><path d="M2 22l5-7h10l5 7z"/><path d="M12 2v7"/></svg>','HERITAGE':'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="10" r="3"/><path d="M12 21.7C17.3 17 20 13 20 10a8 8 0 1 0-16 0c0 3 2.7 6.9 8 11.7z"/></svg>'}
def render(user=None):
    def _stars(r):
        full  = int(r)
        half  = 1 if (r - full) >= 0.5 else 0
        empty = 5 - full - half
        return ('<span style="color:#F59E0B">&#9733;</span>' * full +
                '<span style="color:#F59E0B">&#189;</span>' * half +
                '<span style="color:#D1D5DB">&#9733;</span>' * empty)

    import json as _json
    def _imgs_js(imgs):
        return _json.dumps(imgs)

    dest_cards = "".join(f"""
    <div class="dest-card" onclick="location.href='/attractions.py?city={h['city']}'">
      <div class="dest-card-img" style="position:relative;overflow:hidden;height:170px;border-radius:12px 12px 0 0;background:{h['color']}">
        <div class="img-slider" id="slider-{h['name'].replace(' ','-')}" style="position:absolute;inset:0">
          {''.join(f'''<img src="{img}" referrerpolicy="no-referrer"
               style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1s ease;animation:kenburns 8s ease-in-out infinite alternate"
               onerror="this.style.display='none'"/>''' for i,img in enumerate(h['images']))}
        </div>
        <div style="position:absolute;inset:0;background:linear-gradient(to bottom,transparent 40%,rgba(0,0,0,.45) 100%);z-index:2;pointer-events:none"></div>
        <div style="position:absolute;top:10px;right:10px;background:rgba(0,0,0,.55);z-index:3;
                    color:#F59E0B;font-size:12px;font-weight:700;padding:3px 8px;
                    border-radius:20px;display:flex;align-items:center;gap:4px">
          &#9733; {h['rating']}
        </div>
        <div style="position:absolute;bottom:8px;left:10px;z-index:3;display:flex;gap:4px">
          {''.join(f'<div class="img-dot" id="dot-{h["name"].replace(" ","-")}-{i}" style="width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,{0.9 if i==0 else 0.4});transition:background .3s"></div>' for i in range(len(h['images'])))}
        </div>
      </div>
      <div class="dest-card-body">
        <div style="font-weight:700;font-size:14px;margin-bottom:2px">{h['name']}</div>
        <div style="font-size:11px;color:#6B7280;margin-bottom:6px">{h['city']} &middot; {h['cat']}</div>
        <div style="font-size:11px;color:#374151;line-height:1.55;margin-bottom:10px;
                    display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden">
          {h['desc']}
        </div>
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
    <div class="hero" style="position:relative;overflow:hidden">
      <!-- Animated background slideshow -->
      <div id="hero-slides" style="position:absolute;inset:0;z-index:0">
        <img referrerpolicy="no-referrer" src="https://commons.wikimedia.org/wiki/Special:FilePath/Intramuros,_The_Walled_City.jpg?width=1200"
             style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:1;transition:opacity 1.5s ease;animation:heroKB 12s ease-in-out infinite alternate" onerror="this.style.display='none'"/>
        <img referrerpolicy="no-referrer" src="https://commons.wikimedia.org/wiki/Special:FilePath/Taal_Lake_and_Taal_Volcano_Island_from_Tagaytay.jpg?width=1200"
             style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1.5s ease;animation:heroKB2 12s ease-in-out infinite alternate" onerror="this.style.display='none'"/>
        <img referrerpolicy="no-referrer" src="https://commons.wikimedia.org/wiki/Special:FilePath/Paoay_Church_2.jpg?width=1200"
             style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1.5s ease;animation:heroKB 12s ease-in-out infinite alternate" onerror="this.style.display='none'"/>
        <img referrerpolicy="no-referrer" src="https://commons.wikimedia.org/wiki/Special:FilePath/Calle_Crisologo_Vigan.jpg?width=1200"
             style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1.5s ease;animation:heroKB2 12s ease-in-out infinite alternate" onerror="this.style.display='none'"/>
        <img referrerpolicy="no-referrer" src="https://commons.wikimedia.org/wiki/Special:FilePath/Mayon_Volcano.jpg?width=1200"
             style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1.5s ease;animation:heroKB 12s ease-in-out infinite alternate" onerror="this.style.display='none'"/>
      </div>
      <!-- Dark overlay so text stays readable -->
      <div style="position:absolute;inset:0;z-index:1;background:linear-gradient(to right, rgba(0,0,0,.62) 0%, rgba(0,0,0,.35) 60%, rgba(0,0,0,.15) 100%)"></div>
      <!-- Hero content -->
      <div style="position:relative;z-index:2">
        <div class="hero-dots">
          <div class="hero-dot" style="background:#0038A8"></div>
          <div class="hero-dot" style="background:#CE1126"></div>
          <div class="hero-dot" style="background:#FCD116"></div>
        </div>
        <h1 style="color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.4)">Discover the <span style="color:#93C5FD">Beauty</span> of <span style="color:#FCA5A5">Luzon</span>, Philippines</h1>
        <p class="hero-sub" style="color:rgba(255,255,255,.9);text-shadow:0 1px 6px rgba(0,0,0,.4)">Your all-in-one travel companion for flights, weather, attractions, tour guides and more.</p>
        <div class="search-box">
          <span style="padding:0 10px 0 16px;display:flex;align-items:center"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></span>
          <input id="hero-search" placeholder="Search destinations, attractions, restaurants..."/>
          <button onclick="doSearch()">Search</button>
        </div>
        <!-- Slide indicator dots -->
        <div style="margin-top:18px;display:flex;gap:6px">
          <div class="hero-ind" id="hind-0" style="width:28px;height:4px;border-radius:2px;background:#fff;transition:all .3s;cursor:pointer" onclick="heroGoTo(0)"></div>
          <div class="hero-ind" id="hind-1" style="width:10px;height:4px;border-radius:2px;background:rgba(255,255,255,.45);transition:all .3s;cursor:pointer" onclick="heroGoTo(1)"></div>
          <div class="hero-ind" id="hind-2" style="width:10px;height:4px;border-radius:2px;background:rgba(255,255,255,.45);transition:all .3s;cursor:pointer" onclick="heroGoTo(2)"></div>
          <div class="hero-ind" id="hind-3" style="width:10px;height:4px;border-radius:2px;background:rgba(255,255,255,.45);transition:all .3s;cursor:pointer" onclick="heroGoTo(3)"></div>
          <div class="hero-ind" id="hind-4" style="width:10px;height:4px;border-radius:2px;background:rgba(255,255,255,.45);transition:all .3s;cursor:pointer" onclick="heroGoTo(4)"></div>
        </div>
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

    // ── Hero background slideshow ─────────────────────────────────────────────
    (function() {{
      var slides = document.querySelectorAll('#hero-slides img');
      var total  = slides.length;
      var cur    = 0;
      function heroGoTo(n) {{
        slides[cur].style.opacity = '0';
        document.getElementById('hind-' + cur).style.width  = '10px';
        document.getElementById('hind-' + cur).style.background = 'rgba(255,255,255,.45)';
        cur = (n + total) % total;
        slides[cur].style.opacity = '1';
        document.getElementById('hind-' + cur).style.width  = '28px';
        document.getElementById('hind-' + cur).style.background = '#fff';
      }}
      window.heroGoTo = heroGoTo;
      setInterval(function(){{ heroGoTo(cur + 1); }}, 5000);
    }})();
    (function() {{
      document.querySelectorAll('.img-slider').forEach(function(slider) {{
        var imgs = slider.querySelectorAll('img');
        if (!imgs.length) return;
        var idx = 0;
        // show first image immediately
        imgs[0].style.opacity = '1';
        var id = slider.id; // e.g. "slider-Intramuros"
        var baseName = id.replace('slider-', '');
        function showNext() {{
          imgs[idx].style.opacity = '0';
          var dotOld = document.getElementById('dot-' + baseName + '-' + idx);
          if (dotOld) dotOld.style.background = 'rgba(255,255,255,0.4)';
          idx = (idx + 1) % imgs.length;
          imgs[idx].style.opacity = '1';
          var dotNew = document.getElementById('dot-' + baseName + '-' + idx);
          if (dotNew) dotNew.style.background = 'rgba(255,255,255,0.9)';
        }}
        setInterval(showNext, 3000);
      }});
    }})();
    </script>
    <style>
    @keyframes kenburns {{
      0%   {{ transform: scale(1)    translate(0, 0); }}
      50%  {{ transform: scale(1.08) translate(-1%, -1%); }}
      100% {{ transform: scale(1.04) translate(1%, 0.5%); }}
    }}
    @keyframes heroKB {{
      0%   {{ transform: scale(1)    translate(0, 0); }}
      100% {{ transform: scale(1.12) translate(-2%, -1%); }}
    }}
    @keyframes heroKB2 {{
      0%   {{ transform: scale(1.08) translate(1%, 0); }}
      100% {{ transform: scale(1)    translate(-1%, 1%); }}
    }}
    .img-slider img {{ animation: kenburns 8s ease-in-out infinite alternate; }}
    </style>"""
    return build_shell("Home", body, "home", user=user)