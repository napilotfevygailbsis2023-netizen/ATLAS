import sys, os, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db

def e(s): return html.escape(str(s) if s is not None else "")

_STYLE = """
*{box-sizing:border-box;margin:0;padding:0}
body{min-height:100vh;display:flex;align-items:center;justify-content:center;font-family:'Segoe UI',sans-serif;background:#f0f4f8;padding:20px}
.modal{background:#ffffff;border-radius:16px;padding:40px 40px 32px;width:100%;max-width:400px;box-shadow:0 8px 40px rgba(0,0,0,.12)}
.field{margin-bottom:14px;position:relative}
.field input{width:100%;padding:18px 16px 6px;border:1.5px solid #d1d9e0;border-radius:100px;font-size:14px;color:#1a1a2e;outline:none;background:#f8fafc;transition:.15s;font-family:inherit}
.field input:focus{border-color:#1e3a8a;background:#fff}
.field input::placeholder{color:transparent}
.field label{position:absolute;left:16px;top:50%;transform:translateY(-50%);font-size:14px;color:#9ca3af;pointer-events:none;transition:.15s;background:transparent}
.field input:focus ~ label,
.field input:not(:placeholder-shown) ~ label{top:10px;transform:none;font-size:11px;color:#1e3a8a}
.pill-btn{width:100%;padding:13px;border:1.5px solid #d1d9e0;border-radius:100px;font-size:14px;font-weight:500;cursor:pointer;font-family:inherit;transition:.15s;display:flex;align-items:center;justify-content:center;gap:10px;text-decoration:none;background:#fff;color:#1a1a2e;margin-bottom:10px}
.pill-btn:hover{background:#f1f5f9;border-color:#b0bec5}
.submit-btn{width:100%;padding:14px;background:#1a1a2e;color:#fff;border:none;border-radius:100px;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;transition:.15s;margin-top:6px}
.submit-btn:hover{background:#2d2d4e}
.submit-btn:disabled{background:#d1d9e0;color:#9ca3af;cursor:not-allowed}
.divider{display:flex;align-items:center;gap:12px;margin:18px 0}
.divider hr{flex:1;border:none;border-top:1px solid #e2e8f0}
.divider span{font-size:12px;color:#9ca3af}
.req{font-size:13px;color:#6b7280;display:flex;align-items:center;gap:8px;padding:4px 0}
.req.ok{color:#1e3a8a}
.email-chip{display:flex;align-items:center;justify-content:space-between;padding:14px 18px;border:1.5px solid #d1d9e0;border-radius:100px;background:#f8fafc;margin-bottom:14px}
.email-chip span{font-size:14px;color:#374151}
.email-chip a{font-size:13px;color:#1e3a8a;font-weight:600;text-decoration:none}
.footer-links{margin-top:24px;font-size:12px;color:#9ca3af;text-align:center}
.footer-links a{color:#9ca3af;text-decoration:underline;margin:0 8px}
"""

_GOOGLE_SVG = '<svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/><path fill="none" d="M0 0h48v48H0z"/></svg>'

def _page(title, body_html, wide=False):
    max_w = "520px" if wide else "400px"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{title} - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<style>{_STYLE}.modal{{max-width:{max_w}}}</style>
