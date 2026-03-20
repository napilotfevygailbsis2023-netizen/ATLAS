import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import admin_db

def render(error="", success=""):
    err = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:10px;padding:10px 14px;color:#DC2626;font-size:13px;margin-bottom:18px">&#9888; {error}</div>' if error else ""
    suc = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:10px;padding:10px 14px;color:#065F46;font-size:13px;margin-bottom:18px">&#10003; {success}</div>' if success else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Admin Login - ATLAS</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{min-height:100vh;display:flex;flex-direction:row;font-family:'Segoe UI',sans-serif}}
.split-left{{width:55%;background:linear-gradient(160deg,#0F172A 0%,#1E3A5F 50%,#0038A8 100%);position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 48px;overflow:hidden;min-height:100vh}}
.blob1{{position:absolute;width:420px;height:420px;border-radius:50%;background:rgba(255,255,255,.05);top:-100px;left:-80px}}
.blob2{{position:absolute;width:300px;height:300px;border-radius:50%;background:rgba(0,56,168,.3);bottom:-60px;right:-40px}}
.split-right{{width:45%;flex-shrink:0;background:linear-gradient(160deg,#EFF6FF 0%,#fff 35%);display:flex;flex-direction:column;justify-content:center;padding:52px 48px;min-height:100vh;overflow-y:auto}}
.field{{margin-bottom:18px}}
.field label{{display:block;font-size:12px;font-weight:700;color:#374151;margin-bottom:6px;text-transform:uppercase;letter-spacing:.5px}}
.field input{{width:100%;padding:13px 16px;border:1.5px solid #E5E7EB;border-radius:10px;font-size:14px;color:#1F2937;outline:none;background:#F9FAFB}}
.field input:focus{{border-color:#0038A8;background:#fff;box-shadow:0 0 0 3px rgba(0,56,168,.08)}}
.submit-btn{{width:100%;padding:14px;background:linear-gradient(135deg,#0F172A,#0038A8);color:#fff;border:none;border-radius:12px;font-size:15px;font-weight:700;cursor:pointer;margin-top:4px}}
.submit-btn:hover{{opacity:.92}}
.back-link{{position:fixed;top:20px;left:20px;display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.12);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.25);color:#fff;text-decoration:none;padding:8px 16px;border-radius:30px;font-size:13px;font-weight:600;z-index:999}}
@media(max-width:700px){{.split-left{{display:none}}.split-right{{width:100%}}}}
</style>
</head>
<body>
<a href="/" class="back-link">&#8592; Tourist Site</a>
<div class="split-left">
  <div class="blob1"></div><div class="blob2"></div>
  <div style="position:relative;z-index:2;text-align:center;color:#fff">
    <div style="font-size:72px;margin-bottom:20px">&#9881;</div>
    <div style="font-size:34px;font-weight:900;line-height:1.2;margin-bottom:14px">ATLAS<br/>Admin Panel</div>
    <div style="font-size:15px;opacity:.75;line-height:1.8;margin-bottom:36px;max-width:300px">Manage tourists, attractions, restaurants, tour guides and transportation routes.</div>
    <div style="display:flex;flex-direction:column;gap:10px;font-size:14px;opacity:.9;text-align:left">
      <div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.08);padding:12px 16px;border-radius:12px"><span style="font-size:20px">&#128100;</span> Manage tourist accounts</div>
      <div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.08);padding:12px 16px;border-radius:12px"><span style="font-size:20px">&#127963;</span> Add attractions & restaurants</div>
      <div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.08);padding:12px 16px;border-radius:12px"><span style="font-size:20px">&#129517;</span> Manage tour guides</div>
      <div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.08);padding:12px 16px;border-radius:12px"><span style="font-size:20px">&#128652;</span> Transportation routes</div>
    </div>
  </div>
</div>
<div class="split-right">
  <div style="margin-bottom:32px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
      <img src="/ATLAS_LOGO.jpg" alt="ATLAS" style="width:32px;height:32px;border-radius:50%;object-fit:cover;flex-shrink:0"/>
      <span style="font-weight:900;font-size:18px;color:#1F2937">ATLAS Admin</span>
    </div>
    <div style="font-size:13px;color:#6B7280">Restricted access — authorized personnel only</div>
  </div>
  <div style="display:inline-flex;align-items:center;gap:8px;background:#FEF3C7;border:1px solid #FDE68A;color:#92400E;padding:8px 14px;border-radius:10px;font-size:13px;font-weight:600;margin-bottom:28px">
    &#128274; Admin Portal
  </div>
  <div style="font-size:24px;font-weight:800;color:#1F2937;margin-bottom:6px">Welcome back</div>
  <div style="font-size:14px;color:#6B7280;margin-bottom:28px">Sign in to the ATLAS admin dashboard</div>
  {err}{suc}
  <form method="post" action="/admin/login">
    <div class="field">
      <label>Username</label>
      <input type="text" name="username" placeholder="admin" required autocomplete="off"/>
    </div>
    <div class="field">
      <label>Password</label>
      <input type="password" name="password" placeholder="Enter your password" required/>
    </div>
    <button class="submit-btn" type="submit">Sign In &#8594;</button>
  </form>
</div>
</body>
</html>"""

def handle_post(form):
    username = form.get("username","").strip()
    password = form.get("password","").strip()
    if not username or not password:
        return None, render("Please fill in all fields.")
    token = admin_db.admin_login(username, password)
    if token:
        return token, None
    return None, render("Invalid username or password.")
