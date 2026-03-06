# includes/template.py
# ─────────────────────────────────────────────────────────────
# WHAT THIS FILE CONTROLS:
#   - Navbar (logo, links, login/signup buttons)
#   - Category tiles row below navbar
#   - Footer (LocalFlair-style, 4 columns)
#   - Booking modal
#   - Login / Register MODALS (popup overlays)
#   - NO status bar, NO API credits, NO team names
# ─────────────────────────────────────────────────────────────

def build_shell(page_title: str, body_content: str, active: str = "") -> str:

    def na(page):
        return "active" if active == page else ""

    def ta(page):
        return "active" if active == page else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{page_title} — ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
</head>
<body>

<!-- ══════════════════════════════════════════════════════════
     NAVBAR  (LocalFlair style)
     FILE: includes/template.py  → build_shell() → NAVBAR section
     Links: Home · Categories (dropdown) · About Us · Log In · Sign Up
     ══════════════════════════════════════════════════════════ -->
<nav class="topnav">
  <div class="nav-inner">

    <!-- Logo -->
    <a href="/" class="logo">
      <div class="logo-box">A</div>
      <span class="logo-text">ATLAS</span>
    </a>

    <!-- Main links -->
    <div class="nav-links">
      <a href="/" class="nav-link {na('home')}">Home</a>

      <!-- Categories dropdown -->
      <div class="dropdown" id="cat-drop">
        <button class="nav-link drop-btn" onclick="toggleDrop()">
          Categories
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="drop-menu" id="drop-menu">
          <a href="/flights.py"     class="drop-item">✈️ Flights</a>
          <a href="/weather.py"     class="drop-item">🌤️ Weather</a>
          <a href="/attractions.py" class="drop-item">🏛️ Tourist Attractions</a>
          <a href="/restaurants.py" class="drop-item">🍽️ Restaurants</a>
          <a href="/guides.py"      class="drop-item">🧭 Tour Guides</a>
          <a href="/transport.py"   class="drop-item">🚌 Transportation</a>
          <a href="/itinerary.py"   class="drop-item">📅 Itinerary</a>
        </div>
      </div>

      <a href="#about" class="nav-link">About Us</a>
    </div>

    <!-- Auth buttons -->
    <div class="nav-auth">
      <button class="btn-login" onclick="openModal('login')">Log In</button>
      <button class="btn-signup" onclick="openModal('register')">Sign Up</button>
    </div>

  </div>
</nav>

<!-- ══════════════════════════════════════════════════════════
     CATEGORY TILES ROW
     FILE: includes/template.py  → build_shell() → TILES section
     ══════════════════════════════════════════════════════════ -->
<div class="tiles-bar">
  <div class="tiles-inner">
    <a href="/flights.py"     class="tile {ta('flights')}">  <span class="tile-icon">✈️</span> <span class="tile-lbl">Flight Search</span></a>
    <a href="/attractions.py" class="tile {ta('attractions')}"><span class="tile-icon">🏛️</span><span class="tile-lbl">Tourist Attractions</span></a>
    <a href="/restaurants.py" class="tile {ta('restaurants')}"><span class="tile-icon">🍽️</span><span class="tile-lbl">Restaurants</span></a>
    <a href="/guides.py"      class="tile {ta('guides')}">   <span class="tile-icon">🧭</span> <span class="tile-lbl">Tour Guide Booking</span></a>
    <a href="/weather.py"     class="tile {ta('weather')}">  <span class="tile-icon">🌤️</span><span class="tile-lbl">Weather Forecast</span></a>
    <a href="/transport.py"   class="tile {ta('transport')}"><span class="tile-icon">🚌</span> <span class="tile-lbl">Transportation</span></a>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════
     PAGE CONTENT injected here
     ══════════════════════════════════════════════════════════ -->
{body_content}

<!-- ══════════════════════════════════════════════════════════
     FOOTER  (LocalFlair style, 4 columns)
     FILE: includes/template.py  → build_shell() → FOOTER section
     NO team names, NO API credits, NO course/subject info
     ══════════════════════════════════════════════════════════ -->
