import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tourist_ui import build_shell
import admin_db

COLORS = {
    "Bus":     "#0038A8",
    "Van":     "#7C3AED",
    "Ferry":   "#0891B2",
    "Train":   "#059669",
    "Jeepney": "#D97706",
}
ICONS = {
    "Bus":     '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="13" rx="2"/><path d="M3 11h18"/><path d="M8 5V3"/><path d="M16 5V3"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/><path d="M5 18H3v-3"/><path d="M19 18h2v-3"/></svg>',
    "Van":     '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 17H3a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v9a2 2 0 0 1-2 2h-3"/><circle cx="7.5" cy="17.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>',
    "Ferry":   '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20c0 1 1 1 2 1s2 0 2-1 1-1 2-1 2 0 2 1 1 1 2 1 2 0 2-1 1-1 2-1 2 0 2 1"/><path d="M4 15h16l-3-8H7z"/><path d="M12 7V3"/><path d="M10 3h4"/></svg>',
    "Train":   '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="14" rx="2"/><path d="M4 11h16"/><path d="M8 3v8"/><circle cx="8.5" cy="19.5" r="2.5"/><circle cx="15.5" cy="19.5" r="2.5"/><path d="M6.5 22l2-2.5"/><path d="M17.5 22l-2-2.5"/></svg>',
    "Jeepney": '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 9l2-2h18l2 2v5H1z"/><path d="M4 14v3"/><path d="M20 14v3"/><circle cx="6" cy="17" r="2"/><circle cx="18" cy="17" r="2"/><path d="M8 9V7h8v2"/></svg>',
}

def _card(t):
    col  = COLORS.get(t["type"], "#374151")
    icon = ICONS.get(t["type"], "&#128663;")
    fare = str(t.get("fare", "—"))
    # Store data in attributes — no inline JS args (avoids quote/brace escaping issues)
    origin = t.get("origin", "").replace('"', "&quot;")
    dest   = t.get("dest",   "").replace('"', "&quot;")
    route  = t.get("route",  "").replace('"', "&quot;")
    ttype  = t.get("type",   "").replace('"', "&quot;")
    fare_a = fare.replace('"', "&quot;")
    return (
        f'<div class="grid-card atlas-route-card" style="cursor:pointer"'
        f' data-origin="{origin}" data-dest="{dest}" data-route="{route}"'
        f' data-type="{ttype}" data-fare="{fare_a}">'
        f'<div class="grid-card-top" style="background:linear-gradient(135deg,{col},{col}99)">'
        f'<div style="margin-bottom:10px">{icon}</div>'
        f'<div style="font-weight:800;font-size:15px;color:#fff;margin-bottom:4px">{t["route"]}</div>'
        f'<span class="badge" style="background:rgba(255,255,255,.2);color:#fff">{t["type"]}</span>'
        f'</div>'
        f'<div class="grid-card-body">'
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px">'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">From</div>'
        f'<div style="font-weight:700;font-size:12px">{t.get("origin","—")}</div></div>'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">To</div>'
        f'<div style="font-weight:700;font-size:12px">{t.get("dest","—")}</div></div>'
        f'<div class="info-stat"><div style="font-size:10px;color:#9CA3AF">Fare</div>'
        f'<div style="font-weight:700;font-size:12px;color:#CE1126">{fare}</div></div>'
        f'</div>'
        f'<button class="btn" style="background:{col};color:#fff;width:100%;padding:9px">'
        f'View Route Map &#128506;</button>'
        f'</div></div>'
    )

