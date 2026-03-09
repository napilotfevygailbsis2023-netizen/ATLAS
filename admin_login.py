import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import admin_db

def render(error=""):
    err = f'<div style="background:rgba(239,68,68,.15);border:1px solid rgba(239,68,68,.4);border-radius:8px;padding:10px 14px;color:#FCA5A5;font-size:13px;margin-bottom:14px">{error}</div>' if error else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>ATLAS Admin Login</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',sans-serif;min-height:100vh;background:#0F172A;display:flex;align-items:center;justify-content:center}}
.card{{background:#1E293B;border:1px solid #334155;border-radius:20px;padding:44px 40px;width:100%;max-width:380px;box-shadow:0 32px 80px rgba(0,0,0,.5)}}
.logo{{display:flex;align-items:center;gap:10px;margin-bottom:8px}}
.logo-box{{width:38px;height:38px;background:linear-gradient(135deg,#0038A8,#CE1126);border-radius:10px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:18px}}
.logo-text{{font-size:20px;font-weight:900;color:#fff}}
.badge{{background:rgba(239,68,68,.15);color:#F87171;font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px;border:1px solid rgba(239,68,68,.3);margin-bottom:28px;display:inline-block}}
h2{{font-size:22px;font-weight:800;color:#F1F5F9;margin-bottom:6px}}
p{{font-size:13px;color:#64748B;margin-bottom:28px}}
label{{display:block;font-size:11px;font-weight:700;color:#94A3B8;margin-bottom:5px;text-transform:uppercase;letter-spacing:.5px}}
input{{width:100%;background:#0F172A;border:1.5px solid #334155;border-radius:8px;padding:11px 14px;color:#F1F5F9;font-size:14px;outline:none;margin-bottom:16px;font-family:inherit}}
input:focus{{border-color:#3B82F6}}
.btn{{width:100%;background:linear-gradient(135deg,#0038A8,#1D4ED8);color:#fff;border:none;border-radius:8px;padding:13px;font-weight:700;font-size:15px;cursor:pointer;font-family:inherit;margin-top:4px}}
.btn:hover{{filter:brightness(1.15)}}
.back{{display:block;text-align:center;margin-top:18px;font-size:12px;color:#475569;text-decoration:none}}
.back:hover{{color:#94A3B8}}
.divider{{height:1px;background:#1E293B;margin:20px 0}}
</style>
</head>
<body>
<div class="card">
  <div class="logo">
    <div class="logo-box">A</div>
    <span class="logo-text">ATLAS</span>
  </div>
  <div class="badge">&#128274; Admin Portal</div>
  <h2>Welcome back</h2>
  <p>Sign in to the ATLAS admin dashboard</p>
  {err}
  <form method="post" action="/admin/login">
    <label>Username</label>
    <input type="text" name="username" placeholder="admin" required autocomplete="off"/>
    <label>Password</label>
    <input type="password" name="password" placeholder="••••••••" required/>
    <button class="btn" type="submit">Sign In &#8594;</button>
  </form>
  <a class="back" href="/">&#8592; Back to ATLAS</a>
</div>
</body>
</html>"""

def handle_post(form):
    username = form.get("username","")
    password = form.get("password","")
    if not username or not password:
        return None, render("Please fill in all fields.")
    token = admin_db.admin_login(username, password)
    if token:
        return token, None
    return None, render("Invalid username or password.")
