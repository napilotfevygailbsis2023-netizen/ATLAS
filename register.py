import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db

def render(error="", success=""):
    err = f'<div style="background:rgba(206,17,38,.15);border:1px solid rgba(206,17,38,.4);border-radius:6px;padding:9px 12px;color:#ffaaaa;font-size:13px;margin-bottom:10px">{error}</div>' if error else ""
    suc = f'<div style="background:rgba(6,95,70,.3);border:1px solid rgba(6,95,70,.5);border-radius:6px;padding:9px 12px;color:#6EE7B7;font-size:13px;margin-bottom:10px">{success}</div>' if success else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Sign Up - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<style>
body{{margin:0;min-height:100vh;background:#0d1b2a;display:flex;align-items:center;justify-content:center;padding:24px}}
.wrap{{display:flex;width:100%;max-width:720px;border-radius:16px;overflow:hidden;box-shadow:0 24px 70px rgba(0,0,0,.5)}}
.left{{flex:1;background:url('https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=900&q=80') center/cover;position:relative;min-height:480px;display:flex;flex-direction:column;justify-content:flex-end;padding:28px}}
.left-overlay{{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.78),rgba(0,0,0,.08))}}
.left-text{{position:relative;z-index:1}}
.left-text h2{{font-size:30px;font-weight:900;color:#fff;text-transform:uppercase;line-height:1.15;margin-bottom:8px}}
.left-text p{{color:rgba(255,255,255,.65);font-size:12px;line-height:1.7;margin-bottom:16px;max-width:220px}}
.learn{{border:1.5px solid #fff;color:#fff;border-radius:30px;padding:7px 20px;font-size:12px;font-weight:700;background:transparent;cursor:pointer;font-family:inherit}}
.right{{width:290px;flex-shrink:0;background:#1565C0;display:flex;flex-direction:column;justify-content:center;padding:28px 24px}}
.brand{{display:flex;align-items:center;gap:8px;margin-bottom:14px}}
.brand-box{{width:28px;height:28px;border-radius:7px;background:linear-gradient(135deg,#0038A8,#CE1126);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:13px}}
.title{{color:#fff;font-size:18px;font-weight:700;margin-bottom:14px}}
label{{display:block;font-size:11px;font-weight:600;color:rgba(255,255,255,.6);margin-bottom:3px}}
input{{width:100%;background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.2);border-radius:6px;padding:8px 11px;color:#fff;font-size:13px;outline:none;margin-bottom:10px;font-family:inherit;box-sizing:border-box}}
input::placeholder{{color:rgba(255,255,255,.35)}}
input:focus{{border-color:#90CAF9;background:rgba(255,255,255,.2)}}
.name-row{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.hint{{font-size:10px;color:rgba(255,255,255,.35);margin:-6px 0 8px}}
.sbtn{{width:100%;background:#CE1126;color:#fff;border:none;border-radius:6px;padding:11px;font-weight:700;font-size:14px;cursor:pointer;margin-bottom:10px;font-family:inherit}}
.sbtn:hover{{filter:brightness(1.15)}}
.sep{{display:flex;align-items:center;gap:8px;margin:6px 0}}
.sep::before,.sep::after{{content:'';flex:1;height:1px;background:rgba(255,255,255,.18)}}
.sep span{{font-size:11px;color:rgba(255,255,255,.38)}}
.alt{{width:100%;background:transparent;border:1.5px solid rgba(255,255,255,.28);color:#fff;border-radius:6px;padding:8px;font-size:12px;font-weight:600;cursor:pointer;font-family:inherit}}
.foot{{text-align:center;font-size:11px;color:rgba(255,255,255,.4);margin-top:10px}}
.foot a{{color:rgba(255,255,255,.75);text-decoration:underline}}
@media(max-width:600px){{.left{{display:none}}.right{{width:100%}}}}
</style>
</head>
<body>
<a href="/" style="position:fixed;top:18px;left:18px;z-index:999;display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.15);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.25);color:#fff;text-decoration:none;padding:8px 14px;border-radius:30px;font-size:13px;font-weight:600">&#8592; Back</a>
<div class="wrap">
  <div class="left">
    <div class="left-overlay"></div>
    <div class="left-text">
      <h2>Join<br>ATLAS</h2>
      <p>Create your free account and start planning your perfect Luzon adventure.</p>
      <a href="/"><button class="learn">Explore First</button></a>
    </div>
  </div>
  <div class="right">
    <div class="brand">
      <div class="brand-box">A</div>
      <span style="font-weight:800;color:#fff;font-size:13px">ATLAS travel</span>
    </div>
    <div class="title">Create Account</div>
    {err}{suc}
    <form method="post" action="/register.py">
      <div class="name-row">
        <div><label>First Name *</label><input type="text" name="fname" placeholder="Juan" required/></div>
        <div><label>Last Name *</label><input type="text" name="lname" placeholder="Cruz" required/></div>
      </div>
      <label>Email *</label>
      <input type="email" name="email" placeholder="you@example.com" required/>
      <label>Password *</label>
      <input type="password" name="password" placeholder="Min. 8 characters" required/>
      <div class="hint">Minimum 8 characters</div>
      <label>Confirm Password *</label>
      <input type="password" name="confirm" placeholder="Repeat password" required/>
      <button class="sbtn" type="submit">Create Account &#8594;</button>
    </form>
    <div class="sep"><span>or</span></div>
    <a href="/login.py"><button class="alt">Sign In Instead</button></a>
    <div class="foot">Have account? <a href="/login.py">Log In</a></div>
  </div>
</div>
</body>
</html>"""

def handle_post(form_data):
    fname   = form_data.get("fname","").strip()
    lname   = form_data.get("lname","").strip()
    email   = form_data.get("email","").strip()
    pw      = form_data.get("password","")
    confirm = form_data.get("confirm","")
    if not all([fname, lname, email, pw, confirm]):
        return False, render(error="Please fill in all fields.")
    if len(pw) < 8:
        return False, render(error="Password must be at least 8 characters.")
    if pw != confirm:
        return False, render(error="Passwords do not match.")
    ok, msg = db.register_user(fname, lname, email, pw)
    if ok:
        return True, render(success="Account created! <a href='/login.py' style='color:#6EE7B7;font-weight:700'>Log In now</a>")
    return False, render(error=msg)
