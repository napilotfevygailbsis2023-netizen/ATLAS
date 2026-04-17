"""
Run this FROM your project folder:  python3 diagnose.py
It will tell you exactly what's in the DB and where the booking flow breaks.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import guide_db
    conn = guide_db.get_conn()
    cur  = conn.cursor(dictionary=True)
    print("=" * 60)
    print("DB CONNECTION: OK")
    print("=" * 60)

    # 1. All guides and their status
    cur.execute("SELECT id, fname, lname, status, email FROM tour_guides ORDER BY id")
    guides = cur.fetchall()
    print(f"\n[1] GUIDES IN DB ({len(guides)} total):")
    for g in guides:
        print(f"    id={g['id']}  name={g['fname']} {g['lname']}  status={g['status']}  email={g['email']}")
    if not guides:
        print("    *** NO GUIDES FOUND — guides table is empty ***")

    # 2. Active guides (what tourists can see)
    cur.execute("SELECT id, fname, lname FROM tour_guides WHERE status='active'")
    active = cur.fetchall()
    print(f"\n[2] ACTIVE GUIDES (visible to tourists): {len(active)}")
    for g in active:
        print(f"    id={g['id']}  {g['fname']} {g['lname']}")
    if not active:
        print("    *** NO ACTIVE GUIDES — tourists see empty list, guide_id will be empty! ***")
        print("    FIX: UPDATE tour_guides SET status='active' WHERE id=<id>;")

    # 3. All bookings
    cur.execute("SELECT id, guide_id, tourist_name, tourist_email, tour_date, status, created FROM bookings ORDER BY id DESC LIMIT 20")
    bookings = cur.fetchall()
    print(f"\n[3] BOOKINGS IN DB ({len(bookings)} shown, most recent first):")
    for b in bookings:
        print(f"    id={b['id']}  guide_id={b['guide_id']}  tourist={b['tourist_name']}  date={b['tour_date']}  status={b['status']}  created={b['created']}")
    if not bookings:
        print("    *** NO BOOKINGS FOUND — either none were saved, or guide_id was 0 ***")

    # 4. Check guide_id mismatch
    if bookings and guides:
        guide_ids = {g['id'] for g in guides}
        for b in bookings:
            if b['guide_id'] not in guide_ids:
                print(f"    *** MISMATCH: booking id={b['id']} has guide_id={b['guide_id']} which doesn't exist in tour_guides! ***")

    # 5. Bookings per guide
    print(f"\n[4] BOOKINGS PER GUIDE:")
    for g in guides:
        cur.execute("SELECT COUNT(*) as cnt FROM bookings WHERE guide_id=%s", (g['id'],))
        cnt = cur.fetchone()['cnt']
        print(f"    guide_id={g['id']} ({g['fname']} {g['lname']}): {cnt} booking(s)")

    # 6. Sessions — check if guide is actually logged in
    cur.execute("SELECT s.token, s.guide_id, s.created, g.fname, g.lname FROM guide_sessions s JOIN tour_guides g ON g.id=s.guide_id ORDER BY s.created DESC LIMIT 5")
    sessions = cur.fetchall()
    print(f"\n[5] ACTIVE GUIDE SESSIONS (last 5):")
    for s in sessions:
        print(f"    guide_id={s['guide_id']} ({s['fname']} {s['lname']})  created={s['created']}")
    if not sessions:
        print("    *** NO GUIDE SESSIONS — guide is not logged in ***")

    cur.close(); conn.close()
    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)

except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
