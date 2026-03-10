import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
import guide_db

CITIES = ["Manila","Baguio","Tagaytay","Vigan","Ilocos Norte","Batangas","Albay","Pangasinan","Bataan"]

def handle_login(form):
    email = form.get("email","").strip()
    pw    = form.get("password","").strip()
    if not email or not pw:
        return None, None, "Please fill in all fields."
    ok, token, guide = guide_db.login_guide(email, pw)
    if ok:
        return token, guide, None
    return None, None, "Invalid email or password."

def handle_register(form):
    fname = form.get("fname","").strip()
    lname = form.get("lname","").strip()
    email = form.get("email","").strip()
    pw    = form.get("password","").strip()
    pw2   = form.get("password2","").strip()
    phone = form.get("phone","").strip()
    city  = form.get("city","Manila")
    if not all([fname, lname, email, pw, phone]):
        return False, "Please fill in all required fields."
    if pw != pw2:
        return False, "Passwords do not match."
    if len(pw) < 6:
        return False, "Password must be at least 6 characters."
    return guide_db.register_guide(fname, lname, email, pw, phone, city)

def render(mode="login", error="", success=""):
    city_opts = "".join(f'<option>{c}</option>' for c in CITIES)

    login_form = f"""
    <form method="post" action="/guide_login.py" style="display:flex;flex-direction:column;gap:14px">
      <input type="hidden" name="action" value="login"/>
      {"" if not error else f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:8px;padding:10px;color:#DC2626;font-size:13px">&#9888; {error}</div>'}
      {"" if not success else f'<div style="background:#D1FAE5;border:1px solid #A7F3D0;border-radius:8px;padding:10px;color:#065F46;font-size:13px">&#10003; {success}</div>'}
      <div>
        <label class="lbl">Email Address</label>
        <input class="inp" type="email" name="email" placeholder="yourname@email.com" required style="width:100%"/>
      </div>
      <div>
        <label class="lbl">Password</label>
        <input class="inp" type="password" name="password" placeholder="Enter password" required style="width:100%"/>
      </div>
      <button class="btn" type="submit" style="background:#6B21A8;color:#fff;padding:12px;font-size:15px;font-weight:700">Log In as Tour Guide</button>
      <div style="text-align:center;font-size:13px;color:#6B7280">
        Don't have an account? <a href="/guide_login.py?mode=register" style="color:#6B21A8;font-weight:700">Register here</a>
      </div>
    </form>"""

    register_form = f"""
    <form method="post" action="/guide_login.py" style="display:flex;flex-direction:column;gap:12px">
      <input type="hidden" name="action" value="register"/>
      {"" if not error else f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:8px;padding:10px;color:#DC2626;font-size:13px">&#9888; {error}</div>'}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
        <div><label class="lbl">First Name *</label><input class="inp" name="fname" placeholder="Juan" required style="width:100%"/></div>
        <div><label class="lbl">Last Name *</label><input class="inp" name="lname" placeholder="Dela Cruz" required style="width:100%"/></div>
      </div>
      <div><label class="lbl">Email Address *</label><input class="inp" type="email" name="email" placeholder="juan@email.com" required style="width:100%"/></div>
      <div><label class="lbl">Phone Number *</label><input class="inp" name="phone" placeholder="09XX-XXX-XXXX" required style="width:100%"/></div>
      <div><label class="lbl">City / Area *</label><select class="inp" name="city" style="width:100%">{city_opts}</select></div>
      <div><label class="lbl">Password *</label><input class="inp" type="password" name="password" placeholder="Min. 6 characters" required style="width:100%"/></div>
      <div><label class="lbl">Confirm Password *</label><input class="inp" type="password" name="password2" placeholder="Repeat password" required style="width:100%"/></div>
      <button class="btn" type="submit" style="background:#6B21A8;color:#fff;padding:12px;font-size:15px;font-weight:700">Create Guide Account</button>
      <div style="text-align:center;font-size:13px;color:#6B7280">
        Already have an account? <a href="/guide_login.py" style="color:#6B21A8;font-weight:700">Log in here</a>
      </div>
    </form>"""

    active_form = register_form if mode == "register" else login_form
    title_text  = "Create Guide Account" if mode == "register" else "Tour Guide Login"
    subtitle    = "Join ATLAS as a verified tour guide" if mode == "register" else "Welcome back, Tour Guide!"

    body = f"""
    <div style="min-height:80vh;display:flex;align-items:center;justify-content:center;padding:40px 16px">
      <div style="display:grid;grid-template-columns:1fr 1fr;max-width:900px;width:100%;border-radius:20px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.15)">
        <!-- Left panel -->
        <div style="background:linear-gradient(160deg,#6B21A8,#0038A8);padding:40px;display:flex;flex-direction:column;justify-content:center;color:#fff">
          <div style="font-size:48px;margin-bottom:16px">&#129517;</div>
          <div style="font-size:26px;font-weight:900;margin-bottom:10px">ATLAS Tour Guides</div>
          <div style="font-size:14px;opacity:.85;line-height:1.7;margin-bottom:24px">
            Join our network of verified local guides across Luzon. Share your knowledge, earn income, and help tourists discover the Philippines.
          </div>
          <div style="display:flex;flex-direction:column;gap:10px">
            <div style="display:flex;align-items:center;gap:10px;font-size:13px"><span style="font-size:18px">&#10003;</span> Create and manage tour packages</div>
            <div style="display:flex;align-items:center;gap:10px;font-size:13px"><span style="font-size:18px">&#10003;</span> Accept bookings from tourists</div>
            <div style="display:flex;align-items:center;gap:10px;font-size:13px"><span style="font-size:18px">&#10003;</span> Set your availability calendar</div>
            <div style="display:flex;align-items:center;gap:10px;font-size:13px"><span style="font-size:18px">&#10003;</span> View ratings and feedback</div>
          </div>
        </div>
        <!-- Right panel -->
        <div style="background:#fff;padding:40px">
          <div style="font-size:22px;font-weight:800;color:#1F2937;margin-bottom:6px">{title_text}</div>
          <div style="font-size:13px;color:#6B7280;margin-bottom:24px">{subtitle}</div>
          {active_form}
        </div>
      </div>
    </div>"""
    return build_shell(title_text, body, "guides")
