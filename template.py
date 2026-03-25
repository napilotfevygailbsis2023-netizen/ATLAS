import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

_PLANE    = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13"/><path d="M22 2L15 22 11 13 2 9l20-7z"/></svg>'
_PIN      = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
_FORK     = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/></svg>'
_USERS    = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
_SUN      = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
_TRUCK    = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>'
_CAL      = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
_USER_SM  = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
_CAL_SM   = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
_LOGOUT   = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>'
_CHEVRON  = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>'
_LOGIN_I  = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>'
_SIGNUP_I = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>'

def build_shell(page_title, body_content, active="", user=None):
    def na(p): return "active" if active == p else ""
    def ta(p): return "active" if active == p else ""

    if user:
        fname = user.get("fname","User")
        lname = user.get("lname","")
        auth_html = f"""
        <div class="nav-auth">
          <div class="user-pill" onclick="toggleProfileDrop()" style="cursor:pointer;position:relative;display:inline-flex;align-items:center;gap:8px;background:#0038A8;border-radius:30px;padding:6px 14px 6px 8px">
            <div style="width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,.25);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#fff;flex-shrink:0">{fname[0].upper()}</div>
            <span style="font-size:13px;font-weight:700;color:#fff">{fname} {lname}</span>
            <span style="color:#fff;display:flex;align-items:center">{_CHEVRON}</span>
            <div id="profile-drop" style="display:none;position:absolute;top:48px;right:0;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,.15);min-width:200px;z-index:999;overflow:hidden">
              <div style="padding:14px 16px;border-bottom:1px solid #F3F4F6;background:#F9FAFB">
                <div style="font-weight:700;font-size:14px;color:#1F2937">{fname} {lname}</div>
                <div style="font-size:12px;color:#6B7280">Tourist Account</div>
              </div>
              <a href="/profile.py" style="display:flex;align-items:center;gap:10px;padding:12px 16px;text-decoration:none;color:#374151;font-size:14px;border-bottom:1px solid #F3F4F6" onmouseover="this.style.background='#F3F4F6'" onmouseout="this.style.background=''">{_USER_SM} My Profile</a>
              <a href="/itinerary.py" style="display:flex;align-items:center;gap:10px;padding:12px 16px;text-decoration:none;color:#374151;font-size:14px;border-bottom:1px solid #F3F4F6" onmouseover="this.style.background='#F3F4F6'" onmouseout="this.style.background=''">{_CAL_SM} My Itinerary</a>
              <a href="/logout.py" style="display:flex;align-items:center;gap:10px;padding:12px 16px;text-decoration:none;color:#CE1126;font-size:14px" onmouseover="this.style.background='#FEF2F2'" onmouseout="this.style.background=''">{_LOGOUT} Log Out</a>
            </div>
          </div>
        </div>
        <script>
        function toggleProfileDrop() {{
          var d = document.getElementById('profile-drop');
          d.style.display = d.style.display === 'none' ? 'block' : 'none';
        }}
        document.addEventListener('click', function(e) {{
          var pill = document.querySelector('.user-pill');
          if (pill && !pill.contains(e.target)) {{
            var d = document.getElementById('profile-drop');
            if (d) d.style.display = 'none';
          }}
        }});
        </script>"""
    else:
        auth_html = f"""
        <div class="nav-auth">
          <a href="/login.py" style="display:inline-flex;align-items:center;gap:6px;padding:8px 18px;border:1.5px solid #0038A8;border-radius:8px;color:#0038A8;font-weight:700;font-size:13px;text-decoration:none">{_LOGIN_I} Log In</a>
          <a href="/register.py" style="display:inline-flex;align-items:center;gap:6px;padding:8px 18px;background:#0038A8;border-radius:8px;color:#fff;font-weight:700;font-size:13px;text-decoration:none">{_SIGNUP_I} Sign Up</a>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{page_title} - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
</head>
<body>
<nav class="topnav">
  <div class="nav-inner">
    <a href="/" class="logo">
      <img src="/ATLAS_LOGO.jpg" alt="ATLAS" style="width:38px;height:38px;border-radius:50%;object-fit:cover;"/>
      <span class="logo-text" style="color:#0038A8;font-weight:900">ATLAS</span>
    </a>
    <div class="nav-links">
      <a href="/" class="nav-link {na('home')}">Home</a>
      <div class="dropdown" id="cat-drop">
        <button class="nav-link drop-btn" onclick="toggleDrop()">Categories &#9662;</button>
        <div class="drop-menu" id="drop-menu">
          <a href="/flights.py"     class="drop-item" style="display:flex;align-items:center;gap:8px">{_PLANE} Flights</a>
          <a href="/weather.py"     class="drop-item" style="display:flex;align-items:center;gap:8px">{_SUN} Weather</a>
          <a href="/attractions.py" class="drop-item" style="display:flex;align-items:center;gap:8px">{_PIN} Tourist Attractions</a>
          <a href="/restaurants.py" class="drop-item" style="display:flex;align-items:center;gap:8px">{_FORK} Restaurants</a>
          <a href="/guides.py"      class="drop-item" style="display:flex;align-items:center;gap:8px">{_USERS} Tour Guides</a>
          <a href="/transport.py"   class="drop-item" style="display:flex;align-items:center;gap:8px">{_TRUCK} Transportation</a>
          <a href="/itinerary.py"   class="drop-item" style="display:flex;align-items:center;gap:8px">{_CAL} Itinerary</a>
        </div>
      </div>
      <a href="#about" class="nav-link">About Us</a>
    </div>
    {auth_html}
  </div>
</nav>
<div class="tiles-bar">
  <div class="tiles-inner">
    <a href="/flights.py"     class="tile {ta('flights')}"><span class="tile-icon">{_PLANE}</span><span class="tile-lbl">Flight Search</span></a>
    <a href="/attractions.py" class="tile {ta('attractions')}"><span class="tile-icon">{_PIN}</span><span class="tile-lbl">Tourist Attractions</span></a>
    <a href="/restaurants.py" class="tile {ta('restaurants')}"><span class="tile-icon">{_FORK}</span><span class="tile-lbl">Restaurants</span></a>
    <a href="/guides.py"      class="tile {ta('guides')}"><span class="tile-icon">{_USERS}</span><span class="tile-lbl">Tour Guide Booking</span></a>
    <a href="/weather.py"     class="tile {ta('weather')}"><span class="tile-icon">{_SUN}</span><span class="tile-lbl">Weather Forecast</span></a>
    <a href="/transport.py"   class="tile {ta('transport')}"><span class="tile-icon">{_TRUCK}</span><span class="tile-lbl">Transportation</span></a>
  </div>
</div>
{body_content}
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
<footer class="site-footer" id="about">
  <div class="footer-top">
    <div class="footer-brand">
      <div class="footer-logo">
        <img src="/ATLAS_LOGO.jpg" alt="ATLAS" style="width:30px;height:30px;border-radius:50%;object-fit:cover;"/>
        <span style="font-size:18px;font-weight:900;color:#0038A8">ATLAS</span>
      </div>
      <p style="font-size:13px;color:#9CA3AF;max-width:200px;line-height:1.6;margin-top:8px">Your Luzon Travel Companion</p>
    </div>
    <div class="footer-cols">
      <div class="footer-col">
        <div class="footer-col-hdr">The Company</div>
        <a href="/">Home</a><a href="#about">About Us</a>
        <a href="/register.py">Register</a><a href="/login.py">Login</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-hdr">Help</div>
        <a href="#">FAQ</a><a href="#">How It Works</a><a href="#">Contact Us</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-hdr">Legalities</div>
        <a href="#">Privacy Policy</a><a href="#">Terms of Use</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-hdr">Contact</div>
        <div class="footer-contact"><strong>Office Hours:</strong><br>9:00 am - 6:00 pm</div>
        <div class="footer-contact"><strong>Location:</strong><br>Luzon, Philippines</div>
        <div class="footer-contact"><strong>Email:</strong><br>travelatatlas2026@gmail.com
</div>
      </div>
    </div>
  </div>
  <div class="footer-bottom"><span>&copy; 2026 ATLAS. All Rights Reserved.</span></div>
</footer>
<script>
function toggleDrop(){{document.getElementById('cat-drop').classList.toggle('open');}}
document.addEventListener('click',function(e){{var d=document.getElementById('cat-drop');if(d&&!d.contains(e.target))d.classList.remove('open');}});
function openBookingModal(name){{document.getElementById('modal-guide-name').textContent=name;document.getElementById('booking-modal').style.display='flex';document.body.style.overflow='hidden';}}
function closeBooking(){{document.getElementById('booking-modal').style.display='none';document.body.style.overflow='';}}
function confirmBooking(){{var name=document.getElementById('modal-guide-name').textContent;closeBooking();showToast('Booking sent to '+name+'!');}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.style.display='block';setTimeout(function(){{t.style.display='none';}},2800);}}
</script>
</body>
</html>"""