def render(filter_type="All", filter_from="All", search="", user=None):
    try:
        all_items = admin_db.get_transport()
        items = [t for t in all_items if (t.get("status") or "active") == "active"]
    except Exception:
        items = []

    filtered = [t for t in items
        if (filter_type == "All" or t.get("type") == filter_type)
        and (filter_from == "All" or filter_from.lower() in (t.get("origin","") + " " + t.get("dest","")).lower())
        and (not search or search.lower() in t.get("route","").lower()
             or search.lower() in t.get("origin","").lower()
             or search.lower() in t.get("dest","").lower())]

    all_origins = sorted(set(t.get("origin","") for t in items if t.get("origin")))
    origin_opts = '<option value="All">All</option>' + "".join(
        f'<option value="{o}" {"selected" if o==filter_from else ""}>{o}</option>'
        for o in all_origins
    )
    type_opts = "".join(
        f'<option {"selected" if x==filter_type else ""}>{x}</option>'
        for x in ["All","Bus","Van","Ferry","Train","Jeepney"]
    )

    cards = "".join(_card(t) for t in filtered)
    empty = (
        '<div class="guide-empty">'
        '<div style="font-size:40px;margin-bottom:10px">&#128652;</div>'
        '<div style="font-weight:700;font-size:16px">No routes found</div>'
        '</div>'
    ) if not filtered else ""

    # Build the dynamic top section with f-strings
    top_html = (
        '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>'
        '<div class="page-wrap">'
        '<div style="margin-bottom:22px">'
        '<div class="section-title">Transportation</div>'
        '<div class="section-sub">Ground, sea and rail transport routes across Luzon &mdash; click a card to view the route map</div>'
        '</div>'
        '<div class="card" style="margin-bottom:20px">'
        '<div class="card-hdr" style="background:#0038A8"><span>Search &amp; Filter Routes</span></div>'
        '<div class="card-body">'
        '<form method="get" style="display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end">'
        '<div style="flex:1;min-width:200px"><label class="lbl">Search Routes</label>'
        f'<input class="inp" name="search" placeholder="e.g. Manila, Baguio..." value="{search}"/></div>'
        f'<div><label class="lbl">Transport Type</label><select class="inp" name="type" style="width:150px">{type_opts}</select></div>'
        f'<div><label class="lbl">Departure From</label><select class="inp" name="from" style="width:180px">{origin_opts}</select></div>'
        '<button class="btn" style="background:#0038A8;color:#fff" type="submit">Search</button>'
        '</form>'
        '</div></div>'
        f'<div style="font-size:13px;color:#6B7280;margin-bottom:16px">{len(filtered)} route(s) found</div>'
        f'<div class="page-grid3">{cards}</div>{empty}'
        '</div>'
    )

    # Modal HTML — plain string, no .format(), no f-string (no {} conflicts)
    modal_html = (
        '<div id="atlas-route-modal" style="display:none;position:fixed;top:0;left:0;right:0;bottom:0;'
        'background:rgba(0,0,0,.55);z-index:99998;align-items:center;justify-content:center">'
        '<div style="background:#fff;border-radius:16px;width:900px;max-width:96vw;max-height:90vh;'
        'overflow:hidden;box-shadow:0 24px 64px rgba(0,0,0,.3);display:flex;flex-direction:column">'
        '<div id="atlas-modal-header" style="padding:18px 24px;display:flex;justify-content:space-between;'
        'align-items:center;flex-shrink:0;background:#0038A8">'
        '<div>'
        '<div id="atlas-modal-title" style="font-weight:800;font-size:16px;color:#fff"></div>'
        '<div id="atlas-modal-subtitle" style="font-size:12px;color:rgba(255,255,255,0.8);margin-top:2px"></div>'
        '</div>'
        '<button id="atlas-modal-close" style="background:rgba(255,255,255,.2);border:none;border-radius:50%;'
        'width:32px;height:32px;font-size:18px;cursor:pointer;color:#fff">&#10005;</button>'
        '</div>'
        '<div style="display:grid;grid-template-columns:260px 1fr;flex:1;min-height:0">'
        '<div style="padding:20px;border-right:1px solid #E2E8F0;overflow-y:auto;background:#F8FAFC">'
        '<div style="font-size:11px;font-weight:700;color:#9CA3AF;text-transform:uppercase;margin-bottom:12px">Route Details</div>'
        '<div style="margin-bottom:10px">'
        '<div style="font-size:10px;color:#9CA3AF;margin-bottom:2px">FROM</div>'
        '<div id="atlas-modal-origin" style="font-weight:700;font-size:14px;color:#1E293B"></div>'
        '</div>'
        '<div style="border-left:3px solid #0038A8;margin-left:6px;height:18px;margin-bottom:10px"></div>'
        '<div style="margin-bottom:18px">'
        '<div style="font-size:10px;color:#9CA3AF;margin-bottom:2px">TO</div>'
        '<div id="atlas-modal-dest" style="font-weight:700;font-size:14px;color:#1E293B"></div>'
        '</div>'
        '<div style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;padding:10px;margin-bottom:14px">'
        '<div style="font-size:10px;color:#9CA3AF">TYPE</div>'
        '<div id="atlas-modal-type" style="font-weight:700;font-size:13px;color:#1E293B;margin-top:2px"></div>'
        '</div>'
        '<div style="background:#FEF2F2;border:1px solid #FECACA;border-radius:8px;padding:12px;margin-bottom:14px">'
        '<div style="font-size:10px;color:#9CA3AF">FARE</div>'
        '<div id="atlas-modal-fare" style="font-weight:800;font-size:18px;color:#CE1126;margin-top:2px"></div>'
        '</div>'
        '<div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;padding:12px;font-size:12px;color:#1D4ED8">'
        '<div style="font-weight:700;margin-bottom:6px">&#128506; Live Route Data</div>'
        '<div id="atlas-ors-loading" style="color:#6B7280">Loading route info...</div>'
        '<div id="atlas-ors-details" style="display:none;line-height:1.8">'
        '<div>&#9201; <span id="atlas-ors-duration"></span></div>'
        '<div>&#128207; <span id="atlas-ors-distance"></span></div>'
        '<div id="atlas-ors-fare-row" style="display:none">&#128176; <span id="atlas-ors-fare-est"></span> (est.)</div>'
        '</div>'
        '<div id="atlas-ors-error" style="display:none;color:#DC2626;font-size:11px"></div>'
        '</div>'
        '</div>'
        '<div id="atlas-route-map" style="height:480px;min-height:480px"></div>'
        '</div></div></div>'
    )

    # JS — plain string, no .format() so {s}/{z}/{x}/{y} are safe
    js_html = (
        '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'
        '<script>'
        '(function() {'
        '  var _map = null, _markers = [], _routeLayer = null;'
        '  var COL = {Bus:"#0038A8",Van:"#7C3AED",Ferry:"#0891B2",Train:"#059669",Jeepney:"#D97706"};'
        '  function openModal(origin, dest, route, type, fare) {'
        '    var col = COL[type] || "#0038A8";'
        '    document.getElementById("atlas-modal-title").textContent    = route;'
        '    document.getElementById("atlas-modal-subtitle").textContent = origin + " \u2192 " + dest;'
        '    document.getElementById("atlas-modal-origin").textContent   = origin;'
        '    document.getElementById("atlas-modal-dest").textContent     = dest;'
        '    document.getElementById("atlas-modal-type").textContent     = type;'
        '    document.getElementById("atlas-modal-fare").textContent     = fare;'
        '    document.getElementById("atlas-modal-header").style.background = col;'
        '    document.getElementById("atlas-ors-loading").style.display  = "block";'
        '    document.getElementById("atlas-ors-details").style.display  = "none";'
        '    document.getElementById("atlas-ors-error").style.display    = "none";'
        '    document.getElementById("atlas-ors-fare-row").style.display = "none";'
        '    document.getElementById("atlas-route-modal").style.display  = "flex";'
        '    fetch("/api/transport/lookup?origin=" + encodeURIComponent(origin) + "&dest=" + encodeURIComponent(dest))'
        '      .then(function(r){ return r.json(); })'
        '      .then(function(d){'
        '        document.getElementById("atlas-ors-loading").style.display = "none";'
        '        if (d.ok) {'
        '          document.getElementById("atlas-ors-duration").textContent = d.duration;'
        '          document.getElementById("atlas-ors-distance").textContent = d.distance;'
        '          if (d.fare) { document.getElementById("atlas-ors-fare-est").textContent = d.fare; document.getElementById("atlas-ors-fare-row").style.display = "block"; }'
        '          document.getElementById("atlas-ors-details").style.display = "block";'
        '        } else {'
        '          document.getElementById("atlas-ors-error").textContent = d.error || "Live route data unavailable";'
        '          document.getElementById("atlas-ors-error").style.display = "block";'
        '        }'
        '      }).catch(function(){ document.getElementById("atlas-ors-loading").style.display="none"; document.getElementById("atlas-ors-error").textContent="Could not reach route service"; document.getElementById("atlas-ors-error").style.display="block"; });'
        '    setTimeout(function() {'
        '      if (!_map) {'
        '        _map = L.map("atlas-route-map").setView([15.5, 121.0], 7);'
        '        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {attribution: "\u00a9 OpenStreetMap contributors", maxZoom: 18}).addTo(_map);'
        '      } else {'
        '        _markers.forEach(function(m){ _map.removeLayer(m); }); _markers = [];'
        '        if (_routeLayer) { _map.removeLayer(_routeLayer); _routeLayer = null; }'
        '      }'
        '      _map.invalidateSize();'
        '      drawRoute(origin, dest, col);'
        '    }, 250);'
        '  }'
        '  function closeModal() { document.getElementById("atlas-route-modal").style.display = "none"; }'
        '  function drawRoute(origin, dest, color) {'
        '    Promise.all([geocode(origin), geocode(dest)])'
        '      .then(function(c) {'
        '        var o = c[0], d = c[1];'
        '        function mkIcon(lbl) { return L.divIcon({html: \'<div style="background:\' + color + \';color:#fff;font-size:10px;font-weight:700;padding:4px 8px;border-radius:12px;white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,0.3)">\' + lbl + \'</div>\', className: "", iconAnchor: [0,10]}); }'
        '        _markers = [L.marker([o.lat,o.lng],{icon:mkIcon(origin)}).addTo(_map), L.marker([d.lat,d.lng],{icon:mkIcon(dest)}).addTo(_map)];'
        '        _routeLayer = L.polyline([[o.lat,o.lng],[d.lat,d.lng]],{color:color,weight:5,opacity:0.85,dashArray:"12,7"}).addTo(_map);'
        '        _map.invalidateSize();'
        '        _map.fitBounds([[o.lat,o.lng],[d.lat,d.lng]],{padding:[60,60]});'
        '      }).catch(function(e){ console.warn("ATLAS geocode:", e); _map.invalidateSize(); _map.setView([15.5,121.0],7); });'
        '  }'
        '  function geocode(place) {'
        '    return fetch("/api/transport/geocode?place=" + encodeURIComponent(place))'
        '      .then(function(r){ return r.json(); })'
        '      .then(function(d){ if (!d || !d.ok) throw new Error("Not found: " + place); return {lat:d.lat,lng:d.lng}; });'
        '  }'
        '  document.addEventListener("click", function(e) {'
        '    var card = e.target.closest(".atlas-route-card");'
        '    if (card) { e.preventDefault(); e.stopPropagation(); openModal(card.dataset.origin, card.dataset.dest, card.dataset.route, card.dataset.type, card.dataset.fare); return; }'
        '    var modal = document.getElementById("atlas-route-modal");'
        '    if (modal && e.target === modal) closeModal();'
        '  });'
        '  document.getElementById("atlas-modal-close").addEventListener("click", function(e) { e.stopPropagation(); closeModal(); });'
        '  document.addEventListener("keydown", function(e) { if (e.key === "Escape") closeModal(); });'
        '})();'
        '</script>'
    )

    body = top_html + modal_html + js_html
    return build_shell("Transportation", body, "transport", user=user)
