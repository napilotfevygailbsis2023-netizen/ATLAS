import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def build_shell(page_title, body_content, active="", user=None):
    def na(p): return "active" if active == p else ""
    def ta(p): return "active" if active == p else ""

    # Navbar auth section - changes based on login state
    is_logged_in = 'true' if user else 'false'
    if user:
        fname = user.get("fname","User")
        lname = user.get("lname","")
        auth_html = f"""
        <div class="nav-auth">
          <div class="user-pill" onclick="toggleProfileDrop()" style="cursor:pointer;position:relative">
            <div class="user-avatar">{fname[0].upper()}</div>
            <span class="user-name">{fname} {lname} &#9662;</span>
            <div id="profile-drop" style="display:none;position:absolute;top:48px;right:0;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,.15);min-width:200px;z-index:999;overflow:hidden">
              <div style="padding:14px 16px;border-bottom:1px solid #F3F4F6;background:#F9FAFB">
                <div style="font-weight:700;font-size:14px;color:#1F2937">{fname} {lname}</div>
                <div style="font-size:12px;color:#6B7280">Tourist Account</div>
              </div>
              <a href="/profile.py" style="display:flex;align-items:center;gap:10px;padding:12px 16px;text-decoration:none;color:#374151;font-size:14px;border-bottom:1px solid #F3F4F6" onmouseover="this.style.background='#F3F4F6'" onmouseout="this.style.background=''">
                &#128100; My Profile
              </a>
              <a href="/itinerary.py" style="display:flex;align-items:center;gap:10px;padding:12px 16px;text-decoration:none;color:#374151;font-size:14px;border-bottom:1px solid #F3F4F6" onmouseover="this.style.background='#F3F4F6'" onmouseout="this.style.background=''">
                &#128197; My Itinerary
              </a>
              <a href="/logout.py" style="display:flex;align-items:center;gap:10px;padding:12px 16px;text-decoration:none;color:#CE1126;font-size:14px" onmouseover="this.style.background='#FEF2F2'" onmouseout="this.style.background=''">
                &#128682; Log Out
              </a>
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
        auth_html = """
        <div class="nav-auth">
          <a href="/login.py"><button class="btn-login">Log In</button></a>
          <a href="/register.py"><button class="btn-signup">Sign Up</button></a>
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
      <div class="logo-box">A</div>
      <span class="logo-text">ATLAS</span>
    </a>
    <div class="nav-links">
      <a href="/" class="nav-link {na('home')}">Home</a>
      <div class="dropdown" id="cat-drop">
        <button class="nav-link drop-btn" onclick="toggleDrop()">Categories &#9662;</button>
        <div class="drop-menu" id="drop-menu">
          <a href="/flights.py"     class="drop-item">&#9992; Flights</a>
          <a href="/weather.py"     class="drop-item">&#127748; Weather</a>
          <a href="/attractions.py" class="drop-item">&#127963; Tourist Attractions</a>
          <a href="/restaurants.py" class="drop-item">&#127869; Restaurants</a>
          <a href="/guides.py"      class="drop-item">&#129517; Tour Guides</a>
          <a href="/transport.py"   class="drop-item">&#128652; Transportation</a>
          <a href="/itinerary.py"   class="drop-item">&#128197; Itinerary</a>
        </div>
      </div>
      <a href="#about" class="nav-link">About Us</a>
    </div>
    {auth_html}
  </div>
</nav>
<div class="tiles-bar">
  <div class="tiles-inner">
    <a href="/flights.py"     class="tile {ta('flights')}">  <span class="tile-icon">&#9992;</span>  <span class="tile-lbl">Flight Search</span></a>
    <a href="/attractions.py" class="tile {ta('attractions')}"><span class="tile-icon">&#127963;</span><span class="tile-lbl">Tourist Attractions</span></a>
    <a href="/restaurants.py" class="tile {ta('restaurants')}"><span class="tile-icon">&#127869;</span><span class="tile-lbl">Restaurants</span></a>
    <a href="/guides.py"      class="tile {ta('guides')}">   <span class="tile-icon">&#129517;</span> <span class="tile-lbl">Tour Guide Booking</span></a>
    <a href="/weather.py"     class="tile {ta('weather')}">  <span class="tile-icon">&#127748;</span><span class="tile-lbl">Weather Forecast</span></a>
    <a href="/transport.py"   class="tile {ta('transport')}"><span class="tile-icon">&#128652;</span> <span class="tile-lbl">Transportation</span></a>
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

