import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_USER     = "travelatatlas2026@gmail.com"
GMAIL_APP_PASS = "lvjy udcy kmfm bwgd"
SITE_URL       = "https://atlas-production.up.railway.app"  # update for production


def send_verification_email(to_email: str, fname: str, code: str) -> bool:
    """Send a 6-digit verification code email. Returns True on success."""

    html_body = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"/></head>
<body style="margin:0;padding:0;background:#F1F5F9;font-family:'Segoe UI',sans-serif">
  <div style="max-width:520px;margin:40px auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08)">
    <div style="background:#1E3A5F;padding:32px 40px;text-align:center">
      <div style="font-size:28px;font-weight:900;color:#fff;letter-spacing:1px">ATLAS</div>
      <div style="font-size:13px;color:rgba(255,255,255,.7);margin-top:4px">Luzon Travel Companion</div>
    </div>
    <div style="padding:36px 40px">
      <div style="font-size:22px;font-weight:800;color:#0F172A;margin-bottom:8px">Hi {fname}!</div>
      <div style="font-size:15px;color:#475569;line-height:1.7;margin-bottom:28px">
        Use the verification code below to activate your ATLAS account.
        The code expires in <strong>15 minutes</strong>.
      </div>
      <div style="text-align:center;margin-bottom:28px">
        <div style="display:inline-block;background:#F8FAFC;border:2px solid #0038A8;border-radius:14px;padding:20px 40px">
          <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px">Verification Code</div>
          <div style="font-size:42px;font-weight:900;color:#0038A8;letter-spacing:10px;font-family:monospace">{code}</div>
        </div>
      </div>
      <div style="font-size:13px;color:#94A3B8;line-height:1.6;border-top:1px solid #F1F5F9;padding-top:20px">
        Enter this code on the verification page. If you didn't create an ATLAS account, ignore this email.
      </div>
    </div>
    <div style="background:#F8FAFC;padding:18px 40px;text-align:center;border-top:1px solid #E2E8F0">
      <div style="font-size:12px;color:#94A3B8">&copy; 2026 ATLAS. All Rights Reserved.</div>
      <div style="font-size:12px;color:#94A3B8;margin-top:2px">Luzon, Philippines &middot; travelatatlas2026@gmail.com</div>
    </div>
  </div>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Your ATLAS verification code: {code}"
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


def send_flight_booking_email(to_email: str, fname: str, airline: str,
                               origin: str, destination: str,
                               dep_time: str, arr_time: str) -> bool:
    """Send a flight booking confirmation email."""
    html_body = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"/></head>
<body style="margin:0;padding:0;background:#F1F5F9;font-family:'Segoe UI',sans-serif">
  <div style="max-width:520px;margin:40px auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08)">
    <div style="background:#0038A8;padding:32px 40px;text-align:center">
      <div style="font-size:42px;margin-bottom:8px">&#9992;</div>
      <div style="font-size:28px;font-weight:900;color:#fff;letter-spacing:1px">ATLAS</div>
      <div style="font-size:13px;color:rgba(255,255,255,.7);margin-top:4px">Flight Booking Confirmation</div>
    </div>
    <div style="padding:36px 40px">
      <div style="font-size:22px;font-weight:800;color:#0F172A;margin-bottom:8px">Hi {fname}!</div>
      <div style="font-size:15px;color:#475569;line-height:1.7;margin-bottom:28px">
        Your flight has been saved to your ATLAS profile. Here are your booking details:
      </div>
      <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:20px 24px;margin-bottom:24px">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
          <div style="font-size:22px;font-weight:900;color:#0038A8">{origin.split("(")[0].strip()}</div>
          <div style="font-size:20px;color:#9CA3AF">&#8594;</div>
          <div style="font-size:22px;font-weight:900;color:#0038A8">{destination.split("(")[0].strip()}</div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
          <div style="background:#fff;border-radius:8px;padding:12px;border:1px solid #E2E8F0">
            <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Airline</div>
            <div style="font-weight:700;color:#1F2937">{airline}</div>
          </div>
          <div style="background:#fff;border-radius:8px;padding:12px;border:1px solid #E2E8F0">
            <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Status</div>
            <div style="font-weight:700;color:#059669">Scheduled</div>
          </div>
          <div style="background:#fff;border-radius:8px;padding:12px;border:1px solid #E2E8F0">
            <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Departs</div>
            <div style="font-weight:700;color:#1F2937">{dep_time or "Check airline"}</div>
          </div>
          <div style="background:#fff;border-radius:8px;padding:12px;border:1px solid #E2E8F0">
            <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Arrives</div>
            <div style="font-weight:700;color:#1F2937">{arr_time or "Check airline"}</div>
          </div>
        </div>
      </div>
      <div style="font-size:13px;color:#94A3B8;line-height:1.6;border-top:1px solid #F1F5F9;padding-top:20px">
        You can track your flight status anytime from your ATLAS profile page.
        Always confirm final details directly with your airline before travel.
      </div>
    </div>
    <div style="background:#F8FAFC;padding:18px 40px;text-align:center;border-top:1px solid #E2E8F0">
      <div style="font-size:12px;color:#94A3B8">&copy; 2026 ATLAS. All Rights Reserved.</div>
      <div style="font-size:12px;color:#94A3B8;margin-top:2px">Luzon, Philippines &middot; travelatatlas2026@gmail.com</div>
    </div>
  </div>
</body>
</html>"""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Flight Booking Confirmed — {origin.split('(')[0].strip()} to {destination.split('(')[0].strip()}"
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
