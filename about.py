import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tourist_ui import build_shell

TEAM = [
    {
        "name": "Reign Beau Vargas",
        "role": "Project Lead & Full-Stack Developer",
        "avatar": "R",
        "color": "#0038A8",
        "desc": "Leads the ATLAS development team and oversees the system architecture, backend logic, and deployment pipeline.",
    },
    {
        "name": "Team Member 2",
        "role": "Frontend Developer",
        "avatar": "T",
        "color": "#CE1126",
        "desc": "Responsible for crafting the user interface, responsive layouts, and seamless user experience across all pages.",
    },
    {
        "name": "Team Member 3",
        "role": "Database Administrator",
        "avatar": "T",
        "color": "#C8930A",
        "desc": "Manages the MySQL database schema, migrations, query optimization, and data integrity for the platform.",
    },
    {
        "name": "Team Member 4",
        "role": "UI/UX Designer",
        "avatar": "T",
        "color": "#065F46",
        "desc": "Designs the visual identity of ATLAS, including wireframes, mockups, color systems, and brand guidelines.",
    },
]

FEATURES = [
    {"icon": "✈️", "title": "Flight Search",        "desc": "Live domestic & international flight data from Manila and Pampanga airports, with real-time status and direct booking links."},
    {"icon": "🏛️", "title": "Tourist Attractions",  "desc": "Hand-curated top spots across Luzon — from heritage sites in Vigan to natural wonders in Batangas and Albay."},
    {"icon": "🧑‍💼", "title": "Tour Guide Booking",  "desc": "Connect with verified local guides featuring transparent pricing, ratings, availability, and multilingual support."},
    {"icon": "🌤️", "title": "Live Weather",          "desc": "Real-time forecasts and travel advisories for every major Luzon city, with severe weather flight warnings."},
    {"icon": "🍽️", "title": "Restaurants",           "desc": "Discover the best local and international dining spots across Luzon, filtered by city, cuisine, and budget."},
    {"icon": "🚌", "title": "Transportation",        "desc": "Ground, sea, and rail routes across Luzon — buses, vans, ferries, trains, and jeepneys with schedules and fares."},
    {"icon": "📅", "title": "Trip Itinerary",        "desc": "AI-powered itinerary builder that creates personalised day-by-day travel plans for any Luzon destination."},
    {"icon": "🗺️", "title": "Luzon Coverage",        "desc": "Comprehensive coverage of all major Luzon provinces — from Metro Manila to the Ilocos Region and Bicol."},
]

STATS = [
    {"value": "50+",  "label": "Luzon Destinations"},
    {"value": "100+", "label": "Tourist Attractions"},
    {"value": "30+",  "label": "Partner Restaurants"},
    {"value": "24/7", "label": "Live Data Updates"},
]


