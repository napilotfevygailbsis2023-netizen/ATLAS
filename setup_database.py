#!/usr/bin/env python3
"""
Database setup script for ATLAS new features
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_all_features():
    """Setup database tables for all new features"""
    
    print("Setting up database for new features...")
    
    # Setup 2FA tables
    try:
        import authenticator
        if authenticator.setup_2fa_database():
            print("  - 2FA database setup complete")
        else:
            print("  - 2FA database setup failed")
    except Exception as e:
        print(f"  - 2FA setup error: {e}")
    
    # Setup flight booking tables
    try:
        import flight_booking
        if flight_booking.init_flight_booking_tables():
            print("  - Flight booking database setup complete")
        else:
            print("  - Flight booking database setup failed")
    except Exception as e:
        print(f"  - Flight booking setup error: {e}")
    
    # Setup guide verification tables
    try:
        import guide_db
        guide_db.init_guide_tables()
        print("  - Guide verification database setup complete")
    except Exception as e:
        print(f"  - Guide verification setup error: {e}")
    
    # Setup system messaging tables
    try:
        import system_messaging
        if system_messaging.init_messaging_tables():
            print("  - System messaging database setup complete")
        else:
            print("  - System messaging database setup failed")
    except Exception as e:
        print(f"  - System messaging setup error: {e}")
    
    print("Database setup completed!")

if __name__ == "__main__":
    setup_all_features()
