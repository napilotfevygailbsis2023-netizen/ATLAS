import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db

def render(error="", success=""):
    err = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:8px;padding:12px 16px;color:#991B1B;font-size:13px;margin-bottom:16px"><i class="fa-solid fa-triangle-exclamation"></i> {error}</div>' if error else ""
    suc = f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:8px;padding:12px 16px;color:#065F46;font-size:13px;margin-bottom:16px"><i class="fa-solid fa-check"></i> {success}</div>' if success else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Register - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{min-height:100vh;display:flex;flex-direction:row;font-family:'Segoe UI',sans-serif;background:#F8FAFC}}
.split-left{{width:55%;flex-shrink:0;background:linear-gradient(160deg,#003087 0%,#0038A8 60%,#001a5e 100%);position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 48px;overflow:hidden;min-height:100vh}}
.blob1{{position:absolute;width:400px;height:400px;border-radius:50%;background:rgba(255,255,255,.07);top:-80px;left:-80px}}
.blob2{{position:absolute;width:300px;height:300px;border-radius:50%;background:rgba(255,255,255,.05);bottom:-60px;right:-60px}}
.split-right{{width:45%;flex-shrink:0;background:linear-gradient(160deg,#F0F4FF 0%,#fff 35%);display:flex;flex-direction:column;justify-content:center;padding:52px 48px;min-height:100vh;overflow-y:auto}}
.tab-row{{display:flex;background:#F3F4F6;border-radius:12px;padding:4px;margin-bottom:32px}}
.tab{{flex:1;padding:10px;text-align:center;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none;color:#6B7280;transition:.2s}}
.tab.active{{background:#fff;color:#1F2937;box-shadow:0 1px 4px rgba(0,0,0,.1)}}
.field{{margin-bottom:16px}}
.field label{{display:block;font-size:11.5px;font-weight:700;color:#475569;margin-bottom:6px;text-transform:uppercase;letter-spacing:.4px}}
.field input{{width:100%;padding:12px 14px;border:1.5px solid #E2E8F0;border-radius:8px;font-size:14px;color:#0F172A;outline:none;background:#F8FAFC;transition:.15s;font-family:inherit}}
.field input:focus{{border-color:#0038A8;background:#fff;box-shadow:0 0 0 3px rgba(0,56,168,.08)}}
.submit-btn{{width:100%;padding:13px;background:#0038A8;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer;margin-top:4px;font-family:inherit;transition:.15s}}
.submit-btn:hover{{background:#0050D0}}
.back-link{{position:fixed;top:20px;left:20px;display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.12);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.2);color:#fff;text-decoration:none;padding:8px 16px;border-radius:20px;font-size:13px;font-weight:600;z-index:999}}
.feature-pill{{display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.08);padding:12px 16px;border-radius:10px;color:#fff;font-size:13px}}
@media(max-width:700px){{.split-left{{display:none}}.split-right{{width:100%}}}}
</style>
</head>
<body>
<a href="/" class="back-link"><i class="fa-solid fa-arrow-left"></i> Tourist Site</a>
<div class="split-left">
  <div class="blob1"></div><div class="blob2"></div>
  <div style="position:relative;z-index:2;text-align:center;color:#fff">
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
  <div style="margin-bottom:24px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
      <img src="/ATLAS_LOGO.jpg" alt="ATLAS" style="width:32px;height:32px;border-radius:50%;object-fit:cover;flex-shrink:0"/>
      <span style="font-weight:800;font-size:18px;color:#0F172A">ATLAS</span>
    </div>
    <div style="font-size:13px;color:#94A3B8">Luzon Travel Companion</div>
  </div>
  <div class="tab-row">
    <a href="/login.py" class="tab">Log In</a>
    <a href="/register.py" class="tab active">Create Account</a>
  </div>
  <div style="font-size:20px;font-weight:800;color:#0F172A;margin-bottom:4px">Create your account</div>
  <div style="font-size:13px;color:#94A3B8;margin-bottom:22px">Start your Luzon adventure — it's free!</div>
  {err}{suc}
  <form method="post" action="/register.py">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
      <div class="field"><label>First Name *</label><input name="fname" placeholder="Juan" required/></div>
      <div class="field"><label>Last Name *</label><input name="lname" placeholder="Dela Cruz" required/></div>
    </div>
    <div class="field"><label>Email Address *</label><input type="email" name="email" placeholder="you@email.com" required/></div>
    <div class="field"><label>Password *</label><input type="password" name="password" placeholder="At least 6 characters" required/></div>
    <div class="field"><label>Confirm Password *</label><input type="password" name="password2" placeholder="Repeat password" required/></div>
    <button class="submit-btn" type="submit"><i class="fa-solid fa-envelope"></i> Create Account &amp; Send Code</button>
  </form>
  <p style="text-align:center;margin-top:18px;font-size:13px;color:#94A3B8">
    Already have an account? <a href="/login.py" style="color:#0038A8;font-weight:700">Log In</a>
  </p>
</div>
</body></html>"""


def render_verify(email, error=""):
    """Step 2: Enter the 6-digit verification code."""
    safe_email = email.replace('"','&quot;')
    err = f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:8px;padding:12px 16px;color:#991B1B;font-size:13px;margin-bottom:16px"><i class="fa-solid fa-triangle-exclamation"></i> {error}</div>' if error else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Verify Email - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{min-height:100vh;display:flex;align-items:center;justify-content:center;background:#F8FAFC;font-family:'Segoe UI',sans-serif;padding:24px}}
.verify-box{{background:#fff;border-radius:16px;padding:40px 48px;max-width:480px;width:100%;box-shadow:0 4px 24px rgba(0,0,0,.08);text-align:center}}
.code-inputs{{display:flex;gap:10px;justify-content:center;margin:28px 0}}
.code-input{{width:52px;height:60px;border:2px solid #E2E8F0;border-radius:10px;font-size:24px;font-weight:800;text-align:center;outline:none;color:#0F172A;font-family:monospace;transition:.15s}}
.code-input:focus{{border-color:#0038A8;box-shadow:0 0 0 3px rgba(0,56,168,.1);background:#F0F7FF}}
.submit-btn{{width:100%;padding:13px;background:#0038A8;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer;font-family:inherit;transition:.15s;margin-top:8px}}
.submit-btn:hover{{background:#0050D0}}
</style>
</head>
<body>
<div class="verify-box">
  <div style="margin-bottom:16px"><i class="fa-solid fa-envelope-circle-check" style="font-size:48px;color:#0038A8"></i></div>
  <div style="font-size:22px;font-weight:800;color:#0F172A;margin-bottom:8px">Check your email</div>
  <div style="font-size:14px;color:#475569;line-height:1.6;margin-bottom:4px">We sent a 6-digit verification code to</div>
  <div style="font-size:14px;font-weight:700;color:#0038A8;margin-bottom:4px">{safe_email}</div>
  <div style="font-size:13px;color:#94A3B8;margin-bottom:8px">Enter the code below to activate your account.</div>
  {err}
  <form method="post" action="/verify" id="verify-form">
    <input type="hidden" name="email" value="{safe_email}"/>
    <input type="hidden" name="code" id="code-hidden"/>
    <div class="code-inputs">
      <input type="text" class="code-input" maxlength="1" inputmode="numeric" pattern="[0-9]" id="c0" autofocus/>
      <input type="text" class="code-input" maxlength="1" inputmode="numeric" pattern="[0-9]" id="c1"/>
      <input type="text" class="code-input" maxlength="1" inputmode="numeric" pattern="[0-9]" id="c2"/>
      <input type="text" class="code-input" maxlength="1" inputmode="numeric" pattern="[0-9]" id="c3"/>
      <input type="text" class="code-input" maxlength="1" inputmode="numeric" pattern="[0-9]" id="c4"/>
      <input type="text" class="code-input" maxlength="1" inputmode="numeric" pattern="[0-9]" id="c5"/>
    </div>
    <button class="submit-btn" type="submit"><i class="fa-solid fa-circle-check"></i> Verify Account</button>
  </form>
  <div style="margin-top:16px;font-size:13px;color:#94A3B8">
    Didn't receive it? Check spam or <a href="/register.py" style="color:#0038A8;font-weight:600">register again</a>.
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
    if (e.key==='ArrowLeft' && idx > 0) inputs[idx-1].focus();
    if (e.key==='ArrowRight' && idx < 5) inputs[idx+1].focus();
  }});
  inp.addEventListener('paste', function(e) {{
    var pasted = (e.clipboardData||window.clipboardData).getData('text').replace(/\\D/g,'');
    if (pasted.length >= 6) {{
      for (var i=0;i<6;i++) inputs[i].value = pasted[i]||'';
      inputs[5].focus();
      e.preventDefault();
    }}
  }});
}});
document.getElementById('verify-form').addEventListener('submit', function(e) {{
  var code = Array.from(inputs).map(function(i){{return i.value;}}).join('');
  if (code.length < 6) {{ e.preventDefault(); alert('Please enter all 6 digits.'); return; }}
  document.getElementById('code-hidden').value = code;
}});
</script>
</body></html>"""


def handle_post(form_data):
    fname    = form_data.get("fname","").strip()
    lname    = form_data.get("lname","").strip()
    email    = form_data.get("email","").strip().lower()
    pw       = form_data.get("password","").strip()
    pw2      = form_data.get("password2","").strip()

    if not all([fname, lname, email, pw]):
        return False, render(error="Please fill in all required fields.")
    if pw != pw2:
        return False, render(error="Passwords do not match.")
    if len(pw) < 6:
        return False, render(error="Password must be at least 6 characters.")
    if db.email_already_registered(email):
        return False, render(error="This email is already registered. Please log in.")

    code = db.store_pending_user(fname, lname, email, pw)
    if not code:
        return False, render(error="Something went wrong. Please try again.")

    try:
        import email_sender
        sent = email_sender.send_verification_email(email, fname, code)
    except Exception:
        sent = False

    if sent:
        return True, render_verify(email)
    else:
        # If email fails, show code on screen for testing
        return True, render_verify(email, error=f"Email failed to send. Your code is: {code} (dev mode)")