</head>
<body>
<div class="modal">
  <div style="text-align:center;margin-bottom:28px">
    <img src="/ATLAS_LOGO.jpg" alt="ATLAS" style="width:40px;height:40px;border-radius:50%;object-fit:cover;display:inline-block"/>
  </div>
{body_html}
</div>
</body></html>"""

def _err_box(msg):
    if not msg: return ""
    return f'<div style="background:#fef2f2;border:1px solid #fca5a5;border-radius:10px;padding:12px 16px;color:#dc2626;font-size:13px;margin-bottom:16px"><i class="fa-solid fa-triangle-exclamation"></i> {e(msg)}</div>'

def _suc_box(msg):
    if not msg: return ""
    return f'<div style="background:#f0fdf4;border:1px solid #86efac;border-radius:10px;padding:12px 16px;color:#16a34a;font-size:13px;margin-bottom:16px"><i class="fa-solid fa-check"></i> {e(msg)}</div>'


# ── STEP 1: Email entry ───────────────────────────────────────────────────────
def render(error="", success=""):
    body = f"""
  <div style="font-size:28px;font-weight:700;color:#1a1a2e;text-align:center;margin-bottom:8px">Log in or sign up</div>
  <div style="font-size:13px;color:#6b7280;text-align:center;margin-bottom:24px">Access flights, attractions, restaurants and more.</div>
  {_err_box(error)}{_suc_box(success)}
  <a href="/auth/google" class="pill-btn">
    {_GOOGLE_SVG} Continue with Google
  </a>
  <button class="pill-btn" style="opacity:.4;cursor:not-allowed" disabled>
    <i class="fa-brands fa-apple" style="font-size:18px"></i> Continue with Apple
  </button>
  <button class="pill-btn" style="opacity:.4;cursor:not-allowed" disabled>
    <i class="fa-solid fa-phone" style="font-size:16px"></i> Continue with phone
  </button>
  <div class="divider"><hr/><span>OR</span><hr/></div>
  <form method="post" action="/login/email">
    <div class="field">
      <input type="email" name="email" id="email-inp" placeholder="Email address" required autocomplete="email" autofocus/>
      <label for="email-inp">Email address</label>
    </div>
    <button class="submit-btn" type="submit">Continue</button>
  </form>
  <div class="footer-links">
    <a href="#">Terms of Use</a> | <a href="#">Privacy Policy</a>
  </div>"""
    return _page("Log In / Sign Up", body)


# ── STEP 2a: Existing user — enter password ───────────────────────────────────
def render_login_password(email, error=""):
    safe_email = e(email)
    body = f"""
  <div style="font-size:28px;font-weight:700;color:#1a1a2e;text-align:center;margin-bottom:8px">Welcome back</div>
  <div style="font-size:13px;color:#6b7280;text-align:center;margin-bottom:24px">Enter your password to continue</div>
  {_err_box(error)}
  <form method="post" action="/login.py">
    <input type="hidden" name="email" value="{safe_email}"/>
    <div class="email-chip">
      <span>{safe_email}</span>
      <a href="/login.py">Edit</a>
    </div>
    <div class="field">
      <input type="password" name="password" id="pw-inp" placeholder="Password" required autofocus style="padding-right:48px"/>
      <label for="pw-inp">Password</label>
      <button type="button" tabindex="-1"
        onclick="var i=document.getElementById('pw-inp');i.type=i.type==='password'?'text':'password';this.querySelector('i').className=i.type==='password'?'fa-regular fa-eye':'fa-regular fa-eye-slash'"
        style="position:absolute;right:16px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:#9ca3af;padding:0">
        <i class="fa-regular fa-eye"></i>
      </button>
    </div>
    <button class="submit-btn" type="submit">Continue</button>
  </form>
  <div class="footer-links">
    <a href="#">Terms of Use</a> | <a href="#">Privacy Policy</a>
  </div>"""
    return _page("Log In", body)


# ── STEP 2b: New user — create password ──────────────────────────────────────
def render_signup_password(email, error=""):
    safe_email = e(email)
    body = f"""
  <div style="font-size:28px;font-weight:700;color:#1a1a2e;text-align:center;margin-bottom:8px">Create a password</div>
  <div style="font-size:13px;color:#6b7280;text-align:center;margin-bottom:24px">You'll use this to log in to ATLAS.</div>
  {_err_box(error)}
  <form method="post" action="/signup/password" id="pw-form">
    <input type="hidden" name="email" value="{safe_email}"/>
    <div class="email-chip">
      <span>{safe_email}</span>
      <a href="/login.py">Edit</a>
    </div>
    <div class="field">
      <input type="password" name="password" id="pw-input" placeholder="Password"
             required autofocus style="padding-right:48px" oninput="checkPw(this.value)"/>
      <label for="pw-input">Password</label>
      <button type="button" tabindex="-1"
        onclick="var i=document.getElementById('pw-input');i.type=i.type==='password'?'text':'password';this.querySelector('i').className=i.type==='password'?'fa-regular fa-eye':'fa-regular fa-eye-slash'"
        style="position:absolute;right:16px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:#9ca3af;padding:0">
        <i class="fa-regular fa-eye"></i>
      </button>
    </div>
    <div style="background:#f8fafc;border:1.5px solid #d1d9e0;border-radius:12px;padding:14px 18px;margin-bottom:16px">
      <div style="font-size:12px;font-weight:600;color:#374151;margin-bottom:8px">Your password must contain:</div>
      <div id="req-len" class="req"><i class="fa-solid fa-xmark" style="width:14px;color:#d1d9e0"></i> At least 12 characters</div>
    </div>
    <button class="submit-btn" type="submit" id="pw-btn" disabled>Continue</button>
  </form>
  <div class="footer-links">
    <a href="#">Terms of Use</a> | <a href="#">Privacy Policy</a>
  </div>