<footer class="site-footer" id="about">
  <div class="footer-top">
    <div class="footer-brand">
      <div class="footer-logo">
        <div class="logo-box" style="width:30px;height:30px;font-size:14px">A</div>
        <span style="font-size:18px;font-weight:900;color:#CE1126">ATLAS</span>
      </div>
      <p style="font-size:13px;color:#9CA3AF;max-width:220px;line-height:1.6">Your Luzon Travel Companion</p>
    </div>
    <div class="footer-cols">
      <div class="footer-col">
        <div class="footer-col-hdr">The Company</div>
        <a href="/">Home</a>
        <a href="#about">About Us</a>
        <a href="#" onclick="openModal('register');return false">Register</a>
        <a href="#" onclick="openModal('login');return false">Login</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-hdr">Help</div>
        <a href="#">FAQ</a>
        <a href="#">Deliveries</a>
        <a href="#">Contact Us</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-hdr">Legalities</div>
        <a href="#">Privacy Policy</a>
        <a href="#">Terms of Use</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-hdr">Contact</div>
        <div class="footer-contact"><strong>Office Hours:</strong><br>9:00 am – 6:00 pm</div>
        <div class="footer-contact"><strong>Location:</strong><br>Luzon, Philippines</div>
        <div class="footer-contact"><strong>Email:</strong><br>atlas@travel.ph</div>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 ATLAS. All Rights Reserved.</span>
  </div>
</footer>

<!-- ══════════════════════════════════════════════════════════
     LOGIN MODAL
     FILE: includes/template.py  → build_shell() → LOGIN MODAL
     Split panel: left=photo, right=form
     ══════════════════════════════════════════════════════════ -->
<div class="modal-overlay" id="modal-login" onclick="if(event.target===this)closeModal('login')">
  <div class="auth-modal">
    <div class="auth-photo" style="background-image:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80')">
      <div class="auth-photo-overlay"></div>
      <div class="auth-photo-text">
        <h2>ENJOY THE<br>WORLD</h2>
        <p>Discover the beauty of Luzon — flights, weather, attractions and more in one place.</p>
        <button class="auth-learn-btn" onclick="closeModal('login')">Learn More</button>
      </div>
    </div>
    <div class="auth-form-panel">
      <button class="auth-close" onclick="closeModal('login')">✕</button>
      <div class="auth-brand">
        <div class="logo-box" style="width:28px;height:28px;font-size:13px">A</div>
        <span style="font-weight:800;color:#fff;font-size:13px">ATLAS travel</span>
      </div>
      <div class="auth-title">Sign In</div>
      <form method="post" action="/login.py">
        <label class="auth-lbl">Email *</label>
        <input class="auth-inp" type="email" name="email" placeholder="you@example.com" required/>
        <label class="auth-lbl">Password *</label>
        <input class="auth-inp" type="password" name="password" placeholder="••••••••" required/>
        <button class="auth-submit" type="submit">Continue →</button>
      </form>
      <div class="auth-sep"><span>or</span></div>
      <button class="auth-alt-btn" onclick="switchModal('login','register')">Create Account</button>
      <div class="auth-foot">No account? <a onclick="switchModal('login','register')">Sign Up</a></div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════
     REGISTER MODAL
     FILE: includes/template.py  → build_shell() → REGISTER MODAL
     ══════════════════════════════════════════════════════════ -->
