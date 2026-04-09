#!/usr/bin/env python3
"""
Add SweetAlert to key pages and actions
"""

import os
import re

def add_sweetalert_to_file(filepath, find_text, replace_text):
    """Add SweetAlert to a specific file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        if find_text in content:
            content = content.replace(find_text, replace_text)
            
            with open(filepath, 'w') as f:
                f.write(content)
            
            print(f"Updated {filepath}")
            return True
        else:
            print(f"Pattern not found in {filepath}")
            return False
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    """Add SweetAlert to important pages"""
    
    # Add SweetAlert to profile page
    profile_sweetalert = """
    <script>
    function confirmDeleteAccount() {
        Swal.fire({
            title: 'Delete Account?',
            text: 'This action cannot be undone. All your data will be permanently deleted.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#CE1126',
            cancelButtonColor: '#6B7280',
            confirmButtonText: 'Yes, delete account'
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '/profile/delete-account';
            }
        });
    }
    </script>
    """
    
    # Add SweetAlert to booking confirmation
    booking_sweetalert = """
    <script>
    function confirmBooking(guideName) {
        Swal.fire({
            title: 'Confirm Booking?',
            text: 'Are you sure you want to book ' + guideName + '?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#0038A8',
            cancelButtonColor: '#6B7280',
            confirmButtonText: 'Yes, book now'
        }).then((result) => {
            if (result.isConfirmed) {
                // Submit booking form
                document.getElementById('booking-form').submit();
            }
        });
    }
    </script>
    """
    
    # Update guides.py to use SweetAlert for booking
    if os.path.exists('guides.py'):
        with open('guides.py', 'r') as f:
            guides_content = f.read()
        
        # Replace confirmBooking function
        guides_content = re.sub(
            r'function confirmBooking\(\)\{.*?\}',
            '''function confirmBooking(name) {
                Swal.fire({
                    title: 'Confirm Booking?',
                    text: 'Are you sure you want to book ' + name + '?',
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonColor: '#0038A8',
                    cancelButtonColor: '#6B7280',
                    confirmButtonText: 'Yes, book now'
                }).then((result) => {
                    if (result.isConfirmed) {
                        closeBooking();
                        showSuccess('Booking Confirmed!', 'Your booking request has been sent to ' + name + '.');
                    }
                });
            }''',
            guides_content,
            flags=re.DOTALL
        )
        
        with open('guides.py', 'w') as f:
            f.write(guides_content)
        
        print("Updated guides.py with SweetAlert")
    
    # Add SweetAlert to flight booking
    if os.path.exists('flight_booking_sqlite.py'):
        with open('flight_booking_sqlite.py', 'r') as f:
            flight_content = f.read()
        
        # Add SweetAlert functions to flight booking
        flight_content += """
        
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
"""
        
        with open('flight_booking_sqlite.py', 'w') as f:
            f.write(flight_content)
        
        print("Updated flight_booking_sqlite.py with SweetAlert")
    
    print("SweetAlert integration complete!")

if __name__ == "__main__":
    main()