<script>
function checkPw(v) {{
  var len = v.length >= 12;
  var el = document.getElementById('req-len');
  el.className = 'req' + (len ? ' ok' : '');
  el.innerHTML = (len
    ? '<i class="fa-solid fa-check" style="width:14px;color:#1e3a8a"></i> At least 12 characters'
    : '<i class="fa-solid fa-xmark" style="width:14px;color:#d1d9e0"></i> At least 12 characters');
  document.getElementById('pw-btn').disabled = !len;
}}
</script>"""
    return _page("Create Password", body)


# ── STEP 3: Check your inbox ──────────────────────────────────────────────────
def render_verify_email(email, error=""):
    safe_email = e(email)
    body = f"""
  <div style="font-size:28px;font-weight:700;color:#1a1a2e;text-align:center;margin-bottom:8px">Check your inbox</div>
  <div style="font-size:13px;color:#6b7280;text-align:center;line-height:1.7;margin-bottom:24px">
    Enter the verification code we just sent to<br/>
    <strong style="color:#1a1a2e">{safe_email}</strong>
  </div>
  {_err_box(error)}
  <form method="post" action="/signup/verify">
    <input type="hidden" name="email" value="{safe_email}"/>
    <div class="field">
      <input type="text" name="code" id="code-inp" placeholder="Code"
             required autofocus maxlength="6" inputmode="numeric"
             autocomplete="one-time-code"
             style="letter-spacing:6px;font-size:20px;font-weight:600;text-align:center;padding:18px 16px 6px"/>
      <label for="code-inp" style="left:50%;transform:translate(-50%,-50%);white-space:nowrap">Code</label>
    </div>
    <button class="submit-btn" type="submit">Continue</button>
  </form>
  <div style="margin-top:16px;text-align:center">
    <form method="post" action="/signup/resend" style="display:inline">
      <input type="hidden" name="email" value="{safe_email}"/>
      <button type="submit"
        style="background:none;border:none;color:#1a1a2e;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;text-decoration:underline">
        Resend email
      </button>
    </form>
  </div>
  <div class="footer-links">
    <a href="#">Terms of Use</a> | <a href="#">Privacy Policy</a>
  </div>"""
    return _page("Verify Email", body)


# ── STEP 4: Complete registration (name + age) ────────────────────────────────
def render_register_complete(email, google_name="", error=""):
    safe_email = e(email)
    safe_name  = e(google_name)
    parts = safe_name.split()
    fname = parts[0] if parts else ""
    lname = " ".join(parts[1:]) if len(parts) > 1 else ""
    body = f"""
  <div style="font-size:28px;font-weight:700;color:#1a1a2e;text-align:center;margin-bottom:8px">How old are you?</div>
  <div style="font-size:13px;color:#6b7280;text-align:center;margin-bottom:24px;line-height:1.7">
    This helps us personalise your experience and provide<br/>the right settings, in line with our
    <a href="#" style="color:#1e3a8a;text-decoration:underline">Privacy Policy</a>.
  </div>
  {_err_box(error)}
  <form method="post" action="/auth/google/complete">
    <input type="hidden" name="email" value="{safe_email}"/>
    <div class="field">
      <input type="text" name="fullname" id="fullname-inp" placeholder="Full name"
             value="{(fname + ' ' + lname).strip()}"
             required maxlength="120" autocomplete="name"/>
      <label for="fullname-inp">Full name</label>
    </div>
    <div class="field">
      <input type="number" name="age" id="age-inp" placeholder="Age" min="13" max="120" required/>
      <label for="age-inp">Age</label>
    </div>
    <div style="font-size:12px;color:#9ca3af;text-align:center;margin-bottom:16px;line-height:1.7">
      By clicking "Finish creating account", you agree to our
      <a href="#" style="color:#1e3a8a;text-decoration:underline">Terms</a> and have read our
      <a href="#" style="color:#1e3a8a;text-decoration:underline">Privacy Policy</a>.
    </div>
    <button class="submit-btn" type="submit">Finish creating account</button>
  </form>"""
    return _page("Complete Registration", body)


# ── 2FA entry screen ──────────────────────────────────────────────────────────
def render_2fa(email, error=""):
    safe_email = e(email)
    err = _err_box(error)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Two-Factor Auth - ATLAS</title>
<link rel="stylesheet" href="/css/styles.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<style>{_STYLE}</style>
</head>
<body>
<div class="modal" style="text-align:center">
  <div style="width:56px;height:56px;background:#f1f5f9;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;border:1.5px solid #d1d9e0">
    <i class="fa-brands fa-google" style="font-size:24px;color:#6b7280"></i>
  </div>
  <div style="font-size:22px;font-weight:700;color:#1a1a2e;margin-bottom:8px">Two-Factor Authentication</div>
  <div style="font-size:13px;color:#6b7280;line-height:1.6;margin-bottom:4px">Open Google Authenticator and enter the 6-digit code for</div>
  <div style="font-size:14px;font-weight:600;color:#1a1a2e;margin-bottom:16px">{safe_email}</div>
  {err}
  <form method="post" action="/login/2fa">
    <input type="hidden" name="email" value="{safe_email}"/>
    <div class="field" style="text-align:left">
      <input type="text" name="code" id="tfa-inp" placeholder="6-digit code"
             required maxlength="6" inputmode="numeric" autofocus
             autocomplete="one-time-code"
             style="letter-spacing:6px;font-size:20px;font-weight:600;text-align:center;padding:18px 16px 6px"/>
      <label for="tfa-inp" style="left:50%;transform:translate(-50%,-50%);white-space:nowrap">Code</label>
    </div>
    <button class="submit-btn" type="submit">Verify</button>
  </form>
  <div style="margin-top:16px">
    <a href="/login.py" style="font-size:13px;color:#6b7280">&#8592; Back to login</a>
  </div>
  <div class="footer-links">
    <a href="#">Terms of Use</a> | <a href="#">Privacy Policy</a>
  </div>
</div>
</body></html>"""