def render(user=None):
    # ── Stats bar ──
    stats_html = "".join(f"""
        <div style="text-align:center;padding:24px 16px">
          <div style="font-size:36px;font-weight:900;color:#0038A8">{s['value']}</div>
          <div style="font-size:13px;color:#6B7280;margin-top:4px;font-weight:600">{s['label']}</div>
        </div>""" for s in STATS)

    # ── Feature cards ──
    feat_html = "".join(f"""
        <div style="background:#fff;border:1px solid #E2E8F0;border-radius:16px;padding:24px;box-shadow:0 2px 8px rgba(0,0,0,.05);transition:.2s"
             onmouseover="this.style.boxShadow='0 8px 24px rgba(0,56,168,.12)';this.style.borderColor='#0038A8'"
             onmouseout="this.style.boxShadow='0 2px 8px rgba(0,0,0,.05)';this.style.borderColor='#E2E8F0'">
          <div style="font-size:36px;margin-bottom:12px">{f['icon']}</div>
          <div style="font-weight:800;font-size:16px;color:#0F172A;margin-bottom:8px">{f['title']}</div>
          <div style="font-size:13px;color:#6B7280;line-height:1.7">{f['desc']}</div>
        </div>""" for f in FEATURES)

    # ── Team cards ──
    team_html = "".join(f"""
        <div style="background:#fff;border:1px solid #E2E8F0;border-radius:16px;padding:28px 20px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.05)">
          <div style="width:72px;height:72px;border-radius:50%;background:{m['color']};display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;color:#fff;margin:0 auto 14px">{m['avatar']}</div>
          <div style="font-weight:800;font-size:16px;color:#0F172A;margin-bottom:4px">{m['name']}</div>
          <div style="font-size:12px;font-weight:700;color:{m['color']};margin-bottom:10px;text-transform:uppercase;letter-spacing:.5px">{m['role']}</div>
          <div style="font-size:13px;color:#6B7280;line-height:1.6">{m['desc']}</div>
        </div>""" for m in TEAM)

    body = f"""
    <!-- Hero Banner -->
    <div style="background:linear-gradient(135deg,#003087 0%,#0038A8 60%,#001a5e 100%);padding:72px 24px;text-align:center;position:relative;overflow:hidden">
      <div style="position:absolute;width:400px;height:400px;border-radius:50%;background:rgba(255,255,255,.05);top:-120px;left:-100px"></div>
      <div style="position:absolute;width:300px;height:300px;border-radius:50%;background:rgba(255,255,255,.04);bottom:-80px;right:-60px"></div>
      <div style="position:relative;z-index:2;max-width:720px;margin:0 auto">
        <div style="display:inline-block;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);border-radius:30px;padding:6px 20px;font-size:13px;font-weight:700;color:#fff;margin-bottom:20px;letter-spacing:1px">OUR STORY</div>
        <h1 style="font-size:clamp(28px,5vw,48px);font-weight:900;color:#fff;margin:0 0 16px;line-height:1.2">About <span style="color:#FCD116">ATLAS</span></h1>
        <p style="font-size:16px;color:rgba(255,255,255,.85);line-height:1.8;margin:0 auto;max-width:600px">
          ATLAS — <strong>Accessible Travel and Luzon Assistance System</strong> — is a capstone project built to empower tourists with everything they need to explore Luzon, Philippines in one seamless platform.
        </p>
      </div>
    </div>

    <div class="page-wrap" style="max-width:1100px">

      <!-- Stats -->
      <div style="background:#fff;border:1px solid #E2E8F0;border-radius:16px;box-shadow:0 2px 12px rgba(0,0,0,.06);margin:-36px auto 48px;display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));overflow:hidden">
        {stats_html}
      </div>

      <!-- Mission -->
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;margin-bottom:64px" class="about-split">
        <div>
          <div style="font-size:11px;font-weight:800;color:#0038A8;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px">Our Mission</div>
          <h2 style="font-size:28px;font-weight:900;color:#0F172A;margin:0 0 16px;line-height:1.3">Making Luzon Travel <span style="color:#0038A8">Accessible</span> for Everyone</h2>
          <p style="font-size:14px;color:#475569;line-height:1.8;margin-bottom:16px">
            We believe that every traveler — whether a first-time visitor or a seasoned explorer — deserves easy access to reliable, up-to-date travel information. ATLAS bridges the gap between tourists and the rich cultural, natural, and culinary heritage of Luzon.
          </p>
          <p style="font-size:14px;color:#475569;line-height:1.8">
            From real-time flight tracking and live weather alerts, to booking verified local guides and discovering hidden gems — ATLAS puts the entire Luzon travel ecosystem at your fingertips.
          </p>
        </div>
        <div style="background:linear-gradient(135deg,#EFF6FF,#DBEAFE);border-radius:20px;padding:36px;text-align:center">
          <div style="font-size:72px;margin-bottom:16px">🗺️</div>
          <div style="font-size:18px;font-weight:800;color:#0038A8;margin-bottom:8px">Luzon, Philippines</div>
          <div style="font-size:13px;color:#475569;line-height:1.6">Covering all major provinces from Metro Manila to the Ilocos Region, Cordillera, Cagayan Valley, Central Luzon, and Bicol.</div>
          <div style="margin-top:20px;display:flex;justify-content:center;gap:8px;flex-wrap:wrap">
            {"".join(f'<span style="background:#0038A8;color:#fff;font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px">{c}</span>' for c in ["Manila","Baguio","Vigan","Ilocos","Batangas","Tagaytay","Albay","Bataan"])}
          </div>
        </div>
      </div>

      <!-- Features Grid -->
      <div style="margin-bottom:64px">
        <div style="text-align:center;margin-bottom:32px">
          <div style="font-size:11px;font-weight:800;color:#0038A8;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px">What We Offer</div>
          <h2 style="font-size:28px;font-weight:900;color:#0F172A;margin:0">Everything You Need for Your Luzon Trip</h2>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px">
          {feat_html}
        </div>
      </div>

      <!-- Team -->
      <div style="margin-bottom:64px">
        <div style="text-align:center;margin-bottom:32px">
          <div style="font-size:11px;font-weight:800;color:#0038A8;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px">The Team</div>
          <h2 style="font-size:28px;font-weight:900;color:#0F172A;margin:0 0 10px">Built with ❤️ by Students</h2>
          <p style="font-size:14px;color:#6B7280">ATLAS is a capstone project developed by a dedicated team of computer science students.</p>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px">
          {team_html}
        </div>
      </div>

      <!-- Contact CTA -->
      <div style="background:linear-gradient(135deg,#0038A8,#001a5e);border-radius:20px;padding:48px 32px;text-align:center;margin-bottom:48px">
        <div style="font-size:36px;margin-bottom:16px">✉️</div>
        <h2 style="font-size:24px;font-weight:900;color:#fff;margin:0 0 10px">Get in Touch</h2>
        <p style="font-size:14px;color:rgba(255,255,255,.8);margin-bottom:24px;line-height:1.7">
          Have questions, feedback, or want to partner with us? We'd love to hear from you.
        </p>
        <a href="mailto:travelatatlas2026@gmail.com" style="text-decoration:none">
          <button style="background:#FCD116;color:#0F172A;border:none;border-radius:10px;padding:14px 32px;font-size:15px;font-weight:800;cursor:pointer">
            travelatatlas2026@gmail.com
          </button>
        </a>
        <div style="margin-top:16px;font-size:13px;color:rgba(255,255,255,.6)">📍 Luzon, Philippines</div>
      </div>

    </div>

    <style>
    @media (max-width: 700px) {{
      .about-split {{ grid-template-columns: 1fr !important; }}
    }}
    </style>
    """
    return build_shell("About Us", body, "about", user=user)
