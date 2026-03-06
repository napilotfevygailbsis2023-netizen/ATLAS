import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def render(error=""):
    err = f'<div style="background:rgba(206,17,38,.15);border:1px solid rgba(206,17,38,.4);border-radius:6px;padding:9px 12px;color:#ffaaaa;font-size:13px;margin-bottom:12px">{error}</div>' if error else ""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Log In - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<style>
body{margin:0;min-height:100vh;background:#0d1b2a;display:flex;align-items:center;justify-content:center;padding:24px}
.wrap{display:flex;width:100%;max-width:720px;border-radius:16px;overflow:hidden;box-shadow:0 24px 70px rgba(0,0,0,.5)}
.left{flex:1;background:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=900&q=80') center/cover;position:relative;min-height:440px;display:flex;flex-direction:column;justify-content:flex-end;padding:28px}
.left-overlay{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.78),rgba(0,0,0,.08))}
.left-text{position:relative;z-index:1}
.left-text h2{font-size:30px;font-weight:900;color:#fff;text-transform:uppercase;line-height:1.15;margin-bottom:8px}
.left-text p{color:rgba(255,255,255,.65);font-size:12px;line-height:1.7;margin-bottom:16px;max-width:220px}
.learn{border:1.5px solid #fff;color:#fff;border-radius:30px;padding:7px 20px;font-size:12px;font-weight:700;background:transparent;cursor:pointer;font-family:inherit}
.right{width:290px;flex-shrink:0;background:#1565C0;display:flex;flex-direction:column;justify-content:center;padding:36px 26px}
.brand{display:flex;align-items:center;gap:8px;margin-bottom:18px}
.brand-box{width:28px;height:28px;border-radius:7px;background:linear-gradient(135deg,#0038A8,#CE1126);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:13px}
.title{color:#fff;font-size:20px;font-weight:700;margin-bottom:18px}
label{display:block;font-size:11px;font-weight:600;color:rgba(255,255,255,.6);margin-bottom:4px}
input{width:100%;background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.2);border-radius:6px;padding:9px 12px;color:#fff;font-size:13px;outline:none;margin-bottom:12px;font-family:inherit;box-sizing:border-box}
input::placeholder{color:rgba(255,255,255,.35)}
input:focus{border-color:#90CAF9;background:rgba(255,255,255,.2)}
.sbtn{width:100%;background:#1976D2;color:#fff;border:none;border-radius:6px;padding:11px;font-weight:700;font-size:14px;cursor:pointer;margin-bottom:12px;font-family:inherit}
.sbtn:hover{filter:brightness(1.15)}
.sep{display:flex;align-items:center;gap:8px;margin:8px 0}
.sep::before,.sep::after{content:'';flex:1;height:1px;background:rgba(255,255,255,.18)}
.sep span{font-size:11px;color:rgba(255,255,255,.38)}
.alt{width:100%;background:transparent;border:1.5px solid rgba(255,255,255,.28);color:#fff;border-radius:6px;padding:9px;font-size:12px;font-weight:600;cursor:pointer;font-family:inherit}
.foot{text-align:center;font-size:11px;color:rgba(255,255,255,.4);margin-top:10px}
.foot a{color:rgba(255,255,255,.75);text-decoration:underline}
@media(max-width:600px){.left{display:none}.right{width:100%}}
</style>
</head>
<body>
<div class="wrap">
  <div class="left">
    <div class="left-overlay"></div>
    <div class="left-text">
      <h2>Enjoy the<br>World</h2>
      <p>Discover the beauty of Luzon - flights, weather, attractions and more.</p>
      <a href="/"><button class="learn">Learn More</button></a>
    </div>
  </div>
  <div class="right">
    <div class="brand">
      <div class="brand-box">A</div>
      <span style="font-weight:800;color:#fff;font-size:13px">ATLAS travel</span>
    </div>
    <div class="title">Sign In</div>
    """ + err + """
    <form method="post" action="/login.py">
      <label>Email *</label>
      <input type="email" name="email" placeholder="you@example.com" required/>
      <label>Password *</label>
      <input type="password" name="password" placeholder="Password" required/>
      <button class="sbtn" type="submit">Continue</button>
    </form>
    <div class="sep"><span>or</span></div>
    <a href="/register.py"><button class="alt">Create Account</button></a>
    <div class="foot">No account? <a href="/register.py">Sign Up</a></div>
  </div>
</div>
</body>
</html>"""
