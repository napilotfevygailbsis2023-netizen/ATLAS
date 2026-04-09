import sys, os, datetime, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guide_db_sqlite as guide_db

def validate_guide_permit(guide_id, permit_number, permit_expiry, permit_document):
    """Validate tour guide permit"""
    try:
        conn = guide_db.get_conn()
        cur = conn.cursor()
        
        # Check if permit number is valid format (basic validation)
        if not permit_number or len(permit_number) < 5:
            return False, "Invalid permit number format"
        
        # Check expiry date
        if permit_expiry:
            expiry_date = datetime.datetime.strptime(permit_expiry, '%Y-%m-%d').date()
            if expiry_date < datetime.date.today():
                return False, "Permit has expired"
        
        # Update guide record with permit information
        cur.execute("""
            UPDATE tour_guides 
            SET permit_number = %s, permit_expiry = %s, permit_document = %s
            WHERE id = %s
        """, (permit_number, permit_expiry, permit_document, guide_id))
        
        conn.commit()
        conn.close()
        return True, "Permit information updated successfully"
        
    except Exception as e:
        print(f"Error validating permit: {e}")
        return False, f"Error validating permit: {str(e)}"

def validate_guide_license(guide_id, license_number, license_expiry, license_document):
    """Validate tour guide license"""
    try:
        conn = guide_db.get_conn()
        cur = conn.cursor()
        
        # Check if license number is valid format (basic validation)
        if not license_number or len(license_number) < 5:
            return False, "Invalid license number format"
        
        # Check expiry date
        if license_expiry:
            expiry_date = datetime.datetime.strptime(license_expiry, '%Y-%m-%d').date()
            if expiry_date < datetime.date.today():
                return False, "License has expired"
        
        # Update guide record with license information
        cur.execute("""
            UPDATE tour_guides 
            SET license_number = %s, license_expiry = %s, license_document = %s
            WHERE id = %s
        """, (license_number, license_expiry, license_document, guide_id))
        
        conn.commit()
        conn.close()
        return True, "License information updated successfully"
        
    except Exception as e:
        print(f"Error validating license: {e}")
        return False, f"Error validating license: {str(e)}"

def update_verification_status(guide_id, status, admin_notes=""):
    """Update guide verification status"""
    try:
        conn = guide_db.get_conn()
        cur = conn.cursor()
        
        valid_statuses = ['pending', 'verified', 'rejected', 'suspended']
        if status not in valid_statuses:
            return False, "Invalid verification status"
        
        cur.execute("""
            UPDATE tour_guides 
            SET verification_status = %s
            WHERE id = %s
        """, (status, guide_id))
        
        conn.commit()
        conn.close()
        return True, f"Verification status updated to {status}"
        
    except Exception as e:
        print(f"Error updating verification status: {e}")
        return False, f"Error updating verification status: {str(e)}"

def get_guide_verification_details(guide_id):
    """Get guide verification details"""
    try:
        conn = guide_db.get_conn()
        cur = conn.cursor(dictionary=True)
        
        cur.execute("""
            SELECT id, fname, lname, email, permit_number, permit_expiry, 
                   license_number, license_expiry, verification_status,
                   permit_document, license_document
            FROM tour_guides 
            WHERE id = %s
        """, (guide_id,))
        
        guide = cur.fetchone()
        conn.close()
        return guide
        
    except Exception as e:
        print(f"Error getting verification details: {e}")
        return None

def check_guide_legitimacy(guide_id):
    """Check if guide is legitimate (has valid permits/licenses)"""
    try:
        guide = get_guide_verification_details(guide_id)
        if not guide:
            return False, "Guide not found"
        
        # Check verification status
        if guide['verification_status'] != 'verified':
            return False, f"Guide verification status: {guide['verification_status']}"
        
        # Check permit expiry
        if guide['permit_expiry']:
            permit_expiry = datetime.datetime.strptime(guide['permit_expiry'], '%Y-%m-%d').date()
            if permit_expiry < datetime.date.today():
                return False, "Guide permit has expired"
        
        # Check license expiry
        if guide['license_expiry']:
            license_expiry = datetime.datetime.strptime(guide['license_expiry'], '%Y-%m-%d').date()
            if license_expiry < datetime.date.today():
                return False, "Guide license has expired"
        
        return True, "Guide is verified and legitimate"
        
    except Exception as e:
        print(f"Error checking guide legitimacy: {e}")
        return False, f"Error checking guide legitimacy: {str(e)}"

def get_all_pending_verifications():
    """Get all guides pending verification"""
    try:
        conn = guide_db.get_conn()
        cur = conn.cursor(dictionary=True)
        
        cur.execute("""
            SELECT id, fname, lname, email, city, created, verification_status
            FROM tour_guides 
            WHERE verification_status = 'pending'
            ORDER BY created ASC
        """)
        
        guides = cur.fetchall()
        conn.close()
        return guides
        
    except Exception as e:
        print(f"Error getting pending verifications: {e}")
        return []

def get_verified_guides():
    """Get all verified guides"""
    try:
        conn = guide_db.get_conn()
        cur = conn.cursor(dictionary=True)
        
        cur.execute("""
            SELECT id, fname, lname, email, city, verification_status,
                   permit_number, permit_expiry, license_number, license_expiry
            FROM tour_guides 
            WHERE verification_status = 'verified'
            ORDER BY fname, lname
        """)
        
        guides = cur.fetchall()
        conn.close()
        return guides
        
    except Exception as e:
        print(f"Error getting verified guides: {e}")
        return []

def render_verification_badge(verification_status):
    """Render verification status badge"""
    badges = {
        'verified': ('&#10003;', '#059669', '#ECFDF5'),
        'pending': ('&#128197;', '#D97706', '#FFFBEB'),
        'rejected': ('&#10060;', '#DC2626', '#FEF2F2'),
        'suspended': ('&#9888;', '#7C2D12', '#FEF3C7')
    }
    
    icon, color, bg = badges.get(verification_status, ('&#63;', '#6B7280', '#F9FAFB'))
    
    return f'<span style="background:{bg};color:{color};padding:2px 8px;border-radius:12px;font-size:11px;font-weight:600">{icon} {verification_status.title()}</span>'

def check_expiry_alerts():
    """Check for permits/licenses expiring soon (within 30 days)"""
    try:
        conn = guide_db.get_conn()
        cur = conn.cursor(dictionary=True)
        
        alert_date = datetime.date.today() + datetime.timedelta(days=30)
        
        cur.execute("""
            SELECT id, fname, lname, email, permit_expiry, license_expiry
            FROM tour_guides 
            WHERE verification_status = 'verified'
            AND (permit_expiry <= %s OR license_expiry <= %s)
            ORDER BY permit_expiry, license_expiry
        """, (alert_date, alert_date))
        
        expiring = cur.fetchall()
        conn.close()
        return expiring
        
    except Exception as e:
        print(f"Error checking expiry alerts: {e}")
        return []
