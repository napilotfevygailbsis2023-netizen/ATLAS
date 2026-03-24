import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db


def render(error="", success=""):
    err = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:8px;padding:12px 16px;color:#991B1B;font-size:13px;margin-bottom:16px;">⚠️ {error}</div>' if error else ""
    suc = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:8px;padding:12px 16px;color:#065F46;font-size:13px;margin-bottom:16px;">✅ {success}</div>' if success else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
    <title>Register - ATLAS</title>
    <link rel="stylesheet" href="/css/styles.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
</head>
<body class="auth-split-body">
<a href="/" class="back-link"><i class="fa-solid fa-arrow-left"></i> Tourist Site</a>

<div class="split-left">
  <div class="blob1"></div>
  <div class="blob2"></div>
  <div style="position:relative;z-index:2;text-align:center;color:#fff">
    <div style="font-size:72px;margin-bottom:20px"><i class="fa-solid fa-earth-asia"></i></div>
    <div style="font-size:28px;font-weight:800;line-height:1.2;margin-bottom:14px">Join ATLAS<br/>Today!</div>
    <p style="font-size:15px;opacity:.8;line-height:1.8;margin-bottom:32px;max-width:300px">Create your free account and start planning your perfect Luzon adventure.</p>

    <div style="display:flex;flex-direction:column;gap:12px;text-align:left">
      <div class="feature-pill">
          <div style="font-weight:700">Itinerary Planner</div>
          <div style="font-size:12px;opacity:.8">Build your custom day-by-day plan</div>
      </div>
      <div class="feature-pill">
          <div style="font-weight:700">Book Tour Guides</div>
          <div style="font-size:12px;opacity:.8">Connect with verified local guides</div>
      </div>
    </div>
  </div>
</div>

<div class="split-right">
  <div style="margin-bottom:24px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
      <img src="/ATLAS_LOGO.jpg" style="width:32px;height:32px;border-radius:50%;object-fit:cover;"/>
      <span style="font-weight:800;font-size:18px;color:#1F2937">ATLAS</span>
    </div>
  </div>

  <div class="tab-row">
    <a href="/login.py" class="tab">Log In</a>
    <a href="/register.py" class="tab active">Create Account</a>
  </div>

  <h2 style="font-size:22px;font-weight:800;color:#1F2937;margin-bottom:6px">Create your account</h2>
  <p style="font-size:14px;color:#475569;margin-bottom:22px">Start your Luzon adventure today — it's free!</p>

  {err}{suc}

  <form method="post" action="/register.py">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
      <div class="field"><label>First Name</label><input name="fname" placeholder="Juan" required/></div>
      <div class="field"><label>Last Name</label><input name="lname" placeholder="Dela Cruz" required/></div>
    </div>
    <div class="field"><label>Email Address</label><input type="email" name="email" placeholder="you@email.com" required/></div>
    <div class="field"><label>Password</label><input type="password" name="password" placeholder="Min. 6 characters" required/></div>
    <div class="field"><label>Confirm Password</label><input type="password" name="password2" placeholder="Repeat password" required/></div>
    <button class="submit-btn" type="submit">Create Account <i class="fa-solid fa-arrow-right"></i></button>
  </form>

  <p style="text-align:center;margin-top:20px;font-size:13px;color:#475569">
    Already have an account? <a href="/login.py" style="color:#0038A8;font-weight:700">Log In</a>
  </p>
</div>
</body>
</html>"""


def handle_post(form_data):
    # (Registration logic stays the same)
    pass