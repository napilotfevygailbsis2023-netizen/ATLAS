import sqlite3
import uuid
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'atlas.db')

def get_conn():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_flight_booking_tables():
    """Initialize flight booking tables"""
    conn = get_conn()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS flight_bookings (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            flight_number TEXT NOT NULL,
            airline TEXT NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time DATETIME NOT NULL,
            arrival_time DATETIME NOT NULL,
            price TEXT NOT NULL,
            passengers INTEGER DEFAULT 1,
            passenger_names TEXT,
            contact_email TEXT NOT NULL,
            contact_phone TEXT,
            status TEXT DEFAULT 'confirmed',
            booking_reference TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def generate_booking_reference():
    """Generate unique booking reference"""
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def create_flight_booking(user_id, flight_data, passenger_info):
    """Create a new flight booking"""
    try:
        booking_id = str(uuid.uuid4())
        booking_ref = generate_booking_reference()
        
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO flight_bookings 
            (id, user_id, flight_number, airline, origin, destination, 
             departure_time, arrival_time, price, passengers, passenger_names,
             contact_email, contact_phone, status, booking_reference)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            booking_id, user_id, flight_data.get('flight_number', ''),
            flight_data['airline'], flight_data['origin'], flight_data['destination'],
            flight_data['departure_time'], flight_data['arrival_time'],
            flight_data['price'], passenger_info['passengers'],
            passenger_info['passenger_names'], passenger_info['email'],
            passenger_info['phone'], 'confirmed', booking_ref
        ))
        
        conn.commit()
        conn.close()
        return booking_id, booking_ref
        
    except Exception as e:
        print(f"Error creating flight booking: {e}")
        return None, None

def get_user_flight_bookings(user_id):
    """Get all flight bookings for a user"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT * FROM flight_bookings 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        """, (user_id,))
        
        bookings = cur.fetchall()
        conn.close()
        return [dict(row) for row in bookings]
        
    except Exception as e:
        print(f"Error getting flight bookings: {e}")
        return []

def get_flight_booking(booking_id):
    """Get a specific flight booking"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT * FROM flight_bookings 
            WHERE id = ?
        """, (booking_id,))
        
        booking = cur.fetchone()
        conn.close()
        return dict(booking) if booking else None
        
    except Exception as e:
        print(f"Error getting flight booking: {e}")
        return None

def update_booking_status(booking_id, status):
    """Update flight booking status"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE flight_bookings 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, booking_id))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error updating booking status: {e}")
        return False

# Initialize tables on import
init_flight_booking_tables()

        
# SweetAlert functions for flight booking
def render_sweetalert_functions():
    return '''
<script>
function confirmFlightBooking(flightNumber) {
    Swal.fire({
        title: 'Confirm Flight Booking?',
        text: 'Are you sure you want to book flight ' + flightNumber + '?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#0038A8',
        cancelButtonColor: '#6B7280',
        confirmButtonText: 'Yes, book now'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('flight-booking-form').submit();
        }
    });
}

function showBookingSuccess(reference) {
    Swal.fire({
        title: 'Booking Confirmed!',
        text: 'Your flight has been booked. Reference: ' + reference,
        icon: 'success',
        timer: 3000,
        showConfirmButton: false
    });
}

function showBookingError(message) {
    Swal.fire({
        title: 'Booking Failed',
        text: message,
        icon: 'error'
    });
}
</script>
'''
