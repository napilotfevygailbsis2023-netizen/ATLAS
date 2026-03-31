def build_guide_shell(title, body, section="", guide=None):
    _ic_dash  = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>'
    _ic_pkg   = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
    _ic_book  = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
    _ic_avail = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
    _ic_star  = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
    _ic_user  = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
    _ic_out   = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>'
    nav_items = [
        ("dashboard",    "/guide/dashboard",    _ic_dash,  "Dashboard"),
        ("packages",     "/guide/packages",     _ic_pkg,   "My Packages"),
        ("bookings",     "/guide/bookings",     _ic_book,  "Bookings"),
        ("availability", "/guide/availability", _ic_avail, "Availability"),
        ("ratings",      "/guide/ratings",      _ic_star,  "Ratings & Feedback"),
    ]

    if guide:
        initials = guide["fname"][0].upper() + guide["lname"][0].upper()
        sidebar = f"""
        <aside style="width:230px;min-height:100vh;background:#0038A8;display:flex;flex-direction:column;padding:0;position:fixed;top:0;left:0;z-index:100">
          <div style="padding:24px 20px;border-bottom:1px solid rgba(255,255,255,.1)">
            <a href="/guide" style="display:flex;align-items:center;gap:10px;text-decoration:none">
              <img src="/ATLAS_LOGO.jpg" alt="ATLAS" style="width:40px;height:40px;border-radius:50%;object-fit:cover;flex-shrink:0"/>
              <div>
                <div style="font-weight:900;color:#fff;font-size:15px">ATLAS</div>
                <div style="font-size:10px;color:#818CF8">Guide Portal</div>
              </div>
            </a>
          </div>
          <a href="/guide/profile" style="display:flex;align-items:center;gap:12px;margin:12px 8px;background:rgba(255,255,255,.1);border-radius:10px;padding:12px;text-decoration:none;transition:background .2s" onmouseover="this.style.background='rgba(255,255,255,.18)'" onmouseout="this.style.background='rgba(255,255,255,.1)'">
            {f'<img src="{guide["photo_url"]}" style="width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,.5);flex-shrink:0"/>' if guide.get("photo_url") else f'<div style="width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#CE1126,#0038A8);border:2px solid rgba(255,255,255,.4);display:flex;align-items:center;justify-content:center;font-size:17px;font-weight:900;color:#fff;flex-shrink:0">{initials}</div>'}
            <div style="min-width:0">
              <div style="font-weight:700;color:#fff;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{guide["fname"]} {guide["lname"]}</div>
              <div style="font-size:11px;color:#818CF8;margin-top:2px">{guide.get("city","")}</div>
            </div>
          </a>
          <nav style="padding:12px 10px;flex:1">
            {"".join(
                f'<a href="{url}" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:8px;text-decoration:none;margin-bottom:2px;font-size:13px;font-weight:{"700" if section==s else "400"};color:{"#fff" if section==s else "#C7D2FE"};background:{"#4338CA" if section==s else "transparent"}">{ic} {lb}</a>'
                for s,url,ic,lb in nav_items
            )}
          </nav>
          <div style="padding:12px 10px;border-top:1px solid rgba(255,255,255,.1)">
            <a href="/guide/logout" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:8px;text-decoration:none;font-size:13px;color:#F87171"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg> Log Out</a>
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
<style>
  body {{ margin:0; font-family:'Segoe UI',sans-serif; background:#F1F5F9; }}
  .g-card {{ background:#fff; border-radius:14px; box-shadow:0 2px 10px rgba(0,0,0,.07); margin-bottom:20px; overflow:hidden; }}
  .g-card-hdr {{ padding:14px 20px; color:#fff; font-weight:800; font-size:15px; }}
  .g-card-body {{ padding:20px; }}
  .g-inp {{ width:100%; padding:9px 12px; border:1px solid #E2E8F0; border-radius:8px; font-size:14px; box-sizing:border-box; }}
  .g-inp:focus {{ outline:none; border-color:#0038A8; box-shadow:0 0 0 3px rgba(0,56,168,.1); }}
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