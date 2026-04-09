#!/usr/bin/env python3
"""
Fix all remaining MySQL imports to use SQLite
"""

import os
import re

def fix_file_imports(filepath, old_import, new_import):
    """Fix imports in a file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Replace the import
        content = content.replace(old_import, new_import)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"Fixed {filepath}")
        return True
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    """Fix all import issues"""
    
    # Files to fix
    fixes = [
        ('admin_panel.py', 'import admin_db, guide_db', 'import admin_db_sqlite as admin_db, guide_db_sqlite as guide_db'),
        ('guide_portal.py', 'import guide_db', 'import guide_db_sqlite as guide_db'),
        ('guide_verification.py', 'import guide_db', 'import guide_db_sqlite as guide_db'),
        ('guides.py', 'import guide_db', 'import guide_db_sqlite as guide_db'),
        ('profile.py', 'import guide_db', 'import guide_db_sqlite as guide_db'),
        ('login.py', 'import db', 'import db_sqlite as db'),
        ('register.py', 'import db', 'import db_sqlite as db'),
        ('setup_2fa.py', 'import db', 'import db_sqlite as db'),
        ('authenticator.py', 'import db', 'import db_sqlite as db'),
        ('admin_login.py', 'import admin_db', 'import admin_db_sqlite as admin_db'),
    ]
    
    for filename, old_import, new_import in fixes:
        fix_file_imports(filename, old_import, new_import)
    
    print("All imports fixed!")

if __name__ == "__main__":
    main()
