#!/usr/bin/env python3
# ── FILE: register.py ─────────────────────────────────────────────────────────
# Standalone register page — separate URL (/register.py), NOT a modal.
# Same split-panel layout as login.py.

def render(error: str = "") -> str:
    err_html = f'<div style="background:rgba(206,17,38,.15);border:1px solid rgba(206,17,38,.4);border-radius:6px;padding:9px 12px;color:#ffaaaa;font-size:13px;margin-bottom:10px">{error}</div>' if error else ""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Sign Up — ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<style>
  body{margin:0;min-height:100vh;display:flex;flex-direction:column;background:#0d1b2a}
  .auth-page{flex:1;display:flex;align-items:center;justify-content:center;padding:24px}
  .auth-wrap{display:flex;width:100%;max-width:720px;border-radius:16px;overflow:hidden;box-shadow:0 24px 70px rgba(0,0,0,.5);animation:pop .22s ease}
  @keyframes pop{from{transform:scale(.94);opacity:0}to{transform:scale(1);opacity:1}}
  .auth-left{flex:1;background:url('https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=900&q=80') center/cover;position:relative;min-height:480px;display:flex;flex-direction:column;justify-content:flex-end;padding:28px}
  .auth-left-overlay{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.78) 0%,rgba(0,0,0,.08) 65%)}
  .auth-left-text{position:relative;z-index:1}
  .auth-left-text h2{font-size:30px;font-weight:900;color:#fff;text-transform:uppercase;line-height:1.15;margin-bottom:8px}
  .auth-left-text p{color:rgba(255,255,255,.65);font-size:12px;line-height:1.7;margin-bottom:16px;max-width:220px}
  .learn-btn{border:1.5px solid #fff;color:#fff;border-radius:30px;padding:7px 20px;font-size:12px;font-weight:700;background:transparent;cursor:pointer;font-family:inherit}
  .learn-btn:hover{background:#fff;color:#1A1A2E}
  .auth-right{width:290px;flex-shrink:0;background:#1565C0;display:flex;flex-direction:column;justify-content:center;padding:28px 24px}
  .auth-brand{display:flex;align-items:center;gap:8px;margin-bottom:14px}
  .auth-brand-box{width:28px;height:28px;border-radius:7px;background:linear-gradient(135deg,#0038A8,#CE1126);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:13px}
  .auth-brand-name{font-weight:800;color:#fff;font-size:13px}
  .auth-title{color:#fff;font-size:18px;font-weight:700;margin-bottom:14px}
  label.al{display:block;font-size:11px;font-weight:600;color:rgba(255,255,255,.6);margin-bottom:3px}
  input.ai{width:100%;background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.2);border-radius:6px;padding:8px 11px;color:#fff;font-size:13px;outline:none;margin-bottom:10px;font-family:inherit}
  input.ai::placeholder{color:rgba(255,255,255,.35)}
  input.ai:focus{border-color:#90CAF9;background:rgba(255,255,255,.2)}
  .name-row{display:grid;grid-template-columns:1fr 1fr;gap:8px}
  .auth-hint{font-size:10px;color:rgba(255,255,255,.35);margin:-6px 0 8px}
  .auth-btn{width:100%;background:#CE1126;color:#fff;border:none;border-radius:6px;padding:11px;font-weight:700;font-size:14px;cursor:pointer;margin-bottom:10px;font-family:inherit;letter-spacing:.3px}
  .auth-btn:hover{filter:brightness(1.15)}
  .auth-sep{display:flex;align-items:center;gap:8px;margin:6px 0}
  .auth-sep::before,.auth-sep::after{content:'';flex:1;height:1px;background:rgba(255,255,255,.18)}
  .auth-sep span{font-size:11px;color:rgba(255,255,255,.38)}
  .auth-alt{width:100%;background:transparent;border:1.5px solid rgba(255,255,255,.28);color:#fff;border-radius:6px;padding:8px;font-size:12px;font-weight:600;cursor:pointer;font-family:inherit}
  .auth-alt:hover{background:rgba(255,255,255,.1)}
  .auth-foot{text-align:center;font-size:11px;color:rgba(255,255,255,.4);margin-top:10px}
  .auth-foot a{color:rgba(255,255,255,.75);text-decoration:underline}
  @media(max-width:600px){.auth-left{display:none}.auth-right{width:100%}}
</style>
</head>
<body>
<div class="auth-page">
  <div class="auth-wrap">
    <!-- LEFT: photo panel -->
    <div class="auth-left">
      <div class="auth-left-overlay"></div>
      <div class="auth-left-text">
        <h2>Join<br>ATLAS</h2>
        <p>Create your free account and start planning your perfect Luzon adventure today.</p>
        <a href="/"><button class="learn-btn">Explore First</button></a>
      </div>
    </div>
    <!-- RIGHT: form panel -->
    <div class="auth-right">
      <div class="auth-brand">
        <div class="auth-brand-box">A</div>
        <span class="auth-brand-name">ATLAS travel</span>
      </div>
      <div class="auth-title">Create Account</div>
      """ + err_html + """
      <form method="post" action="/register.py">
        <div class="name-row">
          <div><label class="al">First Name *</label><input class="ai" type="text" name="fname" placeholder="Juan" required/></div>
          <div><label class="al">Last Name *</label><input class="ai" type="text" name="lname" placeholder="Cruz" required/></div>
        </div>
        <label class="al">Email *</label>
        <input class="ai" type="email" name="email" placeholder="you@example.com" required/>
        <label class="al">Password *</label>
        <input class="ai" type="password" name="password" placeholder="Min. 8 characters" required/>
        <div class="auth-hint">Minimum 8 characters required</div>
        <label class="al">Confirm Password *</label>
        <input class="ai" type="password" name="confirm" placeholder="Repeat password" required/>
        <button class="auth-btn" type="submit">Continue →</button>
      </form>
      <div class="auth-sep"><span>or</span></div>
      <a href="/login.py"><button class="auth-alt">Sign In Instead</button></a>
      <div class="auth-foot">Already have an account? <a href="/login.py">Sign In</a></div>
    </div>
  </div>
</div>
</body>
</html>"""

if __name__ == "__main__":
    print(render())
