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

def build_shell(page_title, body_content, active="", user=None, csrf_token=""):
    def na(p): return "active" if active == p else ""
    def ta(p): return "active" if active == p else ""

    if user:
        fname = user.get("fname","") or user.get("email","user@").split("@")[0].capitalize()
        fname = fname if fname.strip() else "User"
        lname = user.get("lname","") or ""
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
        # Only show Log In button (no Sign Up) in navbar
        auth_html = f"""
        <div class="nav-auth">
          <button onclick="openSigninGate()" style="display:inline-flex;align-items:center;gap:6px;padding:8px 18px;background:#0038A8;border-radius:8px;color:#fff;font-weight:700;font-size:13px;border:none;cursor:pointer;font-family:inherit">{_LOGIN_I} Log In</button>
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
          <a href="/flights.py"     class="drop-item" style="display:flex;align-items:center;gap:8px" onclick="{'return true' if user else 'openSigninGate();return false'};">{_PLANE} Flights</a>
          <a href="/weather.py"     class="drop-item" style="display:flex;align-items:center;gap:8px" onclick="{'return true' if user else 'openSigninGate();return false'};">{_SUN} Weather</a>
          <a href="/attractions.py" class="drop-item" style="display:flex;align-items:center;gap:8px" onclick="{'return true' if user else 'openSigninGate();return false'};">{_PIN} Tourist Attractions</a>
          <a href="/restaurants.py" class="drop-item" style="display:flex;align-items:center;gap:8px" onclick="{'return true' if user else 'openSigninGate();return false'};">{_FORK} Restaurants</a>
          <a href="/guides.py"      class="drop-item" style="display:flex;align-items:center;gap:8px" onclick="{'return true' if user else 'openSigninGate();return false'};">{_USERS} Tour Guides</a>
          <a href="/transport.py"   class="drop-item" style="display:flex;align-items:center;gap:8px" onclick="{'return true' if user else 'openSigninGate();return false'};">{_TRUCK} Transportation</a>
          <a href="/itinerary.py"   class="drop-item" style="display:flex;align-items:center;gap:8px" onclick="{'return true' if user else 'openSigninGate();return false'};">{_CAL} Itinerary</a>
        </div>
      </div>
      <a href="/about.py" class="nav-link {na('about')}">About Us</a>
    </div>
    {auth_html}
  </div>
</nav>
<div class="tiles-bar">
  <div class="tiles-inner">
    <a href="/flights.py"     class="tile {ta('flights')}"     onclick="{'return true' if user else 'openSigninGate();return false'};"><span class="tile-icon">{_PLANE}</span><span class="tile-lbl">Flight Search</span></a>
    <a href="/attractions.py" class="tile {ta('attractions')}" onclick="{'return true' if user else 'openSigninGate();return false'};"><span class="tile-icon">{_PIN}</span><span class="tile-lbl">Tourist Attractions</span></a>
    <a href="/restaurants.py" class="tile {ta('restaurants')}" onclick="{'return true' if user else 'openSigninGate();return false'};"><span class="tile-icon">{_FORK}</span><span class="tile-lbl">Restaurants</span></a>
    <a href="/guides.py"      class="tile {ta('guides')}"      onclick="{'return true' if user else 'openSigninGate();return false'};"><span class="tile-icon">{_USERS}</span><span class="tile-lbl">Tour Guide Booking</span></a>
    <a href="/weather.py"     class="tile {ta('weather')}"     onclick="{'return true' if user else 'openSigninGate();return false'};"><span class="tile-icon">{_SUN}</span><span class="tile-lbl">Weather Forecast</span></a>
    <a href="/transport.py"   class="tile {ta('transport')}"   onclick="{'return true' if user else 'openSigninGate();return false'};"><span class="tile-icon">{_TRUCK}</span><span class="tile-lbl">Transportation</span></a>
  </div>
</div>

<!-- Sign-in Gate Modal -->
<div id="signin-gate" style="display:none;position:fixed;inset:0;z-index:99999;align-items:center;justify-content:center;background:rgba(0,0,0,.50);backdrop-filter:blur(4px)">
  <div style="background:#fff;border-radius:20px;padding:36px 36px 28px;max-width:400px;width:92%;box-shadow:0 24px 60px rgba(0,0,0,.2);position:relative">
    <button onclick="closeSigninGate()" style="position:absolute;top:14px;right:16px;background:none;border:none;font-size:22px;color:#9CA3AF;cursor:pointer;line-height:1">&times;</button>

    <!-- Header -->
    <div style="text-align:center;margin-bottom:6px">
      <img src="/ATLAS_LOGO.jpg" style="width:36px;height:36px;border-radius:50%;object-fit:cover;display:inline-block;margin-bottom:14px"/>
      <div style="font-size:22px;font-weight:900;color:#0F172A;margin-bottom:6px">Log in or sign up</div>
      <div style="font-size:13px;color:#94A3B8;margin-bottom:22px">Access flights, attractions, restaurants, guides and more.</div>
    </div>

    <!-- Google button -->
    <a href="/auth/google" style="display:flex;align-items:center;justify-content:center;gap:10px;width:100%;padding:12px;border:1.5px solid #E2E8F0;border-radius:100px;background:#fff;font-size:14px;font-weight:600;color:#1F2937;text-decoration:none;box-sizing:border-box;margin-bottom:10px"
       onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='#fff'">
      <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/><path fill="none" d="M0 0h48v48H0z"/></svg>
      Continue with Google
    </a>

    <!-- OR divider -->
    <div style="display:flex;align-items:center;gap:10px;margin:16px 0">
      <div style="flex:1;height:1px;background:#E2E8F0"></div>
      <span style="font-size:12px;color:#94A3B8;letter-spacing:.5px">OR</span>
      <div style="flex:1;height:1px;background:#E2E8F0"></div>
    </div>

    <!-- Email input -->
    <div id="gate-error" style="display:none;background:#FEE2E2;border:1px solid #FECACA;border-radius:8px;padding:10px 13px;color:#991B1B;font-size:13px;margin-bottom:12px"></div>
    <input id="gate-email" type="email" placeholder="Email address" autocomplete="email"
      style="width:100%;padding:13px 16px;border:1.5px solid #E2E8F0;border-radius:100px;font-size:14px;color:#0F172A;outline:none;background:#F8FAFC;font-family:inherit;box-sizing:border-box;margin-bottom:10px"
      onfocus="this.style.borderColor='#0038A8';this.style.background='#fff'" onblur="this.style.borderColor='#E2E8F0';this.style.background='#F8FAFC'"
      onkeydown="if(event.key==='Enter')submitGateLogin()"/>
    <button onclick="submitGateLogin()"
      style="width:100%;padding:13px;background:#0F172A;color:#fff;border:none;border-radius:100px;font-size:15px;font-weight:700;cursor:pointer;font-family:inherit">
      Continue
    </button>

    <!-- Footer links -->
    <div style="margin-top:20px;text-align:center;font-size:12px;color:#94A3B8">
      <a href="#" style="color:#94A3B8;text-decoration:underline;margin:0 6px">Terms of Use</a>|<a href="#" style="color:#94A3B8;text-decoration:underline;margin:0 6px">Privacy Policy</a>
    </div>
  </div>
</div>
{body_content}
<div id="toast"></div>
<footer class="site-footer" id="about">
  <div class="footer-top">
    <div class="footer-brand">
      <div class="footer-logo">
        <img src="/ATLAS_LOGO.jpg" alt="ATLAS" style="width:30px;height:30px;border-radius:50%;object-fit:cover;"/>
        <span style="font-size:18px;font-weight:900;color:#0038A8">ATLAS</span>
      </div>
      <p style="font-size:13px;color:#9CA3AF;max-width:220px;line-height:1.6;margin-top:8px">Your all-in-one Luzon Travel Companion — discover attractions, book guides, search flights, and plan your perfect trip.</p>
    </div>
    <div class="footer-cols">
      <div class="footer-col">
        <div class="footer-col-hdr">The Company</div>
        <a href="/">Home</a>
        <a href="#about">About Us</a>
        <a href="/register.py">Tourist Register</a>
        <a href="/guide/register">Tour Guide Register</a>
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
        <div class="footer-contact"><strong>Location:</strong><br>Luzon, Philippines</div>
        <div class="footer-contact"><strong>Email:</strong><br><a href="mailto:travelatatlas2026@gmail.com" style="color:#9CA3AF;text-decoration:underline">travelatatlas2026@gmail.com</a></div>
      </div>
    </div>
  </div>

  <div class="footer-bottom"><span>&copy; 2026 ATLAS. All Rights Reserved.</span></div>
</footer>
<script>
var ATLAS_LOGGED_IN = {'true' if user else 'false'};
var ATLAS_CSRF = '{csrf_token}';
function openSigninGate(){{var g=document.getElementById('signin-gate');if(g){{g.style.display='flex';document.body.style.overflow='hidden';setTimeout(function(){{var el=document.getElementById('gate-email');if(el)el.focus();}},100);}}}}
function closeSigninGate(){{var g=document.getElementById('signin-gate');if(g){{g.style.display='none';document.body.style.overflow='';document.getElementById('gate-email').value='';var err=document.getElementById('gate-error');err.style.display='none';err.textContent='';}}}}
function submitGateLogin(){{
  var email=document.getElementById('gate-email').value.trim();
  var err=document.getElementById('gate-error');
  if(!email){{err.style.display='block';err.textContent='Please enter your email address.';return;}}
  err.style.display='none';
  var form=document.createElement('form');
  form.method='post';form.action='/login/email';
  var fe=document.createElement('input');fe.type='hidden';fe.name='email';fe.value=email;form.appendChild(fe);
  if(typeof ATLAS_CSRF!=='undefined'){{var fc=document.createElement('input');fc.type='hidden';fc.name='csrf_token';fc.value=ATLAS_CSRF;form.appendChild(fc);}}
  document.body.appendChild(form);form.submit();
}}
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeSigninGate();}});
function toggleDrop(){{document.getElementById('cat-drop').classList.toggle('open');}}
document.addEventListener('click',function(e){{var d=document.getElementById('cat-drop');if(d&&!d.contains(e.target))d.classList.remove('open');var g=document.getElementById('signin-gate');if(g&&e.target===g)closeSigninGate();}});
// openBookingModal, closeBooking, confirmBooking are defined per-page (e.g. guides.py) and must not be overridden here
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.style.display='block';setTimeout(function(){{t.style.display='none';}},2800);}}
</script>
</body>
</html>"""
