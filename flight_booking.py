import sys, os, datetime, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build_shell
import db

def init_flight_booking_tables():
    """Initialize flight booking tables"""
    try:
        conn = db.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS flight_bookings (
                id VARCHAR(36) PRIMARY KEY,
                user_id INT NOT NULL,
                flight_number VARCHAR(20) NOT NULL,
                airline VARCHAR(100) NOT NULL,
                origin VARCHAR(200) NOT NULL,
                destination VARCHAR(200) NOT NULL,
                departure_time DATETIME NOT NULL,
                arrival_time DATETIME NOT NULL,
                price VARCHAR(50) NOT NULL,
                passengers INT DEFAULT 1,
                passenger_names TEXT,
                contact_email VARCHAR(255) NOT NULL,
                contact_phone VARCHAR(50),
                status VARCHAR(20) DEFAULT 'confirmed',
                booking_reference VARCHAR(20) UNIQUE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error initializing flight booking tables: {e}")
        return False

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
        
        conn = db.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO flight_bookings 
            (id, user_id, flight_number, airline, origin, destination, 
             departure_time, arrival_time, price, passengers, passenger_names,
             contact_email, contact_phone, status, booking_reference)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        conn = db.get_conn()
        cur = conn.cursor(dictionary=True)
        
        cur.execute("""
            SELECT * FROM flight_bookings 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """, (user_id,))
        
        bookings = cur.fetchall()
        conn.close()
        return bookings
    except Exception as e:
        print(f"Error getting flight bookings: {e}")
        return []

def get_flight_booking(booking_id):
    """Get a specific flight booking"""
    try:
        conn = db.get_conn()
        cur = conn.cursor(dictionary=True)
        
        cur.execute("""
            SELECT * FROM flight_bookings 
            WHERE id = %s
        """, (booking_id,))
        
        booking = cur.fetchone()
        conn.close()
        return booking
    except Exception as e:
        print(f"Error getting flight booking: {e}")
        return None

def update_booking_status(booking_id, status):
    """Update flight booking status"""
    try:
        conn = db.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE flight_bookings 
            SET status = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (status, booking_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating booking status: {e}")
        return False

def render_booking_confirmation(booking_id, user=None):
    """Render flight booking confirmation page"""
    booking = get_flight_booking(booking_id)
    if not booking:
        return build_shell("Booking Not Found", 
            '<div class="page-wrap"><div class="card"><div class="card-body" style="text-align:center;padding:40px"><div style="font-size:40px;margin-bottom:16px">&#128533;</div><div style="font-size:18px;font-weight:700;margin-bottom:12px">Booking Not Found</div><div style="color:#6B7280">The booking you are looking for does not exist.</div></div></div></div>', 
            "home", user=user)

    status_colors = {
        'confirmed': '#059669',
        'pending': '#D97706',
        'cancelled': '#DC2626',
        'completed': '#7C3AED'
    }
    
    status_bg = {
        'confirmed': '#ECFDF5',
        'pending': '#FFFBEB',
        'cancelled': '#FEF2F2',
        'completed': '#F5F3FF'
    }
    
    status_color = status_colors.get(booking['status'], '#6B7280')
    status_bg_color = status_bg.get(booking['status'], '#F9FAFB')
    
    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Flight Booking Confirmation</div>
        <div class="section-sub">Your flight has been successfully booked</div>
      </div>
      
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#059669">
          <span>&#10003; Booking Confirmed</span>
        </div>
        <div class="card-body">
          <div style="text-align:center;margin-bottom:20px">
            <div style="font-size:48px;margin-bottom:12px">&#9992;</div>
            <div style="font-size:24px;font-weight:800;color:#059669;margin-bottom:8px">Booking Reference</div>
            <div style="font-size:20px;font-weight:700;background:#F3F4F6;padding:12px 20px;border-radius:8px;display:inline-block">{booking['booking_reference']}</div>
          </div>
          
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px">
            <div>
              <div style="font-size:12px;color:#6B7280;margin-bottom:4px">Flight Number</div>
              <div style="font-weight:700;font-size:16px">{booking['flight_number'] or 'TBD'}</div>
            </div>
            <div>
              <div style="font-size:12px;color:#6B7280;margin-bottom:4px">Airline</div>
              <div style="font-weight:700;font-size:16px">{booking['airline']}</div>
            </div>
            <div>
              <div style="font-size:12px;color:#6B7280;margin-bottom:4px">Departure</div>
              <div style="font-weight:700;font-size:16px">{booking['origin']}</div>
              <div style="color:#6B7280;font-size:13px">{booking['departure_time'].strftime('%Y-%m-%d %H:%M') if isinstance(booking['departure_time'], datetime.datetime) else booking['departure_time']}</div>
            </div>
            <div>
              <div style="font-size:12px;color:#6B7280;margin-bottom:4px">Arrival</div>
              <div style="font-weight:700;font-size:16px">{booking['destination']}</div>
              <div style="color:#6B7280;font-size:13px">{booking['arrival_time'].strftime('%Y-%m-%d %H:%M') if isinstance(booking['arrival_time'], datetime.datetime) else booking['arrival_time']}</div>
            </div>
          </div>
          
          <div style="display:flex;justify-content:space-between;align-items:center;padding-top:16px;border-top:1px solid #E5E7EB">
            <div>
              <div style="font-size:12px;color:#6B7280;margin-bottom:4px">Total Price</div>
              <div style="font-size:20px;font-weight:800;color:#0038A8">{booking['price']}</div>
            </div>
            <div style="text-align:right">
              <div style="font-size:12px;color:#6B7280;margin-bottom:4px">Status</div>
              <div style="background:{status_bg_color};color:{status_color};padding:4px 12px;border-radius:20px;font-size:12px;font-weight:700;display:inline-block">{booking['status'].title()}</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card">
        <div class="card-hdr" style="background:#0038A8">
          <span>Passenger Information</span>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
            <div>
              <div style="font-size:12px;color:#6B7280;margin-bottom:4px">Passengers</div>
              <div style="font-weight:700">{booking['passengers']}</div>
            </div>
            <div>
              <div style="font-size:12px;color:#6B7280;margin-bottom:4px">Contact Email</div>
              <div style="font-weight:700">{booking['contact_email']}</div>
            </div>
            <div>
              <div style="font-size:12px;color:#6B7280;margin-bottom:4px">Contact Phone</div>
              <div style="font-weight:700">{booking['contact_phone'] or 'Not provided'}</div>
            </div>
            <div>
              <div style="font-size:12px;color:#6B7280;margin-bottom:4px">Booking Date</div>
              <div style="font-weight:700">{booking['created_at'].strftime('%Y-%m-%d %H:%M') if isinstance(booking['created_at'], datetime.datetime) else booking['created_at']}</div>
            </div>
          </div>
          
          {f'<div style="margin-top:16px;padding-top:16px;border-top:1px solid #E5E7EB"><div style="font-size:12px;color:#6B7280;margin-bottom:8px">Passenger Names</div><div style="font-size:13px;line-height:1.5">{booking["passenger_names"]}</div></div>' if booking['passenger_names'] else ''}
        </div>
      </div>
      
      <div style="margin-top:24px;display:flex;gap:12px">
        <button class="btn" style="background:#0038A8;color:#fff;flex:1" onclick="window.print()">
          <i class="fa-solid fa-print"></i> Print Confirmation
        </button>
        <a href="/profile.py" class="btn-outline" style="flex:1;text-decoration:none;display:block;text-align:center">
          View All Bookings
        </a>
      </div>
    </div>"""
    
    return build_shell("Flight Booking Confirmation", body, "booking-confirmation", user=user)

def render_flight_booking_form(flight_data, user=None):
    """Render flight booking form"""
    if not user:
        return build_shell("Login Required", 
            '<div class="page-wrap"><div class="card"><div class="card-body" style="text-align:center;padding:40px"><div style="font-size:40px;margin-bottom:16px">&#128100;</div><div style="font-size:18px;font-weight:700;margin-bottom:12px">Login Required</div><div style="color:#6B7280;margin-bottom:20px">Please log in to book flights</div><a href="/login.py"><button class="btn" style="background:#0038A8;color:#fff">Log In</button></a></div></div></div>', 
            "home", user=None)

    body = f"""
    <div class="page-wrap">
      <div style="margin-bottom:22px">
        <div class="section-title">Complete Your Booking</div>
        <div class="section-sub">Review flight details and provide passenger information</div>
      </div>
      
      <div class="card" style="margin-bottom:20px">
        <div class="card-hdr" style="background:#0038A8">
          <span>Flight Details</span>
        </div>
        <div class="card-body">
          <div style="display:flex;align-items:center;gap:16px;margin-bottom:16px">
            <div style="font-size:32px">&#9992;</div>
            <div style="flex:1">
              <div style="font-weight:800;font-size:18px;margin-bottom:4px">{flight_data['airline']}</div>
              <div style="color:#6B7280">{flight_data['flight_number'] or 'Flight Number TBD'}</div>
            </div>
          </div>
          
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
            <div>
              <div style="font-size:12px;color:#6B7280;margin-bottom:4px">From</div>
              <div style="font-weight:700">{flight_data['origin']}</div>
              <div style="color:#6B7280;font-size:13px">{flight_data['dep']}</div>
            </div>
            <div>
              <div style="font-size:12px;color:#6B7280;margin-bottom:4px">To</div>
              <div style="font-weight:700">{flight_data['destination']}</div>
              <div style="color:#6B7280;font-size:13px">{flight_data['arr']}</div>
            </div>
          </div>
          
          <div style="margin-top:16px;padding-top:16px;border-top:1px solid #E5E7EB">
            <div style="font-size:20px;font-weight:800;color:#0038A8">{flight_data['price']}</div>
          </div>
        </div>
      </div>
      
      <div class="card">
        <div class="card-hdr" style="background:#0038A8">
          <span>Passenger Information</span>
        </div>
        <div class="card-body">
          <form method="post" action="/book-flight" style="display:flex;flex-direction:column;gap:16px">
            <input type="hidden" name="flight_data" value='{flight_data}'/>
            
            <div class="form-row">
              <div>
                <label class="lbl">Number of Passengers</label>
                <select class="inp" name="passengers" id="passengers" onchange="updatePassengerFields()">
                  <option value="1">1 Passenger</option>
                  <option value="2">2 Passengers</option>
                  <option value="3">3 Passengers</option>
                  <option value="4">4 Passengers</option>
                  <option value="5">5+ Passengers</option>
                </select>
              </div>
              <div>
                <label class="lbl">Contact Email</label>
                <input class="inp" type="email" name="email" value="{user.get('email', '')}" required/>
              </div>
            </div>
            
            <div>
              <label class="lbl">Contact Phone</label>
              <input class="inp" type="tel" name="phone" placeholder="09XX-XXX-XXXX"/>
            </div>
            
            <div id="passenger-names-container">
              <label class="lbl">Passenger Name(s)</label>
              <div id="passenger-fields">
                <input class="inp" type="text" name="passenger_name_1" placeholder="Passenger 1 Full Name" required/>
              </div>
            </div>
            
            <div style="background:#FFFBEB;border-left:3px solid #C8930A;padding:12px;border-radius:6px">
              <div style="font-size:12px;color:#92400E;font-weight:700;margin-bottom:4px">&#9888; Important</div>
              <div style="font-size:12px;color:#92400E">Please ensure all passenger names match government-issued IDs exactly as they appear.</div>
            </div>
            
            <div style="display:flex;gap:12px;margin-top:20px">
              <button type="submit" class="btn" style="background:#059669;color:#fff;flex:1;font-weight:700">
                <i class="fa-solid fa-check"></i> Complete Booking
              </button>
              <button type="button" class="btn-outline" style="flex:1" onclick="history.back()">
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <script>
    function updatePassengerFields() {{
      const count = parseInt(document.getElementById('passengers').value);
      const container = document.getElementById('passenger-fields');
      container.innerHTML = '';
      
      for (let i = 1; i <= count; i++) {{
        const input = document.createElement('input');
        input.type = 'text';
        input.name = 'passenger_name_' + i;
        input.placeholder = 'Passenger ' + i + ' Full Name';
        input.className = 'inp';
        input.required = true;
        input.style.marginBottom = '8px';
        container.appendChild(input);
      }}
    }}
    </script>"""
    
    return build_shell("Flight Booking", body, "flight-booking", user=user)

def handle_flight_booking(form_data, user):
    """Handle flight booking submission"""
    if not user:
        return None, render_flight_booking_form({}, user=None)
    
    try:
        import json
        flight_data = json.loads(form_data.get('flight_data', '{}'))
        
        passengers = int(form_data.get('passengers', 1))
        email = form_data.get('email', '').strip()
        phone = form_data.get('phone', '').strip()
        
        # Collect passenger names
        passenger_names = []
        for i in range(1, passengers + 1):
            name = form_data.get(f'passenger_name_{i}', '').strip()
            if name:
                passenger_names.append(name)
        
        if not email or not passenger_names:
            return None, render_flight_booking_form(flight_data, user)
        
        # Prepare flight data for database
        flight_booking_data = {
            'flight_number': flight_data.get('flight_number', ''),
            'airline': flight_data['airline'],
            'origin': flight_data['from'],
            'destination': flight_data['to'],
            'departure_time': datetime.datetime.now(),  # This should come from flight data
            'arrival_time': datetime.datetime.now(),    # This should come from flight data
            'price': flight_data['price']
        }
        
        passenger_info = {
            'passengers': passengers,
            'passenger_names': ', '.join(passenger_names),
            'email': email,
            'phone': phone
        }
        
        booking_id, booking_ref = create_flight_booking(user['id'], flight_booking_data, passenger_info)
        
        if booking_id:
            return f"/booking-confirmation/{booking_id}", None
        else:
            return None, render_flight_booking_form(flight_data, user)
            
    except Exception as e:
        print(f"Error handling flight booking: {e}")
        return None, render_flight_booking_form({}, user)
