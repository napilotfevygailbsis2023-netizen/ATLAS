import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
import authenticator
import db_sqlite as db

def render(user=None, error="", success=""):
    if not user:
        return build_shell("2FA Setup", '<div class="page-wrap"><div class="card"><div class="card-body" style="text-align:center;padding:40px"><div style="font-size:40px;margin-bottom:16px">&#128100;</div><div style="font-size:18px;font-weight:700;margin-bottom:12px">Please log in to set up 2FA</div><a href="/login.py"><button class="btn" style="background:#0038A8;color:#fff;padding:10px 28px">Log In</button></a></div></div></div>', "home", user=None)

    # Check if 2FA is already enabled
    totp_status = authenticator.get_user_2fa_status(user['id'])
    is_enabled = totp_status and totp_status['totp_enabled']
    
    err_html = f'<div style="background:#FEE2E2;color:#DC2626;padding:12px 16px;border-radius:8px;margin-bottom:16px;font-weight:600">&#9888; {error}</div>' if error else ""
    suc_html = f'<div style="background:#D1FAE5;color:#065F46;padding:12px 16px;border-radius:8px;margin-bottom:16px;font-weight:600">&#10003; {success}</div>' if success else ""

    if is_enabled:
        body = f"""
        <div class="page-wrap">
          <div style="margin-bottom:22px">
            <div class="section-title">Two-Factor Authentication</div>
            <div class="section-sub">Manage your 2FA settings</div>
          </div>
          {suc_html}
          <div class="card">
            <div class="card-hdr" style="background:#059669"><span>&#10003; 2FA Enabled</span></div>
            <div class="card-body">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
                <div style="width:48px;height:48px;background:#D1FAE5;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px">&#128274;</div>
                <div>
                  <div style="font-weight:700;color:#059669;font-size:16px">2FA is Active</div>
                  <div style="color:#6B7280;font-size:13px">Your account is protected with two-factor authentication</div>
                </div>
              </div>
              <div style="background:#F3F4F6;border-radius:8px;padding:12px;margin-bottom:16px">
                <div style="font-size:13px;color:#6B7280;margin-bottom:4px">For your security:</div>
                <ul style="font-size:13px;color:#374151;margin:0;padding-left:20px">
                  <li>Keep your backup codes safe</li>
                  <li>Don't share your authentication app</li>
                  <li>Update your recovery options regularly</li>
                </ul>
              </div>
              <form method="post" action="/setup-2fa">
                <input type="hidden" name="action" value="disable"/>
                <button class="btn" style="background:#DC2626;color:#fff;width:100%">Disable 2FA</button>
              </form>
            </div>
          </div>
        </div>"""
    else:
        # Generate new secret for setup
        secret = authenticator.generate_secret()
        qr_code = authenticator.generate_qr_code(user['email'], secret)
        
        body = f"""
        <div class="page-wrap">
          <div style="margin-bottom:22px">
            <div class="section-title">Setup Two-Factor Authentication</div>
            <div class="section-sub">Add an extra layer of security to your account</div>
          </div>
          {err_html}
          <div class="card" style="margin-bottom:20px">
            <div class="card-hdr" style="background:#0038A8"><span>Step 1: Scan QR Code</span></div>
            <div class="card-body">
              <div style="text-align:center;margin-bottom:20px">
                <div style="font-weight:700;margin-bottom:12px">Scan with Google Authenticator</div>
                <img src="{qr_code}" alt="QR Code" style="width:200px;height:200px;border:2px solid #E5E7EB;border-radius:8px"/>
                <div style="font-size:12px;color:#6B7280;margin-top:8px">Can't scan? Use this secret key:</div>
                <div style="background:#F3F4F6;padding:8px 12px;border-radius:6px;font-family:monospace;font-size:14px;margin-top:4px">{secret}</div>
              </div>
            </div>
          </div>
          
          <div class="card">
            <div class="card-hdr" style="background:#0038A8"><span>Step 2: Enter Verification Code</span></div>
            <div class="card-body">
              <form method="post" action="/setup-2fa">
                <input type="hidden" name="action" value="enable"/>
                <input type="hidden" name="secret" value="{secret}"/>
                <div class="field">
                  <label>Authentication Code</label>
                  <input class="inp" type="text" name="verification_code" placeholder="Enter 6-digit code" required/>
                </div>
                <button class="btn" style="background:#0038A8;color:#fff;width:100%">Enable 2FA</button>
              </form>
            </div>
          </div>
        </div>"""

    return build_shell("2FA Setup", body, "setup-2fa", user=user)

def handle_post(form_data, user):
    if not user:
        return None, render(error="User not authenticated")
    
    action = form_data.get("action", "")
    
    if action == "enable":
        secret = form_data.get("secret", "")
        verification_code = form_data.get("verification_code", "")
        
        if not secret or not verification_code:
            return None, render(user=user, error="Please provide the verification code")
        
        # Verify the token
        if authenticator.verify_totp(secret, verification_code):
            # Enable 2FA for user
            if authenticator.enable_2fa_for_user(user['id'], secret):
                return None, render(user=user, success="2FA has been successfully enabled for your account")
            else:
                return None, render(user=user, error="Failed to enable 2FA. Please try again.")
        else:
            return None, render(user=user, error="Invalid verification code. Please try again.")
    
    elif action == "disable":
        # You might want to add password confirmation here
        if authenticator.disable_2fa_for_user(user['id']):
            return None, render(user=user, success="2FA has been disabled for your account")
        else:
            return None, render(user=user, error="Failed to disable 2FA. Please try again.")
    
    return None, render(user=user, error="Invalid action")
