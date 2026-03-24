import sys, os, base64, uuid, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import admin_db, guide_db
from datetime import datetime, date, timedelta

CITIES = ['Albay','Baguio','Bataan','Batangas','Ilocos Norte','Manila','Pangasinan','Tagaytay','Vigan']
BASE   = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_image(file_data, filename_hint="img"):
    if not file_data: return ""
    ext = os.path.splitext(filename_hint)[-1] or ".jpg"
    fname = f"{uuid.uuid4().hex}{ext}"
    fpath = os.path.join(UPLOAD_DIR, fname)
    with open(fpath, "wb") as f: f.write(file_data)
    return f"/uploads/{fname}"

# ── SIDEBAR COLORS (matches guide portal style) ──
SIDEBAR_BG    = "#1E1B4B"   # deep indigo
SIDEBAR_HOVER = "#312E81"
SIDEBAR_ACTIVE= "#4338CA"
SIDEBAR_TEXT  = "#C7D2FE"
SIDEBAR_MUTED = "#818CF8"

NAV_ITEMS = [
    ("dashboard",   "grid",         "Dashboard"),
    ("tourists",    "users",        "Tourists"),
    ("spots",       "map-pin",      "Attractions"),
    ("restaurants", "coffee",       "Restaurants"),
    ("guides",      "user-check",   "Tour Guides"),
    ("transport",   "truck",        "Transportation"),
    ("flights",     "navigation",   "Flights"),
]

# SVG icons (Feather-style)
ICONS = {
    "grid":         '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>',
    "users":        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "map-pin":      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "coffee":       '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>',
    "user-check":   '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><polyline points="17 11 19 13 23 9"/></svg>',
    "truck":        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
    "navigation":   '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>',
    "log-out":      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>',
    "external":     '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>',
    "user":         '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "download":     '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
    "search":       '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
}

def icon(name):
    return ICONS.get(name, "")

def shell(title, body, active, admin):
    aname  = admin.get("fullname","Admin") if admin else "Admin"
    ainit  = (aname[0] if aname else "A").upper()
    today  = datetime.now().strftime("%A, %B %d, %Y")

    nav_html = ""
    for key, ico, label in NAV_ITEMS:
        is_active = active == key
        bg    = f"background:{SIDEBAR_ACTIVE};" if is_active else ""
        color = "color:#fff;font-weight:700;" if is_active else f"color:{SIDEBAR_TEXT};"
        nav_html += f'<a href="/admin/{key}" style="display:flex;align-items:center;gap:10px;padding:11px 20px;text-decoration:none;font-size:13px;border-radius:8px;margin:1px 8px;{bg}{color}">{icon(ico)} {label}</a>'

    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title} - ATLAS Admin</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',sans-serif;background:#F1F5F9;color:#1E293B;min-height:100vh;display:flex}}
