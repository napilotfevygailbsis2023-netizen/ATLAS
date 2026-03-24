import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def build_shell(page_title, body_content, active="", user=None):
    def na(p): return "active" if active == p else ""
    def ta(p): return "active" if active == p else ""

    # Navbar auth section - changes based on login state
    if user:
        fname = user.get("fname","User")
        lname = user.get("lname","")
        auth_html = f"""
        <div class="nav-auth">
          <div class="user-pill" onclick="toggleProfileDrop()" style="cursor:pointer;position:relative">
            <div class="user-avatar">{fname[0].upper()}</div>
            <span class="user-name">{fname} {lname} <i class="fa-solid fa-chevron-down"></i></span>
            <div id="profile-drop" style="display:none;position:absolute;top:48px;right:0;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,.15);min-width:200px;z-index:999;overflow:hidden">
              <div style="padding:14px 16px;border-bottom:1px solid #F3F4F6;background:#F9FAFB">
                <div style="font-weight:700;font-size:14px;color:#1F2937">{fname} {lname}</div>
                <div style="font-size:12px;color:#6B7280">Tourist Account</div>
              </div>
              <a href="/profile.py" style="display:flex;align-items:center;gap:10px;padding:12px 16px;text-decoration:none;color:#374151;font-size:14px;border-bottom:1px solid #F3F4F6" onmouseover="this.style.background='#F3F4F6'" onmouseout="this.style.background=''">
                <i class="fa-solid fa-user"></i> My Profile
              </a>
              <a href="/itinerary.py" style="display:flex;align-items:center;gap:10px;padding:12px 16px;text-decoration:none;color:#374151;font-size:14px;border-bottom:1px solid #F3F4F6" onmouseover="this.style.background='#F3F4F6'" onmouseout="this.style.background=''">
                <i class="fa-regular fa-calendar"></i> My Itinerary
              </a>
              <a href="/logout.py" style="display:flex;align-items:center;gap:10px;padding:12px 16px;text-decoration:none;color:#DC2626;font-size:14px" onmouseover="this.style.background='#FEF2F2'" onmouseout="this.style.background=''">
                <i class="fa-solid fa-right-from-bracket"></i> Log Out
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
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
</head>
<body>
<nav class="topnav">
  <div class="nav-inner">
    <a href="/" class="logo">
      <img src="/ATLAS_LOGO.jpg" alt="ATLAS" style="width:38px;height:38px;border-radius:50%;object-fit:cover;"/>
      <span class="logo-text">ATLAS</span>
    </a>
    <div class="nav-links">
      <a href="/" class="nav-link {na('home')}">Home</a>
      <div class="dropdown" id="cat-drop">
        <button class="nav-link drop-btn" onclick="toggleDrop()">Categories <i class="fa-solid fa-chevron-down"></i></button>
        <div class="drop-menu" id="drop-menu">
          <a href="/flights.py"     class="drop-item"><i class="fa-solid fa-plane"></i> Flights</a>
          <a href="/weather.py"     class="drop-item"><i class="fa-solid fa-cloud-sun"></i> Weather</a>
          <a href="/attractions.py" class="drop-item"><i class="fa-solid fa-landmark"></i> Tourist Attractions</a>
          <a href="/restaurants.py" class="drop-item"><i class="fa-solid fa-utensils"></i> Restaurants</a>
          <a href="/guides.py"      class="drop-item"><i class="fa-solid fa-user-tie"></i> Tour Guides</a>
          <a href="/transport.py"   class="drop-item"><i class="fa-solid fa-bus"></i> Transportation</a>
          <a href="/itinerary.py"   class="drop-item"><i class="fa-regular fa-calendar"></i> Itinerary</a>
        </div>
      </div>
      <a href="#about" class="nav-link">About Us</a>
    </div>
    {auth_html}
  </div>
</nav>
<div class="tiles-bar">
  <div class="tiles-inner">
    <a href="/flights.py"     class="tile {ta('flights')}">  <span class="tile-icon"><i class="fa-solid fa-plane"></i></span>  <span class="tile-lbl">Flight Search</span></a>
    <a href="/attractions.py" class="tile {ta('attractions')}"><span class="tile-icon"><i class="fa-solid fa-landmark"></i></span><span class="tile-lbl">Tourist Attractions</span></a>
    <a href="/restaurants.py" class="tile {ta('restaurants')}"><span class="tile-icon"><i class="fa-solid fa-utensils"></i></span><span class="tile-lbl">Restaurants</span></a>
    <a href="/guides.py"      class="tile {ta('guides')}">   <span class="tile-icon"><i class="fa-solid fa-user-tie"></i></span> <span class="tile-lbl">Tour Guide Booking</span></a>
    <a href="/weather.py"     class="tile {ta('weather')}">  <span class="tile-icon"><i class="fa-solid fa-cloud-sun"></i></span><span class="tile-lbl">Weather Forecast</span></a>
    <a href="/transport.py"   class="tile {ta('transport')}"><span class="tile-icon"><i class="fa-solid fa-bus"></i></span> <span class="tile-lbl">Transportation</span></a>
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
        <span style="font-size:18px;font-weight:800;color:#DC2626">ATLAS</span>
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
function toggleDrop(){{document.getElementById('cat-drop').classList.toggle('open');}}
document.addEventListener('click',function(e){{var d=document.getElementById('cat-drop');if(d&&!d.contains(e.target))d.classList.remove('open');}});
function openBookingModal(name){{document.getElementById('modal-guide-name').textContent=name;document.getElementById('booking-modal').style.display='flex';document.body.style.overflow='hidden';}}
function closeBooking(){{document.getElementById('booking-modal').style.display='none';document.body.style.overflow='';}}
function confirmBooking(){{var name=document.getElementById('modal-guide-name').textContent;closeBooking();showToast('Booking sent to '+name+'!');}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.style.display='block';setTimeout(function(){{t.style.display='none';}},2800);}}
</script>
</body>
</html>"""