<!-- Sign-In Required Modal -->
<div id="signin-gate" style="display:none;position:fixed;inset:0;z-index:9999;align-items:center;justify-content:center">
  <div style="position:absolute;inset:0;background:rgba(0,0,0,.45);backdrop-filter:blur(4px)" onclick="closeSigninGate()"></div>
  <div style="position:relative;background:#fff;border-radius:24px;padding:44px 36px;max-width:440px;width:90%;text-align:center;box-shadow:0 24px 64px rgba(0,0,0,.2);z-index:1">
    <button onclick="closeSigninGate()" style="position:absolute;top:14px;right:16px;background:rgba(0,0,0,.07);border:none;border-radius:50%;width:30px;height:30px;font-size:16px;cursor:pointer;color:#6B7280">&#x2715;</button>
    <div style="font-size:52px;margin-bottom:12px">&#128274;</div>
    <div style="font-size:22px;font-weight:900;color:#1F2937;margin-bottom:8px">Sign In to Continue</div>
    <div style="font-size:14px;color:#6B7280;line-height:1.7;margin-bottom:24px">Log in or create a free account to access this feature and explore everything ATLAS has to offer.</div>
    <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:20px;text-align:left">
      <div style="display:flex;align-items:center;gap:10px;background:#F9FAFB;border-radius:10px;padding:10px 14px;font-size:13px;color:#374151"><span style="font-size:18px">&#128197;</span> Build and save your travel itinerary</div>
      <div style="display:flex;align-items:center;gap:10px;background:#F9FAFB;border-radius:10px;padding:10px 14px;font-size:13px;color:#374151"><span style="font-size:18px">&#129517;</span> Book certified local tour guides</div>
      <div style="display:flex;align-items:center;gap:10px;background:#F9FAFB;border-radius:10px;padding:10px 14px;font-size:13px;color:#374151"><span style="font-size:18px">&#9992;</span> Search real-time flights &amp; weather</div>
    </div>
    <div style="display:flex;gap:12px;justify-content:center">
      <a href="/login.py" style="flex:1;padding:13px;border:2px solid #0038A8;border-radius:12px;font-size:14px;font-weight:700;color:#0038A8;text-decoration:none;display:block">Log In</a>
      <a href="/register.py" style="flex:1;padding:13px;background:linear-gradient(135deg,#CE1126,#0038A8);border-radius:12px;font-size:14px;font-weight:700;color:#fff;text-decoration:none;display:block">Create Account</a>
    </div>
  </div>
</div>
<footer class="site-footer" id="about">
  <div class="footer-top">
    <div class="footer-brand">
      <div class="footer-logo">
        <div class="logo-box" style="width:30px;height:30px;font-size:14px">A</div>
        <span style="font-size:18px;font-weight:900;color:#CE1126">ATLAS</span>
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
        <div class="footer-contact"><strong>Email:</strong><br>atlas@travel.ph</div>
      </div>
    </div>
  </div>
  <div class="footer-bottom"><span>&copy; 2026 ATLAS. All Rights Reserved.</span></div>
</footer>
<script>
var ATLAS_LOGGED_IN = {is_logged_in};
var PROTECTED = ['/flights.py','/weather.py','/attractions.py','/restaurants.py','/guides.py','/transport.py','/itinerary.py','/profile.py'];
function openSigninGate(){{document.getElementById('signin-gate').style.display='flex';document.body.style.overflow='hidden';}}
function closeSigninGate(){{document.getElementById('signin-gate').style.display='none';document.body.style.overflow='';}}
document.addEventListener('click',function(e){{
  var a=e.target.closest('a');
  if(!a) return;
  var href=a.getAttribute('href')||'';
  var path=href.split('?')[0];
  if(!ATLAS_LOGGED_IN && PROTECTED.indexOf(path)!==-1){{
    e.preventDefault();
    openSigninGate();
  }}
}});
function toggleDrop(){{document.getElementById('cat-drop').classList.toggle('open');}}
document.addEventListener('click',function(e){{var d=document.getElementById('cat-drop');if(d&&!d.contains(e.target))d.classList.remove('open');}});
function openBookingModal(name){{document.getElementById('modal-guide-name').textContent=name;document.getElementById('booking-modal').style.display='flex';document.body.style.overflow='hidden';}}
function closeBooking(){{document.getElementById('booking-modal').style.display='none';document.body.style.overflow='';}}
function confirmBooking(){{var name=document.getElementById('modal-guide-name').textContent;closeBooking();showToast('Booking sent to '+name+'!');}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.style.display='block';setTimeout(function(){{t.style.display='none';}},2800);}}
</script>
</body>
</html>"""
