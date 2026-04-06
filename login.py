import sys, os, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db

def e(s): return html.escape(str(s) if s is not None else "")

_STYLE = """
*{box-sizing:border-box;margin:0;padding:0}
body{min-height:100vh;display:flex;flex-direction:row;font-family:'Segoe UI',sans-serif;background:#F8FAFC}
.split-left{width:55%;flex-shrink:0;background:linear-gradient(160deg,#003087 0%,#0038A8 60%,#001a5e 100%);position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 48px;overflow:hidden;min-height:100vh}
.blob1{position:absolute;width:400px;height:400px;border-radius:50%;background:rgba(255,255,255,.07);top:-80px;left:-80px}
.blob2{position:absolute;width:300px;height:300px;border-radius:50%;background:rgba(255,255,255,.05);bottom:-60px;right:-60px}
.split-right{width:45%;flex-shrink:0;background:linear-gradient(160deg,#F0F4FF 0%,#fff 35%);display:flex;flex-direction:column;justify-content:center;padding:52px 48px;min-height:100vh;overflow-y:auto}
.tab-row{display:flex;background:#F3F4F6;border-radius:12px;padding:4px;margin-bottom:32px}
.tab{flex:1;padding:10px;text-align:center;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none;color:#6B7280;transition:.2s}
.tab.active{background:#fff;color:#1F2937;box-shadow:0 1px 4px rgba(0,0,0,.1)}
.field{margin-bottom:16px}
.field label{display:block;font-size:11.5px;font-weight:700;color:#475569;margin-bottom:6px;text-transform:uppercase;letter-spacing:.4px}
.field input{width:100%;padding:12px 14px;border:1.5px solid #E2E8F0;border-radius:8px;font-size:14px;color:#0F172A;outline:none;background:#F8FAFC;transition:.15s;font-family:inherit}
.field input:focus{border-color:#0038A8;background:#fff;box-shadow:0 0 0 3px rgba(0,56,168,.08)}
.submit-btn{width:100%;padding:13px;background:#0038A8;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer;margin-top:4px;font-family:inherit;transition:.15s}
.submit-btn:hover{background:#0050D0}
.back-link{position:fixed;top:20px;left:20px;display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.12);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.2);color:#fff;text-decoration:none;padding:8px 16px;border-radius:20px;font-size:13px;font-weight:600;z-index:999}
@media(max-width:700px){.split-left{display:none}.split-right{width:100%}}
"""

def render(error="", success=""):
    err = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:8px;padding:12px 16px;color:#991B1B;font-size:13px;margin-bottom:16px"><i class="fa-solid fa-triangle-exclamation"></i> {e(error)}</div>' if error else ""
    suc = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:8px;padding:12px 16px;color:#065F46;font-size:13px;margin-bottom:16px"><i class="fa-solid fa-check"></i> {e(success)}</div>' if success else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Log In - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<style>{_STYLE}</style>
</head>
<body>
<a href="/" class="back-link"><i class="fa-solid fa-arrow-left"></i> Tourist Site</a>
<div class="split-left">
  <div class="blob1"></div><div class="blob2"></div>
  <div style="position:relative;z-index:2;text-align:center;color:#fff">
    <div style="font-size:72px;margin-bottom:20px">&#127963;</div>
    <div style="font-size:36px;font-weight:900;line-height:1.2;margin-bottom:14px">Explore.<br/>Discover.<br/>Adventure.</div>
    <div style="font-size:15px;opacity:.8;line-height:1.8;margin-bottom:32px;max-width:300px">Your Luzon travel companion for flights, attractions, restaurants and guided tours.</div>
    <div style="display:flex;flex-direction:column;gap:10px;font-size:14px;opacity:.9;text-align:left">
      <div style="display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.1);padding:10px 16px;border-radius:10px">
        <i class="fa-solid fa-plane" style="width:18px"></i> Real-time flight search
      </div>
      <div style="display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.1);padding:10px 16px;border-radius:10px">
        <i class="fa-solid fa-location-dot" style="width:18px"></i> Tourist attraction guides
      </div>
      <div style="display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.1);padding:10px 16px;border-radius:10px">
        <i class="fa-solid fa-users" style="width:18px"></i> Verified local tour guides
      </div>
      <div style="display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.1);padding:10px 16px;border-radius:10px">
        <i class="fa-solid fa-cloud-sun" style="width:18px"></i> Live weather forecasts
      </div>
    </div>
  </div>
