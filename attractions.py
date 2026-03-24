def _card(s):
    col   = CAT_COLORS.get(s["cat"],"#0038A8")
    icon  = CAT_ICONS.get(s["cat"],"🏛")
    city  = s["city"]
    name  = s["name"]
    img   = s.get("img","") or (f"https://source.unsplash.com/800x500/?{urllib.parse.quote(name+' Philippines')}")
    maps  = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(name + ' ' + city + ' Philippines')}"
    desc  = s.get("desc","")
    entry = s.get("entry","Check on-site")
    hours = s.get("hours","Check on-site")
    full  = int(round(s["rating"]))
    stars = "★" * full + "☆" * (5 - full)
    mid   = "m" + str(abs(hash(name + city)) % 999999)
    ns    = name.replace("'","\\'")
    cs    = city.replace("'","\\'")

    def H(x): return x.replace('"','&quot;')

    modal = f"""
    <div id="{mid}" class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header" style="background:linear-gradient(135deg,{col},{col}99)">
                <div style="margin-bottom:8px">{icon}</div>
                <div style="font-weight:800;font-size:18px;color:#fff">{H(name)}</div>
                <div style="font-size:13px;color:rgba(255,255,255,.8);margin-top:4px">📍 {H(city)}</div>
                <button onclick="closeModal('{mid}')" class="modal-close">✕</button>
            </div>
            <div class="modal-body">
                <img src="{H(img)}" class="modal-img" onerror="this.style.display='none'"/>
                <div style="color:#F59E0B;font-size:14px;margin-bottom:10px">{stars} <span style="color:#9CA3AF">{s['rating']}</span></div>
                <div class="modal-grid">
                    <div class="modal-stat-box">
                        <div class="modal-stat-label">Entry Fee</div>
                        <div class="modal-stat-value">{entry}</div>
                    </div>
                    <div class="modal-stat-box">
                        <div class="modal-stat-label">Hours</div>
                        <div class="modal-stat-value" style="color:#1A1A2E">{hours}</div>
                    </div>
                </div>
                <p style="font-size:13px;color:#4B5563;line-height:1.7;margin-bottom:18px">{desc}</p>
                <div style="display:flex;flex-direction:column;gap:8px">
                    <button class="btn" style="background:{col};color:#fff;width:100%;padding:10px;font-size:14px" onclick="addToItinerary('{ns}','{cs}');closeModal('{mid}')">+ Add to Itinerary</button>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
                        <a href="/restaurants.py?city={city}" style="text-decoration:none"><button class="btn" style="background:#0038A8;color:#fff;width:100%;padding:9px;font-size:13px">Nearby Food</button></a>
                        <a href="{maps}" target="_blank" style="text-decoration:none"><button class="btn" style="background:#0038A8;color:#fff;width:100%;padding:9px;font-size:13px">Directions</button></a>
                    </div>
                </div>
            </div>
        </div>
    </div>"""

    card = f"""
    {modal}
    <div class="grid-card" style="cursor:pointer" onclick="if(typeof ATLAS_LOGGED_IN!=='undefined'&&!ATLAS_LOGGED_IN){{openSigninGate();}}else{{document.getElementById('{mid}').style.display='flex';}}">
        <div class="grid-card-top" style="background:linear-gradient(135deg,{col},{col}99)">
            <div style="margin-bottom:10px;display:flex;justify-content:center">{icon}</div>
            <div style="font-weight:800;font-size:15px;color:#fff;margin-bottom:4px">{H(name)}</div>
            <span class="badge" style="background:rgba(255,255,255,.2);color:#fff">{s['cat']}</span>
        </div>
        <div class="grid-card-body">
            <img src="{H(img)}" alt="{H(name)}" style="width:100%;height:130px;object-fit:cover;border-radius:10px;margin-bottom:10px" onerror="this.style.display='none'"/>
            <div style="color:#F59E0B;font-size:13px;margin-bottom:6px">{stars} <span style="color:#9CA3AF">{s['rating']}</span></div>
            <div style="font-size:12px;color:#6B7280;margin-bottom:2px">📍 {H(city)}</div>
            <div style="font-size:14px;font-weight:800;color:#0038A8;margin:8px 0 6px">Entry: {entry}</div>
            <div style="font-size:12px;color:#6B7280;line-height:1.5;margin-bottom:14px">{desc[:80]}...</div>
            <div style="font-size:12px;color:#0038A8;font-weight:600;text-align:center;padding:6px 0">👁 View Spot Details</div>
        </div>
    </div>"""
    return card