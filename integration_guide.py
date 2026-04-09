#!/usr/bin/env python3
"""
Integration guide for ATLAS new features
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def integrate_weather_with_flights():
    """Integrate weather system with flight booking"""
    
    # Update flights.py to include weather alerts
    with open('flights.py', 'r') as f:
        content = f.read()
    
    # Add weather import
    if 'import weather_flight_integration' not in content:
        content = content.replace(
            'from data import FLIGHTS as FALLBACK',
            'from data import FLIGHTS as FALLBACK\nimport weather_flight_integration'
        )
    
    # Add weather check to flight cards
    weather_check = """
    # Check weather impact for this route
    origin_city = f["from"].split("(")[0].strip()
    dest_city = f["to"].split("(")[0].strip()
    weather_data = weather_flight_integration.check_flight_route_weather(origin_city, dest_city)
    weather_alert = weather_flight_integration.render_weather_flight_alert(weather_data.get('origin', {}).get('weather', {}))
    """
    
    # Add weather alert to card template
    if 'return f"""' in content and 'weather_alert' not in content:
        # Find the card function and add weather integration
        card_start = content.find('def _card(f):')
        if card_start != -1:
            # Add weather check at the beginning of _card function
            insertion_point = content.find('col = AIRLINE_COLORS.get', card_start)
            if insertion_point != -1:
                content = content[:insertion_point] + weather_check + '\n    ' + content[insertion_point:]
    
    # Add weather alert to card HTML
    if '<div class="grid-card">' in content and 'weather_alert' not in content:
        content = content.replace(
            '<div class="grid-card">',
            f'<div class="grid-card">\n        {{weather_alert}}'
        )
    
    with open('flights.py', 'w') as f:
        f.write(content)
    
    print("Weather integration added to flights.py")

def integrate_verification_with_guides():
    """Integrate verification system with guide display"""
    
    with open('guides.py', 'r') as f:
        content = f.read()
    
    # Add verification import
    if 'import guide_verification' not in content:
        content = content.replace(
            'import guide_db',
            'import guide_db\nimport guide_verification'
        )
    
    # Add verification badge to guide cards
    verification_check = """
    # Check guide verification status
    is_verified = False
    verification_badge = ""
    try:
        is_legitimate, verification_msg = guide_verification.check_guide_legitimacy(g.get("guide_id", ""))
        if is_legitimate:
            verification_badge = '<div style="background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:700;margin-bottom:6px">&#10003; Verified Guide</div>'
    except:
        pass
    """
    
    # Add verification check to _card function
    if 'def _card(g, i):' in content and 'is_verified' not in content:
        insertion_point = content.find('col   = COLORS[i % len(COLORS)]')
        if insertion_point != -1:
            content = content[:insertion_point] + verification_check + '\n    ' + content[insertion_point:]
    
    # Add verification badge to card HTML
    if 'grid-card-top' in content and 'verification_badge' not in content:
        content = content.replace(
            'f\'<div class="grid-card-top" style="background:linear-gradient(135deg,{col},{col}bb);position:relative">\'',
            f'f\'<div class="grid-card-top" style="background:linear-gradient(135deg,{col},{col}bb);position:relative">\'\n        + verification_badge'
        )
    
    with open('guides.py', 'w') as f:
        f.write(content)
    
    print("Verification integration added to guides.py")

def integrate_messaging_with_profile():
    """Integrate messaging system with user profile"""
    
    with open('profile.py', 'r') as f:
        content = f.read()
    
    # Add messaging import
    if 'import system_messaging' not in content:
        content = content.replace(
            'from template import build_shell',
            'from template import build_shell\nimport system_messaging'
        )
    
    # Add system status section to profile
    status_section = """
    # System Status Updates
    system_status = system_messaging.render_system_status()
    """
    
    # Add status section before booking cards
    if 'current_bookings = []' in content and 'system_status' not in content:
        insertion_point = content.find('current_bookings = []')
        if insertion_point != -1:
            content = content[:insertion_point] + status_section + '\n    ' + content[insertion_point:]
    
    # Add status display to profile HTML
    if 'page-wrap' in content and 'system_status' not in content:
        content = content.replace(
            '<div class="page-wrap">',
            f'<div class="page-wrap">\n      {system_status}'
        )
    
    with open('profile.py', 'w') as f:
        f.write(content)
    
    print("Messaging integration added to profile.py")

def integrate_2fa_with_register():
    """Integrate 2FA setup with registration"""
    
    with open('register.py', 'r') as f:
        content = f.read()
    
    # Add 2FA setup option to registration success
    if 'import authenticator' not in content:
        content = content.replace(
            'import db',
            'import db\nimport authenticator'
        )
    
    # Add 2FA setup prompt after successful registration
    setup_prompt = """
    # Initialize 2FA database for new user
    authenticator.setup_2fa_database()
    """
    
    if 'return token, None' in content and 'setup_2fa_database' not in content:
        insertion_point = content.find('return token, None')
        if insertion_point != -1:
            content = content[:insertion_point] + '\n    ' + setup_prompt + '\n    ' + content[insertion_point:]
    
    with open('register.py', 'w') as f:
        f.write(content)
    
    print("2FA integration added to register.py")

def add_navigation_links():
    """Add navigation links for new features"""
    
    with open('template.py', 'r') as f:
        content = f.read()
    
    # Add new navigation items
    new_nav_items = """
    <a href="/setup-2fa" class="nav-link" style="color:#0038A8;text-decoration:none;padding:8px 16px;border-radius:6px;font-weight:600">2FA Setup</a>
    <a href="/system-messages" class="nav-link" style="color:#0038A8;text-decoration:none;padding:8px 16px;border-radius:6px;font-weight:600">Messages</a>"""
    
    # Find navigation section and add new items
    if 'class="nav"' in content and '2FA Setup' not in content:
        # Look for existing navigation links
        nav_start = content.find('<div class="nav">')
        if nav_start != -1:
            nav_end = content.find('</div>', nav_start)
            if nav_end != -1:
                nav_content = content[nav_start:nav_end]
                # Add new links before closing div
                updated_nav = nav_content.replace('</div>', new_nav_items + '</div>')
                content = content.replace(nav_content, updated_nav)
    
    with open('template.py', 'w') as f:
        f.write(content)
    
    print("Navigation links added to template.py")

if __name__ == "__main__":
    print("Integrating new features with existing system...")
    
    try:
        integrate_weather_with_flights()
        integrate_verification_with_guides()
        integrate_messaging_with_profile()
        integrate_2fa_with_register()
        add_navigation_links()
        
        print("\nIntegration completed successfully!")
        print("\nNext steps:")
        print("1. Start the MySQL server")
        print("2. Run: python setup_database.py")
        print("3. Run: python main.py")
        print("4. Test the new features")
        
    except Exception as e:
        print(f"Integration error: {e}")
        print("Please check the error and try again.")