</div>
<div class="split-right">
  <div style="margin-bottom:24px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
      <img src="/ATLAS_LOGO.jpg" alt="ATLAS" style="width:32px;height:32px;border-radius:50%;object-fit:cover;flex-shrink:0"/>
      <span style="font-weight:800;font-size:18px;color:#0F172A">ATLAS</span>
    </div>
    <div style="font-size:13px;color:#94A3B8">Luzon Travel Companion</div>
  </div>
  <div class="tab-row">
    <a href="/login.py" class="tab active">Log In</a>
    <a href="/register.py" class="tab">Create Account</a>
  </div>
  <div style="font-size:20px;font-weight:800;color:#0F172A;margin-bottom:4px">Welcome back</div>
  <div style="font-size:13px;color:#94A3B8;margin-bottom:22px">Sign in to your ATLAS account</div>
  {err}{suc}
  <form method="post" action="/login.py">
    <div class="field"><label>Email Address</label><input type="email" name="email" placeholder="you@email.com" required autocomplete="email"/></div>
    <div class="field"><label>Password</label><input type="password" name="password" placeholder="Enter your password" required/></div>
    <button class="submit-btn" type="submit"><i class="fa-solid fa-right-to-bracket"></i> Log In</button>
  </form>
  <div style="display:flex;align-items:center;gap:10px;margin:18px 0">
    <div style="flex:1;height:1px;background:#E2E8F0"></div>
    <span style="font-size:12px;color:#94A3B8;white-space:nowrap">or continue with</span>
    <div style="flex:1;height:1px;background:#E2E8F0"></div>
  </div>
  <a href="/auth/google" style="display:flex;align-items:center;justify-content:center;gap:10px;width:100%;padding:12px;border:1.5px solid #E2E8F0;border-radius:8px;background:#fff;font-size:14px;font-weight:600;color:#1F2937;text-decoration:none;transition:.15s" onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='#fff'">
    <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/><path fill="none" d="M0 0h48v48H0z"/></svg>
    Continue with Google
  </a>
  <p style="text-align:center;margin-top:18px;font-size:13px;color:#94A3B8">
    Don't have an account? <a href="/register.py" style="color:#0038A8;font-weight:700">Sign Up</a>
  </p>