<div class="modal-overlay" id="modal-register" onclick="if(event.target===this)closeModal('register')">
  <div class="auth-modal">
    <div class="auth-photo auth-photo-alt" style="background-image:url('https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=800&q=80')">
      <div class="auth-photo-overlay"></div>
      <div class="auth-photo-text">
        <h2>JOIN<br>ATLAS</h2>
        <p>Create your free account and start planning your perfect Luzon adventure today.</p>
        <button class="auth-learn-btn" onclick="closeModal('register')">Explore First</button>
      </div>
    </div>
    <div class="auth-form-panel">
      <button class="auth-close" onclick="closeModal('register')">✕</button>
      <div class="auth-brand">
        <div class="logo-box" style="width:28px;height:28px;font-size:13px">A</div>
        <span style="font-weight:800;color:#fff;font-size:13px">ATLAS travel</span>
      </div>
      <div class="auth-title">Create Account</div>
      <form method="post" action="/register.py">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
          <div><label class="auth-lbl">First Name *</label><input class="auth-inp" type="text" name="fname" placeholder="Juan" required/></div>
          <div><label class="auth-lbl">Last Name *</label><input class="auth-inp" type="text" name="lname" placeholder="Cruz" required/></div>
        </div>
        <label class="auth-lbl">Email *</label>
        <input class="auth-inp" type="email" name="email" placeholder="you@example.com" required/>
        <label class="auth-lbl">Password *</label>
        <input class="auth-inp" type="password" name="password" placeholder="Min. 8 characters" required/>
        <div style="font-size:10px;color:rgba(255,255,255,.4);margin:-6px 0 8px">Minimum 8 characters</div>
        <label class="auth-lbl">Confirm Password *</label>
        <input class="auth-inp" type="password" name="confirm" placeholder="Repeat password" required/>
        <button class="auth-submit" style="background:#CE1126" type="submit">Continue →</button>
      </form>
      <div class="auth-sep"><span>or</span></div>
      <button class="auth-alt-btn" onclick="switchModal('register','login')">Sign In Instead</button>
      <div class="auth-foot">Have account? <a onclick="switchModal('register','login')">Sign In</a></div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════
     TOUR GUIDE BOOKING MODAL
     FILE: includes/template.py  → build_shell() → BOOKING MODAL
     ══════════════════════════════════════════════════════════ -->
<div class="modal-overlay" id="booking-modal" onclick="if(event.target===this)closeBooking()">
  <div class="modal-box">
    <div class="modal-hdr">
      <div style="font-weight:800;font-size:18px">Book Tour Guide</div>
      <div id="modal-guide-name" style="opacity:.8;font-size:14px;margin-top:4px"></div>
    </div>
    <div class="modal-body">
      <div style="margin-bottom:14px"><label class="lbl">Tour Date</label><input class="inp" type="date" id="m-date"/></div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px">
        <div><label class="lbl">Duration (days)</label><input class="inp" id="m-dur" value="2"/></div>
        <div><label class="lbl">Group Size</label><input class="inp" id="m-grp" value="3"/></div>
      </div>
      <div style="margin-bottom:20px"><label class="lbl">Special Requests</label><input class="inp" placeholder="Any requirements..."/></div>
      <div style="display:flex;gap:10px">
        <button class="btn" style="background:#0038A8;color:#fff;flex:1;padding:11px" onclick="confirmBooking()">Confirm Booking</button>
        <button class="btn-outline" style="flex:1;padding:11px" onclick="closeBooking()">Cancel</button>
      </div>
    </div>
  </div>
</div>

<div id="toast"></div>

<script>
// ── DROPDOWN ──────────────────────────────────────────────
function toggleDrop() {{
  document.getElementById('cat-drop').classList.toggle('open');
}}
document.addEventListener('click', function(e) {{
  var d = document.getElementById('cat-drop');
  if (d && !d.contains(e.target)) d.classList.remove('open');
}});

// ── AUTH MODALS ───────────────────────────────────────────
function openModal(type) {{
  document.getElementById('modal-' + type).style.display = 'flex';
  document.body.style.overflow = 'hidden';
}}
function closeModal(type) {{
  document.getElementById('modal-' + type).style.display = 'none';
  document.body.style.overflow = '';
}}
function switchModal(from, to) {{
  closeModal(from);
  setTimeout(function() {{ openModal(to); }}, 150);
}}

// ── BOOKING MODAL ─────────────────────────────────────────
function openBookingModal(name) {{
  document.getElementById('modal-guide-name').textContent = name;
  document.getElementById('booking-modal').style.display = 'flex';
  document.body.style.overflow = 'hidden';
}}
function closeBooking() {{
  document.getElementById('booking-modal').style.display = 'none';
  document.body.style.overflow = '';
}}
function confirmBooking() {{
  var name = document.getElementById('modal-guide-name').textContent;
  closeBooking();
  showToast('Booking sent to ' + name + '!');
}}

// ── TOAST ─────────────────────────────────────────────────
function showToast(msg) {{
  var t = document.getElementById('toast');
  t.textContent = msg;
  t.style.display = 'block';
  setTimeout(function() {{ t.style.display = 'none'; }}, 2800);
}}
</script>
</body>
</html>"""
