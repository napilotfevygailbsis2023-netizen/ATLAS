#!/usr/bin/env python3
"""
Script to update main.py routes to include new features
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def update_main_routes():
    """Update main.py to include new route handlers"""
    
    # Read current main.py
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Add new imports
    import_section = """
import index, flights, weather, attractions, restaurants, guides, transport, itinerary
import login, register, db
import admin_login, admin_panel, admin_db
import guide_portal
import profile as profile_page, guide_db
import flight_booking, setup_2fa, guide_verification, system_messaging"""
    
    # Replace import section
    old_import = "import index, flights, weather, attractions, restaurants, guides, transport, itinerary"
    if old_import in content:
        content = content.replace(old_import, import_section)
    
    # Add new routes
    new_routes = """
    "/setup-2fa":      lambda p, u: setup_2fa.render(u) if u else setup_2fa.render(),
    "/book-flight":    lambda p, u: flight_booking.handle_flight_booking(p, u) if u else None,
    "/booking-confirmation": lambda p, u: flight_booking.render_booking_confirmation(p.get('id', ''), u) if u else None,
    "/guide-verification": lambda p, u: guide_verification.render_verification_panel(u) if u else None,
    "/system-messages": lambda p, u: system_messaging.render_thread_list(u['id']) if u else None,"""
    
    # Find ROUTES dictionary and add new routes
    if 'ROUTES = {' in content:
        routes_start = content.find('ROUTES = {')
        routes_end = content.find('\n}', routes_start) + 2
        
        existing_routes = content[routes_start:routes_end]
        
        # Add new routes before closing brace
        if '"/profile.py":' in existing_routes:
            updated_routes = existing_routes.replace(
                '"/profile.py":     lambda p, u: profile_page.render(user=u),',
                '"/profile.py":     lambda p, u: profile_page.render(user=u),\n' + new_routes
            )
            content = content.replace(existing_routes, updated_routes)
    
    # Write updated content
    with open('main.py', 'w') as f:
        f.write(content)
    
    print("Updated main.py with new routes")

def update_login_handler():
    """Update login handler to support 2FA"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the login handler section
    if 'if path == "/login.py" and method == "POST":' in content:
        # Add 2FA handling logic
        two_fa_handler = """
        # Check if this is 2FA verification
        if "totp_token" in form_data:
            result, html = login.handle_post(form_data)
            if isinstance(result, str) and result.startswith("2FA_REQUIRED:"):
                # Store temp session and show 2FA form
                parts = result.split(":")
                temp_token, user_id = parts[1], parts[2]
                # In production, store this in Redis or database
                return send_html(handler, html, cookie=f"temp_2fa={temp_token}; path=/; HttpOnly")
            elif result:  # Successful 2FA verification
                return redirect(handler, "/", cookie=f"atlas_token={result}; path=/; HttpOnly")
            else:  # 2FA failed
                return send_html(handler, html)
        else:
            # Normal login flow
            result, html = login.handle_post(form_data)
            if isinstance(result, str) and result.startswith("2FA_REQUIRED:"):
                parts = result.split(":")
                temp_token, user_id = parts[1], parts[2]
                return send_html(handler, html, cookie=f"temp_2fa={temp_token}; path=/; HttpOnly")
            elif result:
                return redirect(handler, "/", cookie=f"atlas_token={result}; path=/; HttpOnly")
            else:
                return send_html(handler, html)"""
        
        # Replace the simple login handler
        old_handler = """if path == "/login.py" and method == "POST":
        form_data = parse_form(handler)
        result, html = login.handle_post(form_data)
        if result:
            return redirect(handler, "/", cookie=f"atlas_token={result}; path=/; HttpOnly")
        else:
            return send_html(handler, html)"""
        
        if old_handler in content:
            content = content.replace(old_handler, two_fa_handler)
    
    # Write updated content
    with open('main.py', 'w') as f:
        f.write(content)
    
    print("Updated login handler for 2FA support")

def add_flight_booking_routes():
    """Add flight booking route handlers"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Add flight booking handler
    booking_handler = """
    # Flight booking routes
    if path.startswith("/booking-confirmation/") and method == "GET":
        booking_id = path.split("/")[-1]
        user = get_user_from_token(handler)
        html = flight_booking.render_booking_confirmation(booking_id, user)
        return send_html(handler, html)
    
    if path == "/book-flight" and method == "POST":
        form_data = parse_form(handler)
        user = get_user_from_token(handler)
        result, html = flight_booking.handle_flight_booking(form_data, user)
        if result and isinstance(result, str) and result.startswith("/"):
            return redirect(handler, result)
        else:
            return send_html(handler, html if html else flight_booking.render_flight_booking_form({}, user))"""
    
    # Find a good place to insert the handler (after existing handlers)
    if 'if path == "/login.py" and method == "POST":' in content:
        insertion_point = content.find('if path == "/login.py" and method == "POST":')
        content = content[:insertion_point] + booking_handler + "\n    " + content[insertion_point:]
    
    # Write updated content
    with open('main.py', 'w') as f:
        f.write(content)
    
    print("Added flight booking routes")

if __name__ == "__main__":
    print("Updating main.py with new features...")
    update_main_routes()
    update_login_handler()
    add_flight_booking_routes()
    print("Main.py updated successfully!")