</div>
</body></html>"""


def render_2fa(email, error=""):
    """Step 2: Enter 6-digit Google Authenticator code."""
    safe_email = e(email)
    err = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:8px;padding:12px 16px;color:#991B1B;font-size:13px;margin-bottom:16px">&#9888; {e(error)}</div>' if error else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Two-Factor Auth - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{min-height:100vh;display:flex;align-items:center;justify-content:center;background:#F8FAFC;font-family:'Segoe UI',sans-serif;padding:24px}}
.box{{background:#fff;border-radius:16px;padding:40px 48px;max-width:480px;width:100%;box-shadow:0 4px 24px rgba(0,0,0,.08);text-align:center}}
.code-inputs{{display:flex;gap:10px;justify-content:center;margin:28px 0}}
.code-input{{width:52px;height:60px;border:2px solid #E2E8F0;border-radius:10px;font-size:24px;font-weight:800;text-align:center;outline:none;color:#0F172A;font-family:monospace;transition:.15s}}
.code-input:focus{{border-color:#0038A8;box-shadow:0 0 0 3px rgba(0,56,168,.1);background:#F0F7FF}}
.submit-btn{{width:100%;padding:13px;background:#0038A8;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer;font-family:inherit;transition:.15s}}
.submit-btn:hover{{background:#0050D0}}
</style>
</head>
<body>
<div class="box">
  <div style="width:64px;height:64px;background:#EFF6FF;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 20px">
    <i class="fa-brands fa-google" style="font-size:28px;color:#0038A8"></i>
  </div>
  <div style="font-size:22px;font-weight:800;color:#0F172A;margin-bottom:8px">Two-Factor Authentication</div>
  <div style="font-size:14px;color:#475569;line-height:1.6;margin-bottom:4px">Open Google Authenticator and enter the 6-digit code for</div>
  <div style="font-size:14px;font-weight:700;color:#0038A8;margin-bottom:16px">{safe_email}</div>
  {err}
  <form method="post" action="/login/2fa" id="tfa-form">
    <input type="hidden" name="email" value="{safe_email}"/>
    <input type="hidden" name="code" id="tfa-code"/>
    <div class="code-inputs">
      <input type="text" class="code-input" maxlength="1" inputmode="numeric" id="t0" autofocus/>
      <input type="text" class="code-input" maxlength="1" inputmode="numeric" id="t1"/>
      <input type="text" class="code-input" maxlength="1" inputmode="numeric" id="t2"/>
      <input type="text" class="code-input" maxlength="1" inputmode="numeric" id="t3"/>
      <input type="text" class="code-input" maxlength="1" inputmode="numeric" id="t4"/>
      <input type="text" class="code-input" maxlength="1" inputmode="numeric" id="t5"/>
    </div>
    <button class="submit-btn" type="submit"><i class="fa-solid fa-shield-halved"></i> Verify</button>
  </form>
  <div style="margin-top:16px;font-size:13px;color:#94A3B8">
    <a href="/login.py" style="color:#0038A8;font-weight:600">&#8592; Back to login</a>
  </div>
</div>
<script>
var inputs = document.querySelectorAll('.code-input');
inputs.forEach(function(inp, idx) {{
  inp.addEventListener('input', function() {{
    this.value = this.value.replace(/[^0-9]/g,'').slice(-1);
    if (this.value && idx < 5) inputs[idx+1].focus();
  }});
  inp.addEventListener('keydown', function(e) {{
    if (e.key==='Backspace' && !this.value && idx > 0) inputs[idx-1].focus();
  }});
  inp.addEventListener('paste', function(e) {{
    var pasted = (e.clipboardData||window.clipboardData).getData('text').replace(/\\D/g,'');
    if (pasted.length >= 6) {{
      for (var i=0;i<6;i++) inputs[i].value = pasted[i]||'';
      inputs[5].focus(); e.preventDefault();
    }}
  }});
}});
document.getElementById('tfa-form').addEventListener('submit', function(e) {{
  var code = Array.from(inputs).map(function(i){{return i.value;}}).join('');
  if (code.length < 6) {{ e.preventDefault(); alert('Please enter all 6 digits.'); return; }}
  document.getElementById('tfa-code').value = code;
}});
</script>
</body></html>"""