def render_2fa_setup(user, secret, qr_b64, error=""):
    err = _err_box(error)
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
body{{min-height:100vh;display:flex;align-items:center;justify-content:center;background:#f0f4f8;font-family:'Segoe UI',sans-serif;padding:24px}}
.box{{background:#ffffff;border-radius:16px;padding:40px 48px;max-width:520px;width:100%;box-shadow:0 8px 40px rgba(0,0,0,.12)}}
.field{{margin-bottom:14px;position:relative}}
.field input{{width:100%;padding:18px 16px 6px;border:1.5px solid #d1d9e0;border-radius:100px;font-size:14px;color:#1a1a2e;outline:none;background:#f8fafc;transition:.15s;font-family:inherit}}
.field input:focus{{border-color:#1e3a8a;background:#fff}}
.field input::placeholder{{color:transparent}}
.field label{{position:absolute;left:16px;top:50%;transform:translateY(-50%);font-size:14px;color:#9ca3af;pointer-events:none;transition:.15s}}
.field input:focus ~ label,.field input:not(:placeholder-shown) ~ label{{top:10px;transform:none;font-size:11px;color:#1e3a8a}}
.btn{{padding:12px 24px;border:none;border-radius:100px;font-size:14px;font-weight:600;cursor:pointer;font-family:inherit}}
</style>
</head>
<body>
<div class="box">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:24px">
    <div style="width:48px;height:48px;background:#f1f5f9;border-radius:50%;display:flex;align-items:center;justify-content:center;border:1.5px solid #d1d9e0">
      <i class="fa-brands fa-google" style="font-size:22px;color:#6b7280"></i>
    </div>
    <div>
      <div style="font-size:20px;font-weight:700;color:#1a1a2e">Google Authenticator</div>
      <div style="font-size:13px;color:#6b7280">Two-factor authentication setup</div>
    </div>
  </div>
  {"" if not enabled else '<div style="background:#f0fdf4;border:1px solid #86efac;border-radius:10px;padding:12px 16px;color:#16a34a;font-size:13px;margin-bottom:20px;display:flex;align-items:center;gap:8px"><i class="fa-solid fa-shield-halved"></i> 2FA is currently <strong>enabled</strong> on your account.</div>'}
  {err}
  {"" if enabled else f'''
  <div>
    <div style="font-weight:600;color:#374151;margin-bottom:8px">Step 1 &mdash; Scan this QR code</div>
    <div style="font-size:13px;color:#6b7280;margin-bottom:14px">Open Google Authenticator on your phone, tap +, then scan.</div>
    <div style="text-align:center;margin-bottom:14px">
      <img src="data:image/png;base64,{qr_b64}" style="width:180px;height:180px;border:2px solid #d1d9e0;border-radius:12px"/>
    </div>
    <div style="background:#f8fafc;border:1px solid #d1d9e0;border-radius:10px;padding:12px;text-align:center;margin-bottom:20px">
      <div style="font-size:11px;color:#9ca3af;margin-bottom:4px">Or enter this key manually</div>
      <div style="font-family:monospace;font-size:14px;font-weight:700;color:#374151;letter-spacing:2px">{e(secret)}</div>
    </div>
    <div style="font-weight:600;color:#374151;margin-bottom:8px">Step 2 &mdash; Enter the 6-digit code to confirm</div>
    <form method="post" action="/setup-2fa">
      <input type="hidden" name="action" value="enable"/>
      <div class="field">
        <input type="text" name="code" id="setup-inp" placeholder="Code"
               maxlength="6" inputmode="numeric" autofocus
               style="letter-spacing:6px;font-size:20px;font-weight:600;text-align:center;padding:18px 16px 6px"/>
        <label for="setup-inp" style="left:50%;transform:translate(-50%,-50%);white-space:nowrap">Code</label>
      </div>
      <button class="btn" type="submit" style="background:#1a1a2e;color:#fff;width:100%;padding:13px">
        <i class="fa-solid fa-check"></i> Enable Two-Factor Authentication
      </button>
    </form>
  </div>
  '''}
  {"" if not enabled else '''
  <form method="post" action="/setup-2fa">
    <input type="hidden" name="action" value="disable"/>
    <button class="btn" type="submit" style="background:#fef2f2;color:#dc2626;width:100%;padding:13px;border:1.5px solid #fca5a5"
      onclick="return confirm(\'Are you sure you want to disable 2FA?\')">
      <i class="fa-solid fa-shield-xmark"></i> Disable Two-Factor Authentication
    </button>
  </form>
  '''}
  <div style="margin-top:16px;text-align:center">
    <a href="/profile.py" style="font-size:13px;color:#6b7280">&#8592; Back to Profile</a>
  </div>
</div>
</body></html>"""


def handle_post(form):
    """Returns (token_or_None, html_or_None, needs_2fa_email_or_None)."""
    email    = form.get("email","").strip().lower()
    password = form.get("password","").strip()
    if not email or not password:
        return None, render(error="Please fill in all fields."), None
    result, token, user = db.login_user(email, password)
    if result == "suspended":
        return None, render_login_password(email, error="Your account has been suspended. Please contact support."), None
    if not result:
        return None, render_login_password(email, error="Incorrect password. Please try again."), None
    if user.get("totp_enabled") and user.get("totp_secret"):
        return None, render_2fa(email), email
    return token, None, None
