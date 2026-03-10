import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db

def render(error="", success=""):
    err = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:10px;padding:10px 14px;color:#DC2626;font-size:13px;margin-bottom:18px;display:flex;align-items:center;gap:8px">&#9888; {error}</div>' if error else ""
    suc = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:10px;padding:10px 14px;color:#065F46;font-size:13px;margin-bottom:18px;display:flex;align-items:center;gap:8px">&#10003; {success}</div>' if success else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Register - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{min-height:100vh;display:flex;flex-direction:row;font-family:'Segoe UI',sans-serif;background:#F8F4EF}}
.split-left{{width:55%;background:linear-gradient(160deg,#0038A8 0%,#CE1126 60%,#1a1a2e 100%);position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 48px;overflow:hidden;min-height:100vh}}
.blob1{{position:absolute;width:400px;height:400px;border-radius:50%;background:rgba(255,255,255,.07);top:-80px;right:-80px}}
.blob2{{position:absolute;width:300px;height:300px;border-radius:50%;background:rgba(255,255,255,.05);bottom:-60px;left:-60px}}
.split-right{{width:45%;flex-shrink:0;background:linear-gradient(160deg,#FFF0F0 0%,#fff 35%);display:flex;flex-direction:column;justify-content:center;padding:48px;min-height:100vh;overflow-y:auto}}
.tab-row{{display:flex;background:#F3F4F6;border-radius:12px;padding:4px;margin-bottom:28px}}
.tab{{flex:1;padding:10px;text-align:center;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;text-decoration:none;color:#6B7280}}
.tab.active{{background:#fff;color:#1F2937;box-shadow:0 1px 4px rgba(0,0,0,.1)}}
.field{{margin-bottom:16px}}
.field label{{display:block;font-size:12px;font-weight:700;color:#374151;margin-bottom:6px;text-transform:uppercase;letter-spacing:.5px}}
.field input{{width:100%;padding:13px 16px;border:1.5px solid #E5E7EB;border-radius:10px;font-size:14px;color:#1F2937;outline:none;background:#F9FAFB}}
.field input:focus{{border-color:#CE1126;background:#fff;box-shadow:0 0 0 3px rgba(206,17,38,.08)}}
.submit-btn{{width:100%;padding:14px;background:linear-gradient(135deg,#CE1126,#0038A8);color:#fff;border:none;border-radius:12px;font-size:15px;font-weight:700;cursor:pointer;margin-top:4px}}
.back-link{{position:fixed;top:20px;left:20px;display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.15);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.3);color:#fff;text-decoration:none;padding:8px 16px;border-radius:30px;font-size:13px;font-weight:600;z-index:999}}
@media(max-width:700px){{.split-left{{display:none}}.split-right{{width:100%}}}}
</style>
</head>
<body>
<a href="/" class="back-link">&#8592; Tourist Site</a>
<div class="split-left">
  <div class="blob1"></div>
  <div class="blob2"></div>
  <div style="position:relative;z-index:2;text-align:center;color:#fff">
    <div style="font-size:72px;margin-bottom:20px">&#127758;</div>
    <div style="font-size:34px;font-weight:900;line-height:1.2;margin-bottom:14px">Join ATLAS<br/>Today!</div>
    <div style="font-size:15px;opacity:.8;line-height:1.8;margin-bottom:32px;max-width:300px">Create your free account and start planning your perfect Luzon adventure.</div>
    <div style="display:flex;flex-direction:column;gap:12px;font-size:14px;opacity:.9;text-align:left">
      <div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.1);padding:12px 16px;border-radius:12px"><span style="font-size:22px">&#128197;</span><div><div style="font-weight:700">Itinerary Planner</div><div style="font-size:12px;opacity:.8">Build your custom day-by-day plan</div></div></div>
      <div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.1);padding:12px 16px;border-radius:12px"><span style="font-size:22px">&#129517;</span><div><div style="font-weight:700">Book Tour Guides</div><div style="font-size:12px;opacity:.8">Connect with verified local guides</div></div></div>
      <div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.1);padding:12px 16px;border-radius:12px"><span style="font-size:22px">&#9992;</span><div><div style="font-weight:700">Track Flights</div><div style="font-size:12px;opacity:.8">Real-time flight information</div></div></div>
    </div>
  </div>
</div>
<div class="split-right">
  <div style="margin-bottom:24px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
      <div style="width:32px;height:32px;background:linear-gradient(135deg,#CE1126,#0038A8);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:15px">A</div>
      <span style="font-weight:900;font-size:18px;color:#1F2937">ATLAS</span>
    </div>
    <div style="font-size:13px;color:#6B7280">Luzon Travel Companion</div>
  </div>
  <div class="tab-row">
    <a href="/login.py" class="tab">Log In</a>
    <a href="/register.py" class="tab active">Create Account</a>
  </div>
  <div style="font-size:22px;font-weight:800;color:#1F2937;margin-bottom:6px">Create your account</div>
  <div style="font-size:14px;color:#6B7280;margin-bottom:22px">Start your Luzon adventure today — it's free!</div>
  {err}{suc}
  <form method="post" action="/register.py">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
      <div class="field"><label>First Name *</label><input name="fname" placeholder="Juan" required/></div>
      <div class="field"><label>Last Name *</label><input name="lname" placeholder="Dela Cruz" required/></div>
    </div>
    <div class="field"><label>Email Address *</label><input type="email" name="email" placeholder="you@email.com" required/></div>
    <div class="field"><label>Password *</label><input type="password" name="password" placeholder="Create a strong password" required/></div>
    <div class="field"><label>Confirm Password *</label><input type="password" name="password2" placeholder="Repeat your password" required/></div>
    <button class="submit-btn" type="submit">Create Account &#8594;</button>
  </form>
  <div style="text-align:center;margin-top:20px;font-size:13px;color:#6B7280">
    Already have an account? <a href="/login.py" style="color:#CE1126;font-weight:700">Log In</a>
  </div>
</div>
</body>
</html>"""

def handle_post(form_data):
    fname = form_data.get("fname","").strip()
    lname = form_data.get("lname","").strip()
    email = form_data.get("email","").strip()
    pw    = form_data.get("password","").strip()
    pw2   = form_data.get("password2","").strip()
    if not all([fname, lname, email, pw]):
        return False, render(error="Please fill in all required fields.")
    if pw != pw2:
        return False, render(error="Passwords do not match.")
    if len(pw) < 6:
        return False, render(error="Password must be at least 6 characters.")
    ok, msg = db.register_user(fname, lname, email, pw)
    if ok:
        return True, render(success="Account created! You can now log in.")
    return False, render(error=msg)
