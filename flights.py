def _card(f):
    col = AIRLINE_COLORS.get(f["airline"], "#374151")
    origin = f["from"].split("(")[0].strip()
    dest = f["to"].split("(")[0].strip()
    airline = f["airline"]
    status = f.get("status", "Scheduled")
    gf_q = urllib.parse.quote(f"{origin} to {dest}")
    booking_link = f"https://www.google.com/travel/flights?q={gf_q}"

    return f"""
    <div class="grid-card">
        <div class="flight-grid-top" style="background:linear-gradient(135deg,{col},{col}99)">
            <div style="margin-bottom:8px">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13"/><path d="M22 2L15 22 11 13 2 9l20-7z"/></svg>
            </div>
            <div style="font-weight:800;font-size:13px;margin-bottom:8px">{airline}</div>
            <div class="flight-route">
                <span class="route-iata">{origin}</span>
                <span class="route-arrow">➔</span>
                <span class="route-iata">{dest}</span>
            </div>
            <div class="flight-status-tag">{status}</div>
        </div>
        <div class="grid-card-body">
            <div class="flight-info-grid">
                <div class="info-stat">
                    <div class="stat-label">Departs</div>
                    <div class="stat-value">{f['dep']}</div>
                </div>
                <div class="info-stat">
                    <div class="stat-label">Arrives</div>
                    <div class="stat-value">{f['arr']}</div>
                </div>
                <div class="info-stat">
                    <div class="stat-label">Duration</div>
                    <div class="stat-value" style="font-size:13px">{f['dur']}</div>
                </div>
                <div class="info-stat">
                    <div class="stat-label">Price</div>
                    <div class="stat-value" style="color:#CE1126">{f['price']}</div>
                </div>
            </div>
            <a href="{booking_link}" target="_blank" style="text-decoration:none">
                <button class="btn" style="background:{col};color:#fff;width:100%;padding:10px;font-weight:700">Book Flight</button>
            </a>
        </div>
    </div>"""