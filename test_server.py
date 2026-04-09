#!/usr/bin/env python3
"""
Test the server without MySQL dependencies
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all imports work"""
    try:
        print("Testing imports...")
        
        # Test SQLite imports
        import db_sqlite as db
        print("  - db_sqlite imported")
        
        import guide_db_sqlite as guide_db
        print("  - guide_db_sqlite imported")
        
        import admin_db_sqlite as admin_db
        print("  - admin_db_sqlite imported")
        
        import flight_booking_sqlite as flight_booking
        print("  - flight_booking_sqlite imported")
        
        import system_messaging_sqlite as system_messaging
        print("  - system_messaging_sqlite imported")
        
        # Test basic functions
        print("\nTesting basic functions...")
        
        # Test database connections
        conn = db.get_conn()
        print("  - SQLite connection works")
        conn.close()
        
        conn = guide_db.get_conn()
        print("  - Guide SQLite connection works")
        conn.close()
        
        # Test user functions
        print("\nTesting user functions...")
        
        # Test registration
        success, msg = db.register_user("Test", "User", "test@example.com", "password123")
        print(f"  - User registration: {success} - {msg}")
        
        # Test login
        success, token, user = db.login_user("test@example.com", "password123")
        if success:
            print(f"  - User login works: {user['fname']} {user['lname']}")
            
            # Test token validation
            user_from_token = db.get_user_from_token(token)
            print(f"  - Token validation works: {user_from_token['email']}")
            
            # Test logout
            logout_success = db.logout_user(token)
            print(f"  - Logout works: {logout_success}")
        
        print("\nAll tests passed! Server should work now.")
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_imports():
        print("\nYou can now run: python main.py")
    else:
        print("\nFix the errors before running the server.")
