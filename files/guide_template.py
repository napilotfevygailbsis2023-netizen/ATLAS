def build_guide_shell(title, body, section="", guide=None):
    nav_items = [
        ("dashboard",    "/guide/dashboard",    "<i class='fa-solid fa-house'></i>", "Dashboard"),
        ("packages",     "/guide/packages",     "<i class='fa-regular fa-file'></i>", "My Packages"),
        ("bookings",     "/guide/bookings",     "<i class='fa-regular fa-calendar'></i>", "Bookings"),
        ("availability", "/guide/availability", "<i class='fa-regular fa-clock'></i>", "Availability"),
        ("ratings",      "/guide/ratings",      "<i class='fa-solid fa-star'></i>",  "Ratings & Feedback"),
        ("profile",      "/guide/profile",      "<i class='fa-solid fa-user'></i>", "My Profile"),
    ]

    if guide:
        initials = guide["fname"][0].upper() + guide["lname"][0].upper()
        sidebar = f"""
        <aside style="width:230px;min-height:100vh;background:linear-gradient(180deg,#3B0764,#4C1D95,#1e1b4b);display:flex;flex-direction:column;padding:0;position:fixed;top:0;left:0;z-index:100">
          <div style="padding:24px 20px;border-bottom:1px solid rgba(255,255,255,.1)">
            <a href="/guide" style="display:flex;align-items:center;gap:10px;text-decoration:none">
              <div style="width:34px;height:34px;background:#CE1126;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff;font-size:16px">G</div>
              <div>
                <div style="font-weight:800;color:#fff;font-size:15px">ATLAS</div>
                <div style="font-size:10px;color:#A78BFA">Guide Portal</div>
              </div>
            </a>
          </div>
          <div style="padding:16px 12px;border-bottom:1px solid rgba(255,255,255,.1)">
            <div style="display:flex;align-items:center;gap:12px">
              <div style="width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.2);border:2px solid rgba(255,255,255,.4);display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:800;color:#fff">{initials}</div>
              <div>
                <div style="font-weight:700;color:#fff;font-size:13px">{guide["fname"]} {guide["lname"]}</div>
                <div style="font-size:11px;color:#A78BFA">{guide.get("city","")}</div>
              </div>
            </div>
          </div>
          <nav style="padding:12px 10px;flex:1">
            {"".join(
                f'<a href="{url}" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:8px;text-decoration:none;margin-bottom:2px;font-size:13px;font-weight:{"700" if section==s else "400"};color:{"#fff" if section==s else "#C4B5FD"};background:{"rgba(255,255,255,.15)" if section==s else "transparent"}">{ic} {lb}</a>'
                for s,url,ic,lb in nav_items
            )}
          </nav>
          <div style="padding:12px 10px;border-top:1px solid rgba(255,255,255,.1)">
            <a href="/guide/logout" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:8px;text-decoration:none;font-size:13px;color:#C4B5FD"><i class='fa-solid fa-right-from-bracket'></i> Log Out</a>
          </div>
        </aside>
        <div style="margin-left:230px;min-height:100vh;background:#F1F5F9">"""
        close_layout = "</div>"
    else:
        sidebar = '<div style="min-height:100vh;background:#F1F5F9">'
        close_layout = "</div>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{title} - ATLAS Guide Portal</title>
<link rel="stylesheet" href="/css/styles.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<style>
  body {{ margin:0; font-family:'Segoe UI',sans-serif; background:#F1F5F9; }}
  .g-card {{ background:#fff; border-radius:14px; box-shadow:0 2px 10px rgba(0,0,0,.07); margin-bottom:20px; overflow:hidden; }}
  .g-card-hdr {{ padding:14px 20px; color:#fff; font-weight:800; font-size:15px; }}
  .g-card-body {{ padding:20px; }}
  .g-inp {{ width:100%; padding:9px 12px; border:1px solid #E2E8F0; border-radius:8px; font-size:14px; box-sizing:border-box; }}
  .g-inp:focus {{ outline:none; border-color:#7C3AED; box-shadow:0 0 0 3px rgba(124,58,237,.1); }}
  .g-btn {{ padding:10px 20px; border:none; border-radius:8px; font-size:14px; font-weight:700; cursor:pointer; }}
  .g-lbl {{ font-size:12px; font-weight:600; color:#4B5563; margin-bottom:4px; display:block; text-transform:uppercase; letter-spacing:.5px; }}
  .g-stat {{ border-radius:12px; padding:18px 20px; color:#fff; text-align:center; }}
</style>
</head>
<body>
{sidebar}
<div style="padding:28px 32px; max-width:1100px">
{body}
</div>
{close_layout}
<div id="toast" style="position:fixed;bottom:24px;right:24px;background:#1F2937;color:#fff;padding:12px 20px;border-radius:10px;font-size:14px;display:none;z-index:9999"></div>
<script>
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.style.display='block';setTimeout(function(){{t.style.display='none';}},3000);}}
</script>
</body>
</html>"""
