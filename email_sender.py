import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ── Gmail credentials ──────────────────────────────────────────
# Use a Gmail App Password (NOT your real password).
# Steps to get one:
#   1. Go to myaccount.google.com → Security → 2-Step Verification (enable it)
#   2. Then go to myaccount.google.com/apppasswords
#   3. Create an app password for "Mail" → copy the 16-char password
GMAIL_USER     = "travelatatlas2026@gmail.com"   # your Gmail address
GMAIL_APP_PASS = "lvjy udcy kmfm bwgd"         # 16-char App Password

SITE_URL = "http://localhost:5000"   # change to your deployed URL when live


def send_verification_email(to_email: str, fname: str, token: str) -> bool:
    """Send a verification email. Returns True on success, False on failure."""
    verify_url = f"{SITE_URL}/verify?token={token}"

    html_body = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"/></head>
<body style="margin:0;padding:0;background:#F1F5F9;font-family:'Segoe UI',sans-serif">
  <div style="max-width:520px;margin:40px auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08)">

    <!-- Header -->
    <div style="background:#0038A8;padding:32px 40px;text-align:center">
      <div style="font-size:28px;font-weight:900;color:#fff;letter-spacing:1px">ATLAS</div>
      <div style="font-size:13px;color:rgba(255,255,255,.7);margin-top:4px">Luzon Travel Companion</div>
    </div>

    <!-- Body -->
    <div style="padding:36px 40px">
      <div style="font-size:22px;font-weight:800;color:#0F172A;margin-bottom:8px">
        Hi {fname}! 👋
      </div>
      <div style="font-size:15px;color:#475569;line-height:1.7;margin-bottom:28px">
        Thank you for creating an ATLAS account. Please verify your email address
        to complete your registration and start exploring Luzon!
      </div>

      <!-- Button -->
      <div style="text-align:center;margin-bottom:28px">
        <a href="{verify_url}" style="display:inline-block;background:#0038A8;color:#fff;text-decoration:none;padding:14px 36px;border-radius:10px;font-size:16px;font-weight:700;letter-spacing:.3px">
          ✅ Verify My Email
        </a>
      </div>

      <div style="font-size:13px;color:#94A3B8;line-height:1.6;border-top:1px solid #F1F5F9;padding-top:20px">
        If the button doesn't work, copy and paste this link into your browser:<br/>
        <a href="{verify_url}" style="color:#0038A8;word-break:break-all">{verify_url}</a>
      </div>
      <div style="font-size:12px;color:#CBD5E1;margin-top:12px">
        This link will expire after 24 hours. If you didn't create an ATLAS account, you can safely ignore this email.
      </div>
    </div>

    <!-- Footer -->
    <div style="background:#F8FAFC;padding:18px 40px;text-align:center;border-top:1px solid #E2E8F0">
      <div style="font-size:12px;color:#94A3B8">&copy; 2026 ATLAS. All Rights Reserved.</div>
      <div style="font-size:12px;color:#94A3B8;margin-top:2px">Luzon, Philippines &middot; travelatatlas2026@gmail.com</div>
    </div>
  </div>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "✅ Verify your ATLAS account"
    msg["From"]    = f"ATLAS Travel <{GMAIL_USER}>"
    msg["To"]      = to_email
    msg.attach(MIMEText(html_body, "html"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASS)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False
