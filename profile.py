import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell

def render(user=None, msg="", err=""):
    if not user:
        return build_shell("Profile", '<div class="page-wrap"><div class="card"><div class="card-body" style="text-align:center;padding:40px"><div style="font-size:40px;margin-bottom:16px">&#128100;</div><div style="font-size:18px;font-weight:700;margin-bottom:12px">Please log in to view your profile</div><a href="/login.py"><button class="btn" style="background:#0038A8;color:#fff;padding:10px 28px">Log In</button></a></div></div></div>', "home", user=None)

    fname = user.get("fname","")
    lname = user.get("lname","")
    email = user.get("email","")
    initials = (fname[0] if fname else "?").upper()

    msg_html = f'<div style="background:#D1FAE5;color:#065F46;padding:12px 16px;border-radius:8px;margin-bottom:16px;font-weight:600">&#10003; {msg}</div>' if msg else ""
    err_html  = f'<div style="background:#FEE2E2;color:#CE1126;padding:12px 16px;border-radius:8px;margin-bottom:16px;font-weight:600">&#9888; {err}</div>' if err else ""

    body = f"""
    <div class="page-wrap" style="max-width:700px;margin:0 auto">
      <div style="margin-bottom:24px">
        <div class="section-title">My Profile</div>
        <div class="section-sub">Manage your tourist account details</div>
      </div>

      {msg_html}{err_html}

      <!-- Profile Card -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8"><span>&#128100; Account Information</span></div>
        <div class="card-body">
          <div style="display:flex;align-items:center;gap:20px;margin-bottom:24px;padding-bottom:20px;border-bottom:1px solid #F3F4F6">
            <div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#0038A8,#CE1126);display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:900;color:#fff;flex-shrink:0">{initials}</div>
            <div>
              <div style="font-size:22px;font-weight:800;color:#1F2937">{fname} {lname}</div>
              <div style="font-size:14px;color:#6B7280;margin-top:4px">&#9993; {email}</div>
              <div style="margin-top:8px"><span style="background:#DBEAFE;color:#1D4ED8;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600">&#9989; Tourist Account</span></div>
            </div>
          </div>
          <form method="post" action="/profile/update">
            <input type="hidden" name="action" value="update_profile"/>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px">
              <div>
                <label class="lbl">First Name</label>
                <input class="inp" name="fname" value="{fname}" style="width:100%"/>
              </div>
              <div>
                <label class="lbl">Last Name</label>
                <input class="inp" name="lname" value="{lname}" style="width:100%"/>
              </div>
            </div>
            <div style="margin-bottom:16px">
              <label class="lbl">Email Address</label>
              <input class="inp" name="email" value="{email}" style="width:100%"/>
            </div>
            <button class="btn" style="background:#0038A8;color:#fff;padding:10px 28px" type="submit">Save Changes</button>
          </form>
        </div>
      </div>

      <!-- Change Password -->
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#CE1126"><span>&#128274; Change Password</span></div>
        <div class="card-body">
          <form method="post" action="/profile/update">
            <input type="hidden" name="action" value="change_password"/>
            <div style="display:flex;flex-direction:column;gap:12px">
              <div>
                <label class="lbl">Current Password</label>
                <input class="inp" type="password" name="old_pw" placeholder="Enter current password" style="width:100%"/>
              </div>
              <div>
                <label class="lbl">New Password</label>
                <input class="inp" type="password" name="new_pw" placeholder="At least 6 characters" style="width:100%"/>
              </div>
              <div>
                <label class="lbl">Confirm New Password</label>
                <input class="inp" type="password" name="new_pw2" placeholder="Repeat new password" style="width:100%"/>
              </div>
            </div>
            <button class="btn" style="background:#CE1126;color:#fff;padding:10px 28px;margin-top:16px" type="submit">Update Password</button>
          </form>
        </div>
      </div>

      <!-- Quick Links -->
      <div class="card">
        <div class="card-hdr" style="background:#065F46"><span>&#128279; Quick Links</span></div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px">
            <a href="/itinerary.py" style="text-decoration:none">
              <div style="background:#EFF6FF;border-radius:10px;padding:14px;text-align:center;border:1px solid #DBEAFE">
                <div style="font-size:28px;margin-bottom:6px">&#128197;</div>
                <div style="font-size:13px;font-weight:700;color:#1D4ED8">My Itinerary</div>
              </div>
            </a>
            <a href="/attractions.py" style="text-decoration:none">
              <div style="background:#F0FDF4;border-radius:10px;padding:14px;text-align:center;border:1px solid #BBF7D0">
                <div style="font-size:28px;margin-bottom:6px">&#127963;</div>
                <div style="font-size:13px;font-weight:700;color:#065F46">Attractions</div>
              </div>
            </a>
            <a href="/restaurants.py" style="text-decoration:none">
              <div style="background:#FFF7ED;border-radius:10px;padding:14px;text-align:center;border:1px solid #FED7AA">
                <div style="font-size:28px;margin-bottom:6px">&#127869;</div>
                <div style="font-size:13px;font-weight:700;color:#C2410C">Restaurants</div>
              </div>
            </a>
            <a href="/guides.py" style="text-decoration:none">
              <div style="background:#FAF5FF;border-radius:10px;padding:14px;text-align:center;border:1px solid #E9D5FF">
                <div style="font-size:28px;margin-bottom:6px">&#129517;</div>
                <div style="font-size:13px;font-weight:700;color:#6B21A8">Tour Guides</div>
              </div>
            </a>
          </div>
        </div>
      </div>
    </div>"""
    return build_shell("My Profile", body, "profile", user=user)
