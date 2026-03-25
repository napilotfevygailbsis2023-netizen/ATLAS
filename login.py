import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db

def _shell(right_content, error="", success=""):
    err = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:10px;padding:10px 14px;color:#DC2626;font-size:13px;margin-bottom:18px;display:flex;align-items:center;gap:8px">&#9888; {error}</div>' if error else ""
    suc = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:10px;padding:10px 14px;color:#065F46;font-size:13px;margin-bottom:18px;display:flex;align-items:center;gap:8px">&#10003; {success}</div>' if success else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Log In - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{min-height:100vh;display:flex;flex-direction:row;font-family:'Segoe UI',sans-serif;background:#F8F4EF}}
.split-left{{width:55%;background:linear-gradient(160deg,#003087 0%,#0038A8 60%,#001a5e 100%);position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 48px;overflow:hidden;min-height:100vh}}
.blob1{{position:absolute;width:400px;height:400px;border-radius:50%;background:rgba(255,255,255,.07);top:-80px;left:-80px}}
.blob2{{position:absolute;width:300px;height:300px;border-radius:50%;background:rgba(255,255,255,.05);bottom:-60px;right:-60px}}
.split-left-content{{position:relative;z-index:2;text-align:center;color:#fff}}
.split-right{{width:45%;flex-shrink:0;background:linear-gradient(160deg,#F0F4FF 0%,#fff 35%);display:flex;flex-direction:column;justify-content:center;padding:52px 48px;min-height:100vh;overflow-y:auto}}
.tab-row{{display:flex;background:#F3F4F6;border-radius:12px;padding:4px;margin-bottom:32px}}
.tab{{flex:1;padding:10px;text-align:center;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;text-decoration:none;color:#6B7280;transition:.2s}}
.tab.active{{background:#fff;color:#1F2937;box-shadow:0 1px 4px rgba(0,0,0,.1)}}
.field{{margin-bottom:18px}}
.field label{{display:block;font-size:12px;font-weight:700;color:#374151;margin-bottom:6px;text-transform:uppercase;letter-spacing:.5px}}
.field input{{width:100%;padding:13px 16px;border:1.5px solid #E5E7EB;border-radius:10px;font-size:14px;color:#1F2937;outline:none;transition:.2s;background:#F9FAFB}}
.field input:focus{{border-color:#0038A8;background:#fff;box-shadow:0 0 0 3px rgba(0,56,168,.08)}}
.submit-btn{{width:100%;padding:14px;background:#0038A8;color:#fff;border:none;border-radius:12px;font-size:15px;font-weight:700;cursor:pointer;letter-spacing:.3px;margin-top:4px}}
.submit-btn:hover{{opacity:.92}}
.divider{{display:flex;align-items:center;gap:12px;margin:20px 0;color:#9CA3AF;font-size:13px}}
.divider::before,.divider::after{{content:'';flex:1;height:1px;background:#E5E7EB}}
.back-link{{position:fixed;top:20px;left:20px;display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.15);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.3);color:#fff;text-decoration:none;padding:8px 16px;border-radius:30px;font-size:13px;font-weight:600;z-index:999}}
@media(max-width:700px){{.split-left{{display:none}}.split-right{{width:100%}}}}
</style>
</head>
<body>
<a href="/" class="back-link">&#8592; Tourist Site</a>
<div class="split-left">
  <div class="blob1"></div>
  <div class="blob2"></div>
  <div class="split-left-content">
    <div style="font-size:72px;margin-bottom:20px">&#127963;</div>
    <div style="font-size:36px;font-weight:900;line-height:1.2;margin-bottom:14px">Explore.<br/>Discover.<br/>Adventure.</div>
    <div style="font-size:15px;opacity:.8;line-height:1.8;margin-bottom:32px;max-width:300px">Your Luzon travel companion for flights, attractions, restaurants and guided tours.</div>
    <div style="display:flex;flex-direction:column;gap:10px;font-size:14px;opacity:.9">
      <div style="display:flex;align-items:center;gap:10px"><span style="display:inline-flex;align-items:center"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13"/><path d="M22 2L15 22 11 13 2 9l20-7z"/></svg></span> Real-time flight search</div>
      <div style="display:flex;align-items:center;gap:10px"><span style="display:inline-flex;align-items:center"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></span> Tourist attraction guides</div>
      <div style="display:flex;align-items:center;gap:10px"><span style="display:inline-flex;align-items:center"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span> Verified local tour guides</div>
      <div style="display:flex;align-items:center;gap:10px"><span style="display:inline-flex;align-items:center"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg></span> Live weather forecasts</div>
    </div>
  </div>
</div>
<div class="split-right">
  <div style="margin-bottom:28px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
      <img src="/ATLAS_LOGO.jpg" alt="ATLAS" style="width:32px;height:32px;border-radius:50%;object-fit:cover;flex-shrink:0"/>
      <span style="font-weight:900;font-size:18px;color:#1F2937">ATLAS</span>
    </div>
    <div style="font-size:13px;color:#6B7280">Luzon Travel Companion</div>
  </div>
  <div class="tab-row">
    <a href="/login.py" class="tab active">Log In</a>
    <a href="/register.py" class="tab">Create Account</a>
  </div>
  <div style="font-size:22px;font-weight:800;color:#1F2937;margin-bottom:6px">Welcome back!</div>
  <div style="font-size:14px;color:#6B7280;margin-bottom:24px">Sign in to your ATLAS account</div>
  {err}{suc}
  {right_content}
  <div style="text-align:center;margin-top:24px;font-size:13px;color:#6B7280">
    Don't have an account? <a href="/register.py" style="color:#0038A8;font-weight:700">Sign Up</a>
  </div>
</div>
</body>
</html>"""

def render(error="", success=""):
    form = """
    <form method="post" action="/login.py" style="display:flex;flex-direction:column;gap:0">
      <div class="field">
        <label>Email Address</label>
        <input type="email" name="email" placeholder="you@email.com" required/>
      </div>
      <div class="field">
        <label>Password</label>
        <input type="password" name="password" placeholder="Enter your password" required/>
      </div>
      <button class="submit-btn" type="submit">Log In &#8594;</button>
    </form>"""
    return _shell(form, error, success)

def handle_post(form_data):
    email    = form_data.get("email","").strip()
    password = form_data.get("password","").strip()
    if not email or not password:
        return None, render("Please fill in all fields.")
    ok, token, user = db.login_user(email, password)
    if ok is True:
        return token, None
    if ok == "suspended":
        return None, render("Your account has been suspended. Please contact support.")
    return None, render("Invalid email or password.")#DC2626