def render_2fa_setup(user, secret, qr_b64, error=""):
    """Setup page: scan QR code then confirm with a code."""
    err = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:8px;padding:12px 16px;color:#991B1B;font-size:13px;margin-bottom:16px">&#9888; {e(error)}</div>' if error else ""
    enabled = user.get("totp_enabled", 0)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Setup 2FA - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{min-height:100vh;display:flex;align-items:center;justify-content:center;background:#F8FAFC;font-family:'Segoe UI',sans-serif;padding:24px}}
.box{{background:#fff;border-radius:16px;padding:40px 48px;max-width:520px;width:100%;box-shadow:0 4px 24px rgba(0,0,0,.08)}}
.code-inputs{{display:flex;gap:10px;justify-content:center;margin:20px 0}}
.code-input{{width:48px;height:56px;border:2px solid #E2E8F0;border-radius:10px;font-size:22px;font-weight:800;text-align:center;outline:none;color:#0F172A;font-family:monospace;transition:.15s}}
.code-input:focus{{border-color:#0038A8;box-shadow:0 0 0 3px rgba(0,56,168,.1);background:#F0F7FF}}
.btn{{padding:12px 24px;border:none;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;font-family:inherit}}
</style>
</head>
<body>
<div class="box">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:24px">
    <div style="width:48px;height:48px;background:#EFF6FF;border-radius:50%;display:flex;align-items:center;justify-content:center">
      <i class="fa-brands fa-google" style="font-size:22px;color:#0038A8"></i>
    </div>
    <div>
      <div style="font-size:20px;font-weight:800;color:#0F172A">Google Authenticator</div>
      <div style="font-size:13px;color:#6B7280">Two-factor authentication setup</div>
    </div>
  </div>

  {"" if not enabled else '<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:8px;padding:12px 16px;color:#065F46;font-size:13px;margin-bottom:20px;display:flex;align-items:center;gap:8px"><i class="fa-solid fa-shield-halved"></i> 2FA is currently <strong>enabled</strong> on your account.</div>'}

  {err}

  {"" if enabled else f'''
  <div style="margin-bottom:20px">
    <div style="font-weight:700;color:#1F2937;margin-bottom:8px">Step 1 — Scan this QR code</div>
    <div style="font-size:13px;color:#6B7280;margin-bottom:14px">Open Google Authenticator on your phone and tap the + button, then scan this code.</div>
    <div style="text-align:center;margin-bottom:14px">
      <img src="data:image/png;base64,{qr_b64}" style="width:180px;height:180px;border:4px solid #E2E8F0;border-radius:12px"/>
    </div>
    <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:12px;text-align:center;margin-bottom:20px">
      <div style="font-size:11px;color:#9CA3AF;margin-bottom:4px">Or enter this key manually</div>
      <div style="font-family:monospace;font-size:14px;font-weight:700;color:#0038A8;letter-spacing:2px">{e(secret)}</div>
    </div>
    <div style="font-weight:700;color:#1F2937;margin-bottom:8px">Step 2 — Enter the 6-digit code to confirm</div>
    <form method="post" action="/setup-2fa" id="setup-form">
      <input type="hidden" name="action" value="enable"/>
      <input type="hidden" name="code" id="setup-code"/>
      <div class="code-inputs">
        <input type="text" class="code-input" maxlength="1" inputmode="numeric" id="s0" autofocus/>
        <input type="text" class="code-input" maxlength="1" inputmode="numeric" id="s1"/>
        <input type="text" class="code-input" maxlength="1" inputmode="numeric" id="s2"/>
        <input type="text" class="code-input" maxlength="1" inputmode="numeric" id="s3"/>
        <input type="text" class="code-input" maxlength="1" inputmode="numeric" id="s4"/>
        <input type="text" class="code-input" maxlength="1" inputmode="numeric" id="s5"/>
      </div>
      <button class="btn" type="submit" style="background:#0038A8;color:#fff;width:100%;padding:13px">
        <i class="fa-solid fa-check"></i> Enable Two-Factor Authentication
      </button>
    </form>
  </div>
  '''}

  {"" if not enabled else '''
  <form method="post" action="/setup-2fa">
    <input type="hidden" name="action" value="disable"/>
    <button class="btn" type="submit" style="background:#FEE2E2;color:#DC2626;width:100%;padding:13px"
      onclick="return confirm('Are you sure you want to disable 2FA? This will make your account less secure.')">
      <i class="fa-solid fa-shield-xmark"></i> Disable Two-Factor Authentication
    </button>
  </form>
  '''}

  <div style="margin-top:16px;text-align:center">
    <a href="/profile.py" style="font-size:13px;color:#6B7280">&#8592; Back to Profile</a>
  </div>
</div>
<script>
var inputs = document.querySelectorAll('.code-input');
inputs.forEach(function(inp, idx) {{
  inp.addEventListener('input', function() {{
    this.value = this.value.replace(/[^0-9]/g,'').slice(-1);
    if (this.value && idx < 5) inputs[idx+1].focus();
  }});
  inp.addEventListener('keydown', function(e) {{
    if (e.key==='Backspace' && !this.value && idx > 0) inputs[idx-1].focus();
  }});
}});
var sf = document.getElementById('setup-form');
if (sf) sf.addEventListener('submit', function(e) {{
  var code = Array.from(inputs).map(function(i){{return i.value;}}).join('');
  if (code.length < 6) {{ e.preventDefault(); alert('Please enter all 6 digits.'); return; }}
  document.getElementById('setup-code').value = code;
}});
</script>
</body></html>"""


def handle_post(form):
    """Returns (token_or_None, html_or_None, needs_2fa_email_or_None)."""
    email    = form.get("email","").strip().lower()
    password = form.get("password","").strip()
    if not email or not password:
        return None, render(error="Please fill in all fields."), None
    result, token, user = db.login_user(email, password)
    if result == "suspended":
        return None, render(error="Your account has been suspended. Please contact support."), None
    if not result:
        return None, render(error="Invalid email or password."), None
    # Check if 2FA is enabled
    if user.get("totp_enabled") and user.get("totp_secret"):
        return None, render_2fa(email), email   # signal caller to show 2FA screen
    return token, None, None
