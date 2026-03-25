import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import admin_db

def render(error="", success=""):
    err = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:8px;padding:12px 16px;color:#991B1B;font-size:13px;margin-bottom:16px;display:flex;align-items:center;gap:8px"><i class="fa-solid fa-triangle-exclamation"></i> {error}</div>' if error else ""
    suc = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:8px;padding:12px 16px;color:#065F46;font-size:13px;margin-bottom:16px;display:flex;align-items:center;gap:8px"><i class="fa-solid fa-check"></i> {success}</div>' if success else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Admin Login - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{min-height:100vh;display:flex;flex-direction:row;font-family:'Segoe UI',sans-serif;}}
.split-left{{width:55%;background:linear-gradient(160deg,#0f2a4a 0%,#1E3A5F 60%,#0a1c30 100%);position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 48px;overflow:hidden;min-height:100vh}}
.blob1{{position:absolute;width:420px;height:420px;border-radius:50%;background:rgba(255,255,255,.05);top:-100px;left:-80px}}
.blob2{{position:absolute;width:280px;height:280px;border-radius:50%;background:rgba(255,255,255,.04);bottom:-60px;right:-40px}}
.split-right{{width:45%;flex-shrink:0;background:linear-gradient(180deg,#F0F4FF 0%,#fff 40%);display:flex;flex-direction:column;justify-content:center;padding:52px 48px;min-height:100vh;overflow-y:auto}}
.field{{margin-bottom:18px}}
.field label{{display:block;font-size:11.5px;font-weight:700;color:#475569;margin-bottom:6px;text-transform:uppercase;letter-spacing:.4px}}
.field input{{width:100%;padding:13px 16px;border:1.5px solid #E2E8F0;border-radius:10px;font-size:14px;color:#0F172A;outline:none;background:#F9FAFB;transition:.15s;font-family:inherit}}
.field input:focus{{border-color:#1E3A5F;background:#fff;box-shadow:0 0 0 3px rgba(30,58,95,.1)}}
.submit-btn{{width:100%;padding:14px;background:#1E3A5F;color:#fff;border:none;border-radius:12px;font-size:15px;font-weight:700;cursor:pointer;margin-top:4px;font-family:inherit;display:flex;align-items:center;justify-content:center;gap:8px;transition:.15s}}
.submit-btn:hover{{background:#274d7a}}
.back-link{{position:fixed;top:20px;left:20px;display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.12);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.2);color:#fff;text-decoration:none;padding:8px 16px;border-radius:20px;font-size:13px;font-weight:600;z-index:999}}
.feature-pill{{display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.09);padding:12px 16px;border-radius:12px;font-size:13px}}
@media(max-width:700px){{.split-left{{display:none}}.split-right{{width:100%}}}}
</style>
</head>
<body>
<a href="/" class="back-link">&#8592; Tourist Site</a>
<div class="split-left">
  <div class="blob1"></div><div class="blob2"></div>
  <div style="position:relative;z-index:2;text-align:center;color:#fff">
    <div style="margin-bottom:20px">
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="opacity:.9"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
    </div>
    <div style="font-size:30px;font-weight:900;line-height:1.2;margin-bottom:12px">ATLAS<br/>Admin Panel</div>
    <div style="font-size:14px;opacity:.7;line-height:1.8;margin-bottom:32px;max-width:300px">Manage tourists, attractions, restaurants, tour guides and transportation routes.</div>
    <div style="display:flex;flex-direction:column;gap:10px;text-align:left">
      <div class="feature-pill">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        Manage tourist accounts
      </div>
      <div class="feature-pill">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="22" x2="21" y2="22"/><line x1="6" y1="18" x2="6" y2="11"/><line x1="10" y1="18" x2="10" y2="11"/><line x1="14" y1="18" x2="14" y2="11"/><line x1="18" y1="18" x2="18" y2="11"/><polygon points="12 2 20 7 4 7"/></svg>
        Add attractions &amp; restaurants
      </div>
      <div class="feature-pill">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M20 21a8 8 0 1 0-16 0"/><path d="M12 12v9"/></svg>
        Manage tour guides
      </div>
      <div class="feature-pill">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="13" rx="2"/><path d="M3 11h18"/><circle cx="7" cy="17" r="1"/><circle cx="17" cy="17" r="1"/></svg>
        Transportation routes
      </div>
    </div>
  </div>
</div>
<div class="split-right">
  <div style="margin-bottom:28px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
      <img src="/ATLAS_LOGO.jpg" alt="ATLAS" style="width:34px;height:34px;border-radius:50%;object-fit:cover;flex-shrink:0"/>
      <span style="font-weight:900;font-size:18px;color:#0F172A">ATLAS Admin</span>
    </div>
    <div style="font-size:13px;color:#94A3B8">Restricted access — authorized personnel only</div>
  </div>
  <div style="display:inline-flex;align-items:center;gap:8px;background:#FEF3C7;border:1px solid #FDE68A;color:#92400E;padding:8px 14px;border-radius:8px;font-size:13px;font-weight:600;margin-bottom:28px">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
    Admin Portal
  </div>
  <div style="font-size:22px;font-weight:800;color:#0F172A;margin-bottom:6px">Welcome back</div>
  <div style="font-size:13px;color:#94A3B8;margin-bottom:24px">Sign in to the ATLAS admin dashboard</div>
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
    <button class="submit-btn" type="submit">
      Sign In
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
    </button>
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