.sidebar{{width:240px;flex-shrink:0;background:{SIDEBAR_BG};display:flex;flex-direction:column;height:100vh;position:sticky;top:0;overflow-y:auto}}
.s-brand{{padding:20px;border-bottom:1px solid rgba(255,255,255,.1)}}
.s-logo-row{{display:flex;align-items:center;gap:10px}}
.s-logo{{width:38px;height:38px;background:linear-gradient(135deg,#CE1126,#0038A8);border-radius:10px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:16px}}
.s-title{{color:#fff;font-weight:800;font-size:16px}}
.s-badge{{font-size:11px;color:{SIDEBAR_MUTED};font-weight:700;margin-top:2px}}
.s-admin-card{{margin:12px 8px;background:rgba(255,255,255,.08);border-radius:10px;padding:12px;display:flex;align-items:center;gap:10px}}
.s-av{{width:36px;height:36px;background:linear-gradient(135deg,#CE1126,#0038A8);border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:15px;flex-shrink:0}}
.s-aname{{color:#fff;font-weight:700;font-size:13px;line-height:1.2}}
.s-arole{{color:{SIDEBAR_MUTED};font-size:11px}}
.s-section{{font-size:10px;font-weight:700;color:{SIDEBAR_MUTED};text-transform:uppercase;letter-spacing:.8px;padding:14px 20px 6px}}
.s-bottom{{margin-top:auto;border-top:1px solid rgba(255,255,255,.1);padding:8px}}
.main{{flex:1;display:flex;flex-direction:column;overflow-x:hidden;min-width:0}}
.content{{padding:28px;flex:1}}
.stat-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px;margin-bottom:24px}}
.stat-card{{border-radius:14px;padding:22px;color:#fff;position:relative;overflow:hidden}}
.stat-card-bg{{position:absolute;inset:0;opacity:.15;font-size:80px;display:flex;align-items:center;justify-content:flex-end;padding-right:10px;pointer-events:none}}
.card{{background:#fff;border:1px solid #E2E8F0;border-radius:14px;overflow:hidden;margin-bottom:20px}}
.card-hdr{{padding:14px 20px;border-bottom:1px solid #F1F5F9;display:flex;align-items:center;justify-content:space-between;background:#FAFAFA}}
.card-hdr h3{{font-size:14px;font-weight:700;color:#1E293B}}
.card-body{{padding:20px}}
.search-bar{{display:flex;align-items:center;gap:8px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:8px;padding:8px 12px;margin-bottom:14px}}
.search-bar input{{border:none;background:none;outline:none;font-size:13px;color:#1E293B;flex:1;font-family:inherit}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:left;padding:10px 16px;font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid #F1F5F9;background:#FAFAFA}}
td{{padding:11px 16px;border-bottom:1px solid #F8FAFC;color:#475569;vertical-align:middle}}
tr:last-child td{{border-bottom:none}}
tr:hover td{{background:#FAFAFA}}
.ba{{background:#DCFCE7;color:#16A34A;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700}}
.bs{{background:#FEE2E2;color:#DC2626;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700}}
.bar{{background:#F3F4F6;color:#475569;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700}}
.bb{{background:#DBEAFE;color:#1D4ED8;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700}}
.bg{{background:#DCFCE7;color:#16A34A;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700}}
.btn{{padding:5px 12px;border-radius:6px;font-size:11px;font-weight:700;border:none;cursor:pointer;font-family:inherit;display:inline-flex;align-items:center;gap:4px}}
.bdanger{{background:#FEE2E2;color:#DC2626}}
.bwarn{{background:#FEF3C7;color:#D97706}}
.bsuccess{{background:#DCFCE7;color:#16A34A}}
.bprimary{{background:#4338CA;color:#fff}}
.bgray{{background:#F3F4F6;color:#475569}}
.bblue{{background:#DBEAFE;color:#1D4ED8}}
.bexport{{background:#0038A8;color:#fff;padding:6px 14px;font-size:12px;border-radius:8px;border:none;cursor:pointer;font-family:inherit;display:inline-flex;align-items:center;gap:6px;font-weight:700;text-decoration:none}}
label{{display:block;font-size:11px;font-weight:700;color:#64748B;margin-bottom:4px;text-transform:uppercase;letter-spacing:.4px}}
input:not([type=file]),select,textarea{{width:100%;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:8px;padding:9px 12px;color:#1E293B;font-size:13px;outline:none;font-family:inherit;margin-bottom:12px}}
input:not([type=file]):focus,select:focus,textarea:focus{{border-color:#4338CA;background:#fff}}
input[type=file]{{width:100%;padding:8px;border:1.5px dashed #CBD5E1;border-radius:8px;font-size:13px;margin-bottom:12px;cursor:pointer;background:#F8FAFC}}
.fg2{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.fg3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}}
.tabs{{display:flex;gap:0;border-bottom:2px solid #E2E8F0}}
.tab-btn{{padding:10px 22px;border:none;background:none;font-size:13px;font-weight:600;color:#475569;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-2px;font-family:inherit}}
.tab-btn.active{{color:#4338CA;border-bottom-color:#4338CA;background:#F8FAFC}}
.tab-pane{{display:none}}
.tab-pane.active{{display:block}}
.pager{{display:flex;align-items:center;gap:6px;padding:14px 20px;border-top:1px solid #F1F5F9;justify-content:flex-end}}
.pager a,.pager span{{padding:6px 12px;border-radius:6px;font-size:12px;font-weight:600;text-decoration:none}}
.pager a{{background:#F1F5F9;color:#374151}}
.pager a:hover{{background:#E2E8F0}}
.pager span.cur{{background:#4338CA;color:#fff}}
.pager span.dots{{color:#94A3B8}}
.img-thumb{{width:44px;height:44px;object-fit:cover;border-radius:8px;border:1px solid #E2E8F0}}
.filter-bar{{display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:12px 16px;background:#F8FAFC;border-bottom:1px solid #F1F5F9}}
.filter-bar select,.filter-bar input{{margin-bottom:0;width:auto;padding:7px 10px;font-size:12px}}
a.snl{{display:flex;align-items:center;gap:10px;padding:11px 20px;text-decoration:none;font-size:13px;color:#F87171;border-radius:8px;margin:1px 8px}}
a.snl:hover{{background:rgba(255,255,255,.08)}}
a.snv{{display:flex;align-items:center;gap:10px;padding:11px 20px;text-decoration:none;font-size:13px;color:{SIDEBAR_TEXT};border-radius:8px;margin:1px 8px}}
a.snv:hover{{background:rgba(255,255,255,.08)}}
</style>
</head><body>
<div class="sidebar">
  <div class="s-brand">
    <div class="s-logo-row">
      <div class="s-logo">A</div>
      <div><div class="s-title">ATLAS</div><div class="s-badge">ADMIN PANEL</div></div>
    </div>
  </div>
  <!-- Admin card under logo -->
  <a href="/admin/profile" style="text-decoration:none">
    <div class="s-admin-card">
      <div class="s-av">{ainit}</div>
      <div>
        <div class="s-aname">{aname}</div>
        <div class="s-arole">Admin</div>
      </div>
    </div>
  </a>
  <div class="s-section">Navigation</div>
  {nav_html}
  <div class="s-bottom">
    <div style="padding:8px 20px 6px;font-size:11px;color:#818CF8;font-weight:600">{today}</div>
    <a class="snl" href="/admin/logout">{icon("log-out")} Log Out</a>
    <a class="snv" href="/" target="_blank">{icon("external")} View Site</a>
  </div>
</div>
<div class="main">
  <div class="content">{body}</div>
</div>
<script>
function switchTab(group, tab) {{
  document.querySelectorAll('[data-group="'+group+'"] .tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('[data-group="'+group+'"] .tab-pane').forEach(p => p.classList.remove('active'));
  document.querySelector('[data-group="'+group+'"] [data-tab="'+tab+'"]').classList.add('active');
  document.getElementById(group+'-'+tab).classList.add('active');
}}
function filterTable(inputId, tableId) {{
  var q = document.getElementById(inputId).value.toLowerCase();
  document.querySelectorAll('#'+tableId+' tbody tr').forEach(function(tr) {{
    tr.style.display = tr.textContent.toLowerCase().includes(q) ? '' : 'none';
  }});
}}
function applyFilters(tableId, filters) {{
  // filters: array of {{col: colIndex, value: ""}}
  document.querySelectorAll('#'+tableId+' tbody tr').forEach(function(tr) {{
    var show = true;
    filters.forEach(function(f) {{
      if (!f.value) return;
      var td = tr.cells[f.col];
      if (!td) return;
      var txt = td.textContent.toLowerCase();
      if (!txt.includes(f.value.toLowerCase())) show = false;
    }});
    tr.style.display = show ? '' : 'none';
  }});
}}
function exportTableCSV(tableId, filename) {{
  var rows = [];
  document.querySelectorAll('#'+tableId+' tr').forEach(function(tr) {{
    var cells = [];
    tr.querySelectorAll('th,td').forEach(function(td) {{
      cells.push('"'+td.innerText.replace(/"/g,'""')+'"');
    }});
    rows.push(cells.join(','));
  }});
  var csv = rows.join('\\n');
  var a = document.createElement('a');
  a.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
  a.download = filename + '.csv';
  a.click();
}}
function exportTablePDF(tableId, title) {{
  var win = window.open('','_blank');
  var tbl = document.getElementById(tableId);
  win.document.write('<html><head><title>'+title+'</title><style>body{{font-family:sans-serif;padding:20px}}h2{{margin-bottom:12px;color:#0038A8}}table{{width:100%;border-collapse:collapse;font-size:12px}}th{{background:#0038A8;color:#fff;padding:8px;text-align:left}}td{{padding:7px 8px;border-bottom:1px solid #eee}}</style></head><body>');
  win.document.write('<h2>'+title+'</h2>');
  win.document.write(tbl.outerHTML);
  win.document.write('<script>window.onload=function(){{window.print();window.close();}}<\\/script></body></html>');
  win.document.close();
}}
</script>
</body></html>"""

def _alert(msg="", err=""):
    out=""
    if msg: out+=f'<div style="background:#DCFCE7;border:1px solid #BBF7D0;border-radius:8px;padding:10px 14px;color:#15803D;font-size:13px;margin-bottom:16px"><i class=&#34;fa-solid fa-check&#34;></i> {msg}</div>'
    if err: out+=f'<div style="background:#FEE2E2;border:1px solid #FECACA;border-radius:8px;padding:12px 16px;color:#991B1B;font-size:13px;margin-bottom:16px"><i class=&#34;fa-solid fa-triangle-exclamation&#34;></i> {err}</div>'
    return out

def _stars(n):
    try: n=int(float(n))
    except: n=0
    return "<i class=&#34;fa-solid fa-star&#34;></i>"*min(n,5)+"<i class=&#34;fa-regular fa-star&#34;></i>"*(5-min(n,5))

def _img_cell(url, ico):
    if url: return f'<img src="{url}" class="img-thumb" onerror="this.style.display=\'none\'"/>'
    return f'<div style="width:44px;height:44px;background:#F1F5F9;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#CBD5E1;font-size:20px">{ico}</div>'

def _paginate(rows_html_list, page, per_page, base_url, extra_params=""):
    total = len(rows_html_list)
    pages = max(1, (total + per_page - 1) // per_page)
    page  = max(1, min(page, pages))
    start = (page-1)*per_page
    shown = rows_html_list[start:start+per_page]
    sep = "&" if "?" in base_url else "?"
    pager = ""
    if pages > 1:
        pager = '<div class="pager">'
        if page > 1: pager += f'<a href="{base_url}{sep}page={page-1}{extra_params}"><i class=&#34;fa-solid fa-arrow-left&#34;></i> Prev</a>'
        for p in range(1, pages+1):
            if p == page: pager += f'<span class="cur">{p}</span>'
            elif abs(p-page) <= 2 or p == 1 or p == pages: pager += f'<a href="{base_url}{sep}page={p}{extra_params}">{p}</a>'
            elif abs(p-page) == 3: pager += '<span class="dots">…</span>'
        if page < pages: pager += f'<a href="{base_url}{sep}page={page+1}{extra_params}">Next <i class=&#34;fa-solid fa-arrow-right&#34;></i></a>'
        pager += "</div>"
    return "".join(shown), pager, total, pages

def _export_btns(table_id, title):
    return f'''<div style="display:flex;gap:8px">
      <button class="bexport" onclick="exportTableCSV('{table_id}','{title}')">{icon("download")} CSV</button>
      <button class="bexport" style="background:#1E3A5F" onclick="exportTablePDF('{table_id}','{title}')">{icon("download")} PDF</button>
    </div>'''

def _search_bar(input_id, table_id, placeholder="Search..."):
    return f'''<div class="filter-bar">
      <div style="display:flex;align-items:center;gap:6px;background:#fff;border:1.5px solid #E2E8F0;border-radius:8px;padding:7px 12px;flex:1;max-width:320px">
        {icon("search")}<input id="{input_id}" placeholder="{placeholder}" oninput="filterTable('{input_id}','{table_id}')" style="border:none;background:none;outline:none;font-size:13px;width:100%;margin:0"/>
      </div>
    </div>'''

# ── DASHBOARD ──
def dashboard(admin):
    s = admin_db.get_stats()
    db_spots   = admin_db.get_spots()
    db_rests   = admin_db.get_restaurants()
    db_guides  = admin_db.get_guides()
    db_trans   = admin_db.get_transport()
    reg_guides = guide_db.get_public_guides()

    cards = [
        ("#1D4ED8","#DBEAFE","users",     "Tourists",       s["total_tourists"],              f'{s["active_tourists"]} active · {s["suspended"]} suspended'),
        ("#D97706","#FEF3C7","map-pin",   "Attractions",    len(db_spots),                    "admin-added spots"),
        ("#BE185D","#FCE7F3","coffee",    "Restaurants",    len(db_rests),                    "admin-added"),
        ("#7C3AED","#EDE9FE","user-check","Tour Guides",    len(db_guides)+len(reg_guides),   f'{len(reg_guides)} registered'),
        ("#0369A1","#E0F2FE","truck",     "Transport",      len(db_trans),                    "admin-added routes"),
        ("#065F46","#DCFCE7","navigation","Flights",        s.get("total_flights",0),         "admin-added"),
    ]
    sc = ""
    for color, bg, ico, lbl, val, sub in cards:
        sc += f'''<div class="stat-card" style="background:{bg};border:1px solid {color}22">
          <div style="font-size:12px;font-weight:700;color:{color};margin-bottom:6px;text-transform:uppercase;letter-spacing:.5px">{lbl}</div>
          <div style="font-size:32px;font-weight:800;color:{color};margin-bottom:4px">{val}</div>
          <div style="font-size:11px;color:{color}99">{sub}</div>
          <div style="position:absolute;bottom:8px;right:12px;opacity:.15">{icon(ico)}</div>
        </div>'''

    recent = admin_db.get_recent_tourists(6)
    def _badge(st):
        if st=="archived": return '<span class=bar>Archived</span>'
        if st=="suspended": return '<span class=bs>Suspended</span>'
        return '<span class=ba>Active</span>'
    rows = "".join(f'<tr><td style="font-weight:600;color:#1E293B">{u["fname"]} {u["lname"]}</td><td>{u["email"]}</td><td>{(u.get("created") or "")[:10]}</td><td>{_badge(u.get("status") or "active")}</td></tr>' for u in recent) or '<tr><td colspan="4" style="text-align:center;color:#94A3B8;padding:20px">No tourists yet</td></tr>'

    body = f'''
    <div style="font-size:22px;font-weight:800;margin-bottom:4px">Dashboard</div>
    <div style="font-size:13px;color:#94A3B8;margin-bottom:24px">Welcome back, {admin.get("fullname","Admin")}!</div>
    <div class="stat-grid">{sc}</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
      <div class="card">
        <div class="card-hdr"><h3>Recent Tourists</h3><a href="/admin/tourists" style="font-size:12px;color:#4338CA;font-weight:700;text-decoration:none">View All</a></div>
        <table id="dash-tourists"><thead><tr><th>Name</th><th>Email</th><th>Joined</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table>
      </div>
      <div class="card">
        <div class="card-hdr"><h3>Quick Stats</h3></div>
        <div class="card-body">
          <div style="display:flex;flex-direction:column;gap:12px">
            <div style="display:flex;justify-content:space-between;align-items:center;padding:10px;background:#F8FAFC;border-radius:8px"><span style="font-size:13px;font-weight:600">Total Tourists</span><span style="font-weight:800;color:#1D4ED8;font-size:18px">{s["total_tourists"]}</span></div>
            <div style="display:flex;justify-content:space-between;align-items:center;padding:10px;background:#F8FAFC;border-radius:8px"><span style="font-size:13px;font-weight:600">Active</span><span style="font-weight:800;color:#16A34A;font-size:18px">{s["active_tourists"]}</span></div>
            <div style="display:flex;justify-content:space-between;align-items:center;padding:10px;background:#F8FAFC;border-radius:8px"><span style="font-size:13px;font-weight:600">Suspended</span><span style="font-weight:800;color:#DC2626;font-size:18px">{s["suspended"]}</span></div>
            <div style="display:flex;justify-content:space-between;align-items:center;padding:10px;background:#F8FAFC;border-radius:8px"><span style="font-size:13px;font-weight:600">Registered Guides</span><span style="font-weight:800;color:#7C3AED;font-size:18px">{len(reg_guides)}</span></div>
          </div>
        </div>
      </div>
    </div>
    <div class="card" style="margin-top:4px">
      <div class="card-hdr"><h3>Export Dashboard Data</h3></div>
      <div class="card-body" style="display:flex;gap:10px;flex-wrap:wrap">
        {_export_btns("dash-tourists","ATLAS_Recent_Tourists")}
      </div>
    </div>'''
    return shell("Dashboard", body, "dashboard", admin)

# ── TOURISTS ──

# ── TOURISTS ──
def tourists_page(admin, msg="", err="", tab="active"):
    users = admin_db.get_all_tourists()
    def _badge(st):
        if st=="archived": return '<span class=bar>Archived</span>'
        if st=="suspended": return '<span class=bs>Suspended</span>'
        return '<span class=ba>Active</span>'

    groups = {
        "active":   [u for u in users if (u.get("status") or "active")=="active"],
        "suspended":[u for u in users if u.get("status")=="suspended"],
        "archived": [u for u in users if u.get("status")=="archived"],
    }
    counts = {k:len(v) for k,v in groups.items()}
    counts["all"] = len(users)

    # Get unique months from joined dates
    months = sorted(set((u.get("created","") or "")[:7] for u in users if u.get("created")), reverse=True)
    month_opts = '<option value="">All Months</option>' + "".join(f'<option value="{m}">{m}</option>' for m in months)

    def build_rows(lst):
        if not lst: return '<tr><td colspan="5" style="text-align:center;color:#94A3B8;padding:20px">No users in this group</td></tr>'
        rows=""
        for u in lst:
            st = u.get("status") or "active"
            if st=="archived":
                acts = f'<a href="/admin/tourists/activate/{u["id"]}"><button class="btn bsuccess" style="margin-right:4px">Restore</button></a><a href="/admin/tourists/delete/{u["id"]}" onclick="return confirm(\'Delete permanently?\')"><button class="btn bdanger">Delete</button></a>'
            elif st=="suspended":
                acts = f'<a href="/admin/tourists/activate/{u["id"]}"><button class="btn bsuccess" style="margin-right:4px">Activate</button></a><a href="/admin/tourists/archive/{u["id"]}"><button class="btn bgray" style="margin-right:4px">Archive</button></a><a href="/admin/tourists/delete/{u["id"]}" onclick="return confirm(\'Delete?\')"><button class="btn bdanger">Delete</button></a>'
            else:
                acts = f'<a href="/admin/tourists/suspend/{u["id"]}"><button class="btn bwarn" style="margin-right:4px">Suspend</button></a><a href="/admin/tourists/archive/{u["id"]}"><button class="btn bgray" style="margin-right:4px">Archive</button></a><a href="/admin/tourists/delete/{u["id"]}" onclick="return confirm(\'Delete?\')"><button class="btn bdanger">Delete</button></a>'
            rows += f'<tr><td style="font-weight:600;color:#1E293B">{u["fname"]} {u["lname"]}</td><td>{u["email"]}</td><td>{(u.get("created") or "")[:10]}</td><td>{_badge(st)}</td><td>{acts}</td></tr>'
        return rows

    tab_labels = [("all","All",counts["all"],"#1D4ED8"),("active","Active",counts["active"],"#16A34A"),("suspended","Suspended",counts["suspended"],"#D97706"),("archived","Archived",counts["archived"],"#6B7280")]
    tab_btns = "".join(f'<button class="tab-btn {"active" if tab==k else ""}" data-tab="{k}" onclick="switchTab(\'tourists\',\'{k}\')">{lbl} <span style="background:{"#EEF2FF" if tab==k else "#F3F4F6"};color:{c};padding:1px 7px;border-radius:10px;font-size:11px">{cnt}</span></button>' for k,lbl,cnt,c in tab_labels)

    def pane(pid, rows_data, tbl_id):
        a = "active" if pid==tab else ""
        rows = build_rows(rows_data)
        return f'''<div id="tourists-{pid}" class="tab-pane {a}">
          <div class="filter-bar">
            <div style="display:flex;align-items:center;gap:6px;background:#fff;border:1.5px solid #E2E8F0;border-radius:8px;padding:7px 12px;flex:1;max-width:280px">
              <input id="srch-{pid}" placeholder="Search name or email..." oninput="applyFilters(\'{tbl_id}\',[{{col:0,value:document.getElementById(\'srch-{pid}\').value}},{{col:1,value:document.getElementById(\'srch-{pid}\').value}}])" style="border:none;background:none;outline:none;font-size:13px;width:100%;margin:0"/>
            </div>
            <select onchange="applyFilters(\'{tbl_id}\',[{{col:2,value:this.value}}])" style="margin:0;width:auto;padding:7px 10px;font-size:12px">{month_opts}</select>
          </div>
          <div style="padding:0 16px 8px;display:flex;justify-content:flex-end">{_export_btns(tbl_id, f"ATLAS_Tourists_{pid}")}</div>
          <table id="{tbl_id}"><thead><tr><th>Name</th><th>Email</th><th>Joined</th><th>Status</th><th>Actions</th></tr></thead><tbody>{rows}</tbody></table>
        </div>'''

    body = f'''
    <div style="font-size:22px;font-weight:800;margin-bottom:4px">Tourists</div>
    <div style="font-size:13px;color:#94A3B8;margin-bottom:20px">Manage tourist accounts · {counts["all"]} total</div>
    {_alert(msg,err)}
    <div class="card">
      <div style="padding:0 20px" data-group="tourists">
        <div class="tabs">{tab_btns}</div>
        {pane("all", users, "tbl-tourists-all")}
        {pane("active", groups["active"], "tbl-tourists-active")}
        {pane("suspended", groups["suspended"], "tbl-tourists-suspended")}
        {pane("archived", groups["archived"], "tbl-tourists-archived")}
      </div>
    </div>'''
    return shell("Tourists", body, "tourists", admin)

# ── ATTRACTIONS ──
def spots_page(admin, msg="", err="", page=1, tab="list"):
    from attractions import get_spots
    ALL_CITIES = ["Manila","Baguio","Ilocos Norte","Vigan","Batangas","Tagaytay","Albay","Pangasinan","Bataan"]
    CATS = ["All","Nature","Historical","Heritage","Landmark","Museum","Park"]
    ENTRY_RANGES = ["All","Free","1-50","51-100","101-150","151-200","201-500","500+"]
    RATINGS = ["All","5","4","3","2","1"]
    PER = 10
    all_rows = []
    seen = set()
    for city in ALL_CITIES:
        for s in get_spots(city):
            key = s["name"].strip().lower()
            if key in seen: continue
            seen.add(key)
            img   = _img_cell(s.get("img",""), "<i class=&#34;fa-solid fa-landmark&#34;></i>")
            cat   = s.get("cat","Landmark")
            entry = s.get("entry","Check on-site")
            rat   = str(s["rating"])
            all_rows.append(f'<tr><td>{img}</td><td style="font-weight:600;color:#1E293B">{s["name"]}</td><td>{city}</td><td><span class=bb>{cat}</span></td><td>{rat}</td><td>{entry}</td></tr>')

    rows_html, pager, total, _ = _paginate(all_rows, page, PER, "/admin/spots")
    city_opts = '<option value="">All Cities</option>' + "".join(f'<option value="{c}">{c}</option>' for c in ALL_CITIES)
    cat_opts  = "".join(f'<option value="{c if c!="All" else ""}">{c}</option>' for c in CATS)
    rat_opts  = "".join(f'<option value="{r if r!="All" else ""}">{r} <i class=&#34;fa-solid fa-star&#34;></i></option>' for r in RATINGS)

    body = f'''
    <div style="font-size:22px;font-weight:800;margin-bottom:4px">Attractions</div>
    <div style="font-size:13px;color:#94A3B8;margin-bottom:20px">{total} attractions across all cities</div>
    {_alert(msg,err)}
    <div class="card">
      <div class="filter-bar">
        <div style="display:flex;align-items:center;gap:6px;background:#fff;border:1.5px solid #E2E8F0;border-radius:8px;padding:7px 12px;flex:1;max-width:240px">
          <input id="srch-spots" placeholder="Search..." oninput="applyFilters('tbl-spots',[{{col:1,value:this.value}}])" style="border:none;background:none;outline:none;font-size:13px;width:100%;margin:0"/>
        </div>
        <select onchange="applyFilters('tbl-spots',[{{col:2,value:this.value}}])" style="margin:0;width:auto;padding:7px 10px;font-size:12px">{city_opts}</select>
        <select onchange="applyFilters('tbl-spots',[{{col:3,value:this.value}}])" style="margin:0;width:auto;padding:7px 10px;font-size:12px">{cat_opts}</select>
        <select onchange="applyFilters('tbl-spots',[{{col:4,value:this.value}}])" style="margin:0;width:auto;padding:7px 10px;font-size:12px">{rat_opts}</select>
        <input placeholder="Entry fee e.g. 75" oninput="applyFilters('tbl-spots',[{{col:5,value:this.value}}])" style="margin:0;width:120px;padding:7px 10px;font-size:12px;border:1.5px solid #E2E8F0;border-radius:8px;background:#fff"/>
      </div>
      <div style="padding:0 16px 8px;display:flex;justify-content:flex-end">{_export_btns("tbl-spots","ATLAS_Attractions")}</div>
      <table id="tbl-spots"><thead><tr><th>Img</th><th>Name</th><th>City</th><th>Category</th><th>Rating</th><th>Entry Fee</th></tr></thead>
      <tbody>{"" if rows_html else "<tr><td colspan=6 style='text-align:center;color:#94A3B8;padding:20px'>No data</td></tr>"}{rows_html}</tbody></table>
      {pager}
    </div>'''
    return shell("Attractions", body, "spots", admin)

# ── RESTAURANTS ──
def restaurants_page(admin, msg="", err="", page=1, tab="list"):
    from restaurants import get_restaurants
    ALL_CITIES = ["Manila","Baguio","Ilocos Norte","Vigan","Batangas","Tagaytay","Albay","Pangasinan","Bataan"]
    CUISINES = ["All","Filipino","Seafood","Cafe","Grill","Heritage","Ilocano","Bicolano","Fine Dining","Street Food","Buffet","International"]
    RATINGS = ["All","5","4","3","2","1"]
    PER = 10
    all_rows = []
    seen = set()
    for city in ALL_CITIES:
        for r in get_restaurants(city):
            key = r["name"].strip().lower()
            if key in seen: continue
            seen.add(key)
            img = _img_cell(r.get("img",""), "<i class=&#34;fa-solid fa-utensils&#34;></i>")
            all_rows.append(f'<tr><td>{img}</td><td style="font-weight:600;color:#1E293B">{r["name"]}</td><td>{city}</td><td>{r.get("type","Filipino")}</td><td style="color:#16A34A;font-weight:600">{r.get("price","Check restaurant")}</td><td>{str(r["rating"])}</td></tr>')

    rows_html, pager, total, _ = _paginate(all_rows, page, PER, "/admin/restaurants")
    city_opts    = '<option value="">All Cities</option>' + "".join(f'<option value="{c}">{c}</option>' for c in ALL_CITIES)
    cuisine_opts = "".join(f'<option value="{c if c!="All" else ""}">{c}</option>' for c in CUISINES)
    rat_opts     = "".join(f'<option value="{r if r!="All" else ""}">{r} <i class=&#34;fa-solid fa-star&#34;></i></option>' for r in RATINGS)

    body = f'''
    <div style="font-size:22px;font-weight:800;margin-bottom:4px">Restaurants</div>
    <div style="font-size:13px;color:#94A3B8;margin-bottom:20px">{total} restaurants across all cities</div>
    {_alert(msg,err)}
    <div class="card">
      <div class="filter-bar">
        <div style="display:flex;align-items:center;gap:6px;background:#fff;border:1.5px solid #E2E8F0;border-radius:8px;padding:7px 12px;flex:1;max-width:240px">
          <input placeholder="Search..." oninput="applyFilters('tbl-rests',[{{col:1,value:this.value}}])" style="border:none;background:none;outline:none;font-size:13px;width:100%;margin:0"/>
        </div>
        <select onchange="applyFilters('tbl-rests',[{{col:2,value:this.value}}])" style="margin:0;width:auto;padding:7px 10px;font-size:12px">{city_opts}</select>
        <select onchange="applyFilters('tbl-rests',[{{col:3,value:this.value}}])" style="margin:0;width:auto;padding:7px 10px;font-size:12px">{cuisine_opts}</select>
        <select onchange="applyFilters('tbl-rests',[{{col:5,value:this.value}}])" style="margin:0;width:auto;padding:7px 10px;font-size:12px">{rat_opts}</select>
        <input placeholder="Price e.g. PHP 200" oninput="applyFilters('tbl-rests',[{{col:4,value:this.value}}])" style="margin:0;width:140px;padding:7px 10px;font-size:12px;border:1.5px solid #E2E8F0;border-radius:8px;background:#fff"/>
      </div>
      <div style="padding:0 16px 8px;display:flex;justify-content:flex-end">{_export_btns("tbl-rests","ATLAS_Restaurants")}</div>
      <table id="tbl-rests"><thead><tr><th>Img</th><th>Name</th><th>City</th><th>Cuisine</th><th>Price</th><th>Rating</th></tr></thead>
      <tbody>{"" if rows_html else "<tr><td colspan=6 style='text-align:center;color:#94A3B8;padding:20px'>No data</td></tr>"}{rows_html}</tbody></table>
      {pager}
    </div>'''
    return shell("Restaurants", body, "restaurants", admin)

# ── TOUR GUIDES ──
def guides_page(admin, msg="", err="", page=1, tab="registered"):
    reg_guides = guide_db.get_public_guides()
    ALL_CITIES = ["Manila","Baguio","Ilocos Norte","Vigan","Batangas","Tagaytay","Albay","Pangasinan","Bataan","La Union","Bataan"]
    LANGS = ["All","English","Filipino","Ilocano","Bicolano","Waray","Kapampangan"]
    PER = 8

    reg_list = []
    for g in reg_guides:
        avg, cnt = guide_db.get_avg_rating(g["id"])
        img = _img_cell(g.get("photo",""), "<i class=&#34;fa-solid fa-user-tie&#34;></i>")
        city = g["city"]
        lang = g.get("languages","EN, FIL")
        rate = g.get("rate","N/A")
        reg_list.append(f'<tr><td>{img}</td><td style="font-weight:600;color:#1E293B">{g["fname"]} {g["lname"]}</td><td>{city}</td><td>{lang}</td><td style="color:#7C3AED;font-weight:600">{rate}</td><td>{avg}<i class=&#34;fa-solid fa-star&#34;></i> ({cnt})</td><td><span class=ba>Registered</span></td></tr>')

    reg_rows, reg_pager, reg_total, _ = _paginate(reg_list, page, PER, "/admin/guides")
    city_opts = '<option value="">All Cities</option>' + "".join(f'<option value="{c}">{c}</option>' for c in sorted(set(ALL_CITIES)))
    lang_opts = "".join(f'<option value="{l if l!="All" else ""}">{l}</option>' for l in LANGS)
    rat_opts  = "".join(f'<option value="{r if r!="All" else ""}">{r} <i class=&#34;fa-solid fa-star&#34;></i></option>' for r in ["All","5","4","3","2","1"])

    body = f'''
    <div style="font-size:22px;font-weight:800;margin-bottom:4px">Tour Guides</div>
    <div style="font-size:13px;color:#94A3B8;margin-bottom:20px">{reg_total} registered guides</div>
    {_alert(msg,err)}
    <div class="card">
      <div class="filter-bar">
        <div style="display:flex;align-items:center;gap:6px;background:#fff;border:1.5px solid #E2E8F0;border-radius:8px;padding:7px 12px;flex:1;max-width:240px">
          <input placeholder="Search guides..." oninput="applyFilters('tbl-guides',[{{col:1,value:this.value}}])" style="border:none;background:none;outline:none;font-size:13px;width:100%;margin:0"/>
        </div>
        <select onchange="applyFilters('tbl-guides',[{{col:2,value:this.value}}])" style="margin:0;width:auto;padding:7px 10px;font-size:12px">{city_opts}</select>
        <select onchange="applyFilters('tbl-guides',[{{col:3,value:this.value}}])" style="margin:0;width:auto;padding:7px 10px;font-size:12px">{lang_opts}</select>
        <select onchange="applyFilters('tbl-guides',[{{col:5,value:this.value}}])" style="margin:0;width:auto;padding:7px 10px;font-size:12px">{rat_opts}</select>
      </div>
      <div style="padding:0 16px 8px;display:flex;justify-content:flex-end">{_export_btns("tbl-guides","ATLAS_Tour_Guides")}</div>
      <table id="tbl-guides"><thead><tr><th>Photo</th><th>Name</th><th>City</th><th>Languages</th><th>Rate</th><th>Rating</th><th>Status</th></tr></thead>
      <tbody>{"" if reg_rows else "<tr><td colspan=7 style='text-align:center;color:#94A3B8;padding:20px'>No registered guides yet</td></tr>"}{reg_rows}</tbody></table>
      {reg_pager}
    </div>'''
    return shell("Tour Guides", body, "guides", admin)

# ── TRANSPORTATION ──
def transport_page(admin, msg="", err="", page=1, tab="list"):
    items = admin_db.get_transport()
    TYPES = ["All","Bus","Van","Train","Ferry","Jeepney"]
    PER = 8
    row_list = []
    for t in items:
        acts = f'<a href="/admin/transport/delete/{t["id"]}" onclick="return confirm(\'Delete?\')"><button class="btn bdanger">Delete</button></a>'
        row_list.append(f'<tr><td style="font-weight:600;color:#1E293B">{t["route"]}</td><td><span class=bb>{t["type"]}</span></td><td>{t["origin"]}</td><td>{t["dest"]}</td><td>{t["dep_time"]}</td><td style="color:#0369A1;font-weight:600">{t["fare"]}</td><td>{acts}</td></tr>')

    rows_html, pager, total, _ = _paginate(row_list, page, PER, "/admin/transport")
    type_opts = "".join(f'<option value="{tp if tp!="All" else ""}">{tp}</option>' for tp in TYPES)
    tab_btns = (
        f'<button class="tab-btn {"active" if tab=="add" else ""}" data-tab="add" onclick="switchTab(\'transport\',\'add\')">+ Add Route</button>'
        f'<button class="tab-btn {"active" if tab=="list" else ""}" data-tab="list" onclick="switchTab(\'transport\',\'list\')">All Routes ({total})</button>'
    )
    add_form = f'''<div id="transport-add" class="tab-pane {"active" if tab=="add" else ""}"><div style="padding:20px">
    <form method="post" action="/admin/transport/add"><div class="fg2">
    <div><label>Route Name *</label><input name="route" placeholder="Manila to Baguio Express" required/></div>
    <div><label>Type</label><select name="type"><option>Bus</option><option>Van</option><option>Train</option><option>Ferry</option><option>Jeepney</option></select></div>
    <div><label>Origin *</label><input name="origin" placeholder="Manila, Tarlac..." required/></div>
    <div><label>Destination *</label><input name="dest" placeholder="Baguio, Ilocos Norte..." required/></div>
    <div><label>Departure Time *</label><input name="dep_time" placeholder="6:00 AM" required/></div>
    <div><label>Fare</label><input name="fare" placeholder="PHP 450"/></div>
    </div><button class="btn bprimary" type="submit" style="padding:9px 22px;font-size:13px">+ Add Route</button>
    </form></div></div>'''

    list_pane = f'''<div id="transport-list" class="tab-pane {"active" if tab=="list" else ""}">
      <div class="filter-bar">
        <div style="display:flex;align-items:center;gap:6px;background:#fff;border:1.5px solid #E2E8F0;border-radius:8px;padding:7px 12px;flex:1;max-width:240px">
          <input placeholder="Search routes..." oninput="applyFilters('tbl-transport',[{{col:0,value:this.value}}])" style="border:none;background:none;outline:none;font-size:13px;width:100%;margin:0"/>
        </div>
        <select onchange="applyFilters('tbl-transport',[{{col:1,value:this.value}}])" style="margin:0;width:auto;padding:7px 10px;font-size:12px">{type_opts}</select>
        <input placeholder="Origin city..." oninput="applyFilters('tbl-transport',[{{col:2,value:this.value}}])" style="margin:0;width:130px;padding:7px 10px;font-size:12px;border:1.5px solid #E2E8F0;border-radius:8px;background:#fff"/>
        <input placeholder="Destination city..." oninput="applyFilters('tbl-transport',[{{col:3,value:this.value}}])" style="margin:0;width:140px;padding:7px 10px;font-size:12px;border:1.5px solid #E2E8F0;border-radius:8px;background:#fff"/>
      </div>
      <div style="padding:0 16px 8px;display:flex;justify-content:flex-end">{_export_btns("tbl-transport","ATLAS_Transport")}</div>
      <table id="tbl-transport"><thead><tr><th>Route Name</th><th>Type</th><th>Origin</th><th>Destination</th><th>Departure</th><th>Fare</th><th>Action</th></tr></thead>
      <tbody>{"" if rows_html else "<tr><td colspan=7 style='text-align:center;color:#94A3B8;padding:20px'>No routes added yet</td></tr>"}{rows_html}</tbody></table>
      {pager}</div>'''

    body = f'''
    <div style="font-size:22px;font-weight:800;margin-bottom:4px">Transportation</div>
    <div style="font-size:13px;color:#94A3B8;margin-bottom:20px">{total} routes</div>
    {_alert(msg,err)}
    <div class="card"><div style="padding:0 20px" data-group="transport">
      <div class="tabs">{tab_btns}</div>
      {add_form}{list_pane}
    </div></div>'''
    return shell("Transportation", body, "transport", admin)

# ── FLIGHTS ──
def flights_page(admin, msg="", err=""):
    # Domestic: Luzon-relevant routes from MNL and CRK
    DOMESTIC_ROUTES = [
        {"airline":"Philippine Airlines","from":"Manila (MNL)","to":"Laoag, Ilocos Norte (LAO)","dep":"06:00","arr":"07:10","dur":"1h 10m","price":"PHP 2,500","status":"Scheduled"},
        {"airline":"Philippine Airlines","from":"Manila (MNL)","to":"Legazpi, Albay (LGP)","dep":"07:30","arr":"08:40","dur":"1h 10m","price":"PHP 2,200","status":"Scheduled"},
        {"airline":"Cebu Pacific","from":"Manila (MNL)","to":"Baguio (BAG)","dep":"08:00","arr":"08:50","dur":"50m","price":"PHP 1,800","status":"Scheduled"},
        {"airline":"Cebu Pacific","from":"Manila (MNL)","to":"Vigan, Ilocos Sur (VIG)","dep":"09:15","arr":"10:20","dur":"1h 05m","price":"PHP 2,000","status":"Scheduled"},
        {"airline":"AirAsia","from":"Manila (MNL)","to":"Tuguegarao, Cagayan (TUG)","dep":"10:00","arr":"11:10","dur":"1h 10m","price":"PHP 1,900","status":"Scheduled"},
        {"airline":"PAL Express","from":"Pampanga/Clark (CRK)","to":"Laoag, Ilocos Norte (LAO)","dep":"11:30","arr":"12:35","dur":"1h 05m","price":"PHP 2,300","status":"Scheduled"},
        {"airline":"Cebu Pacific","from":"Pampanga/Clark (CRK)","to":"Legazpi, Albay (LGP)","dep":"13:00","arr":"14:10","dur":"1h 10m","price":"PHP 2,100","status":"Scheduled"},
        {"airline":"Philippine Airlines","from":"Laoag, Ilocos Norte (LAO)","to":"Manila (MNL)","dep":"15:00","arr":"16:10","dur":"1h 10m","price":"PHP 2,500","status":"Scheduled"},
        {"airline":"Cebu Pacific","from":"Legazpi, Albay (LGP)","to":"Manila (MNL)","dep":"16:30","arr":"17:40","dur":"1h 10m","price":"PHP 2,200","status":"Scheduled"},
        {"airline":"AirAsia","from":"Tuguegarao, Cagayan (TUG)","to":"Manila (MNL)","dep":"18:00","arr":"19:10","dur":"1h 10m","price":"PHP 1,900","status":"Scheduled"},
    ]
    # International: only MNL/CRK ↔ international
    INTL_ROUTES = [
        {"airline":"Philippine Airlines","from":"Manila (MNL)","to":"Tokyo Narita (NRT), Japan","dep":"08:00","arr":"13:30","dur":"4h 30m","price":"PHP 18,000","status":"Scheduled"},
        {"airline":"Philippine Airlines","from":"Manila (MNL)","to":"Singapore Changi (SIN)","dep":"09:30","arr":"12:00","dur":"3h 30m","price":"PHP 12,000","status":"Scheduled"},
        {"airline":"Cebu Pacific","from":"Manila (MNL)","to":"Dubai International (DXB), UAE","dep":"22:00","arr":"03:30+1","dur":"9h 30m","price":"PHP 22,000","status":"Scheduled"},
        {"airline":"AirAsia","from":"Manila (MNL)","to":"Kuala Lumpur (KUL), Malaysia","dep":"07:00","arr":"10:30","dur":"3h 30m","price":"PHP 9,500","status":"Scheduled"},
        {"airline":"Cebu Pacific","from":"Manila (MNL)","to":"Seoul Incheon (ICN), South Korea","dep":"10:00","arr":"15:00","dur":"4h","price":"PHP 15,000","status":"Scheduled"},
        {"airline":"Philippine Airlines","from":"Manila (MNL)","to":"Los Angeles (LAX), USA","dep":"23:30","arr":"20:00","dur":"15h 30m","price":"PHP 65,000","status":"Scheduled"},
        {"airline":"PAL Express","from":"Pampanga/Clark (CRK)","to":"Hong Kong (HKG)","dep":"08:30","arr":"11:00","dur":"2h 30m","price":"PHP 10,000","status":"Scheduled"},
        {"airline":"AirAsia","from":"Pampanga/Clark (CRK)","to":"Kuala Lumpur (KUL), Malaysia","dep":"11:00","arr":"14:30","dur":"3h 30m","price":"PHP 8,500","status":"Scheduled"},
        {"airline":"Philippine Airlines","from":"Tokyo Narita (NRT), Japan","to":"Manila (MNL)","dep":"15:00","arr":"19:00","dur":"4h","price":"PHP 18,000","status":"Scheduled"},
        {"airline":"Cebu Pacific","from":"Singapore Changi (SIN)","to":"Manila (MNL)","dep":"13:30","arr":"16:00","dur":"3h 30m","price":"PHP 12,000","status":"Scheduled"},
    ]
    AIRLINES = ["All","Philippine Airlines","Cebu Pacific","AirAsia","PAL Express"]
    sc_map = {"Scheduled":"#2563EB","On Time":"#16A34A","Delayed":"#D97706","Cancelled":"#DC2626"}

    def flight_row(f):
        status  = f.get("status","Scheduled")
        sc      = sc_map.get(status,"#2563EB")
        badge   = f'<span style="background:{sc}22;color:{sc};padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700">{status}</span>'
        return f'<tr><td style="font-weight:600;color:#1E293B">{f["airline"]}</td><td>{f["from"]}</td><td>{f["to"]}</td><td>{f["dep"]}</td><td>{f["arr"]}</td><td>{f["dur"]}</td><td style="color:#16A34A;font-weight:600">{f["price"]}</td><td>{badge}</td></tr>'

    dom_rows  = "".join(flight_row(f) for f in DOMESTIC_ROUTES)
    intl_rows = "".join(flight_row(f) for f in INTL_ROUTES)
    airline_opts = "".join(f'<option value="{a if a!="All" else ""}">{a}</option>' for a in AIRLINES)
    status_opts  = '<option value="">All Status</option><option value="Scheduled">Scheduled</option><option value="On Time">On Time</option><option value="Delayed">Delayed</option><option value="Cancelled">Cancelled</option>'

    def flight_filter(tbl_id):
        return f'''<div class="filter-bar">
          <div style="display:flex;align-items:center;gap:6px;background:#fff;border:1.5px solid #E2E8F0;border-radius:8px;padding:7px 12px;flex:1;max-width:220px">
            <input placeholder="Search airline or route..." oninput="applyFilters(\'{tbl_id}\',[{{col:0,value:this.value}},{{col:1,value:this.value}},{{col:2,value:this.value}}])" style="border:none;background:none;outline:none;font-size:13px;width:100%;margin:0"/>
          </div>
          <select onchange="applyFilters(\'{tbl_id}\',[{{col:0,value:this.value}}])" style="margin:0;width:auto;padding:7px 10px;font-size:12px">{airline_opts}</select>
          <select onchange="applyFilters(\'{tbl_id}\',[{{col:7,value:this.value}}])" style="margin:0;width:auto;padding:7px 10px;font-size:12px">{status_opts}</select>
        </div>'''

    tab_btns = (
        f'<button class="tab-btn active" data-tab="domestic" onclick="switchTab(\'flights\',\'domestic\')">Domestic ({len(DOMESTIC_ROUTES)})</button>'
        f'<button class="tab-btn" data-tab="intl" onclick="switchTab(\'flights\',\'intl\')">International ({len(INTL_ROUTES)})</button>'
    )

    body = f'''
    <div style="font-size:22px;font-weight:800;margin-bottom:4px">Flights</div>
    <div style="font-size:13px;color:#94A3B8;margin-bottom:20px">{len(DOMESTIC_ROUTES)} domestic · {len(INTL_ROUTES)} international Luzon routes</div>
    {_alert(msg,err)}
    <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:10px;padding:12px 16px;font-size:13px;color:#1D4ED8;margin-bottom:16px">
      <i class=&#34;fa-regular fa-clipboard&#34;></i> Domestic: Luzon airports (MNL, CRK) to/from Luzon destinations. International: MNL/CRK to/from major international airports.
    </div>
    <div class="card"><div style="padding:0 20px" data-group="flights">
      <div class="tabs">{tab_btns}</div>
      <div id="flights-domestic" class="tab-pane active">
        {flight_filter("tbl-dom")}
        <div style="padding:0 16px 8px;display:flex;justify-content:flex-end">{_export_btns("tbl-dom","ATLAS_Domestic_Flights")}</div>
        <table id="tbl-dom"><thead><tr><th>Airline</th><th>From</th><th>To</th><th>Departs</th><th>Arrives</th><th>Duration</th><th>Price</th><th>Status</th></tr></thead>
        <tbody>{dom_rows}</tbody></table>
      </div>
      <div id="flights-intl" class="tab-pane">
        {flight_filter("tbl-intl")}
        <div style="padding:0 16px 8px;display:flex;justify-content:flex-end">{_export_btns("tbl-intl","ATLAS_International_Flights")}</div>
        <table id="tbl-intl"><thead><tr><th>Airline</th><th>From</th><th>To</th><th>Departs</th><th>Arrives</th><th>Duration</th><th>Price</th><th>Status</th></tr></thead>
        <tbody>{intl_rows}</tbody></table>
      </div>
    </div></div>'''
    return shell("Flights", body, "flights", admin)

def profile_page(admin, msg="", err=""):
    ainit   = (admin.get("fullname","A") or "A")[0].upper()
    aname   = admin.get("fullname","ATLAS Administrator")
    aemail  = admin.get("email","admin@atlas.ph")
    created = (admin.get("created","") or "")[:10]

    body = f'''
    <div style="font-size:22px;font-weight:800;margin-bottom:4px">Admin Profile</div>
    <div style="font-size:13px;color:#94A3B8;margin-bottom:20px">Your account information</div>
    {_alert(msg,err)}
    <div style="display:grid;grid-template-columns:280px 1fr;gap:20px;align-items:start">
      <div class="card"><div class="card-body" style="text-align:center;padding:32px 20px">
        <div style="width:80px;height:80px;background:linear-gradient(135deg,#0038A8,#CE1126);border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:32px;margin:0 auto 16px">{ainit}</div>
        <div style="font-size:18px;font-weight:800;margin-bottom:4px">{aname}</div>
        <div style="font-size:13px;color:#94A3B8;margin-bottom:10px">{aemail}</div>
        <span class=bb>Admin</span>
        <div style="height:1px;background:#F1F5F9;margin:18px 0"></div>
        <div style="text-align:left;display:flex;flex-direction:column;gap:10px">
          <div style="display:flex;justify-content:space-between;font-size:13px"><span style="color:#94A3B8;font-weight:600">Role</span><span style="font-weight:700">Admin</span></div>
          <div style="display:flex;justify-content:space-between;font-size:13px"><span style="color:#94A3B8;font-weight:600">Member since</span><span style="font-weight:700">{created}</span></div>
          <div style="display:flex;justify-content:space-between;font-size:13px"><span style="color:#94A3B8;font-weight:600">System</span><span style="font-weight:700">ATLAS v1.0</span></div>
        </div>
      </div></div>
      <div class="card">
        <div class="card-hdr"><h3>Change Password</h3></div>
        <div class="card-body">
          <div style="background:#FEF9C3;border:1px solid #FDE047;border-radius:8px;padding:10px 14px;font-size:13px;color:#854D0E;margin-bottom:16px">&#9432; Only password changes are allowed for security.</div>
          <form method="post" action="/admin/profile/update">
            <div class="fg2">
              <div><label>New Password</label><input name="new_password" type="password" placeholder="Min. 8 characters"/></div>
              <div><label>Confirm Password</label><input name="confirm_password" type="password" placeholder="Repeat password"/></div>
            </div>
            <button class="btn bprimary" type="submit" style="padding:10px 24px;font-size:13px">Change Password</button>
          </form>
        </div>
      </div>
    </div>'''
    return shell("Admin Profile", body, "profile", admin)
