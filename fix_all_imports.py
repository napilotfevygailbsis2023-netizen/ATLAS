#!/usr/bin/env python3
"""
Fix all double import errors
"""

import os
import re

def fix_double_imports():
    """Fix all double import statements"""
    
    files_to_fix = {
        'register.py': 'import db_sqlite as db_sqlite as db',
        'setup_2fa.py': 'import db_sqlite as db_sqlite as db', 
        'authenticator.py': 'import db_sqlite as db_sqlite as db',
        'admin_login.py': 'import admin_db_sqlite as admin_db_sqlite as admin_db',
        'profile.py': 'import guide_db_sqlite as guide_db_sqlite as guide_db',
        'admin_panel.py': 'import admin_db_sqlite as admin_db_sqlite as admin_db, guide_db_sqlite as guide_db_sqlite as guide_db',
        'guide_portal.py': 'import guide_db_sqlite as guide_db_sqlite as guide_db'
    }
    
    for filename, bad_import in files_to_fix.items():
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            # Fix double imports
            content = content.replace('import db_sqlite as db_sqlite as db', 'import db_sqlite as db')
            content = content.replace('import admin_db_sqlite as admin_db_sqlite as admin_db', 'import admin_db_sqlite as admin_db')
            content = content.replace('import guide_db_sqlite as guide_db_sqlite as guide_db', 'import guide_db_sqlite as guide_db')
            
            # Fix complex double imports
            content = content.replace('import admin_db_sqlite as admin_db_sqlite as admin_db, guide_db_sqlite as guide_db_sqlite as guide_db', 
                                     'import admin_db_sqlite as admin_db, guide_db_sqlite as guide_db')
            
            with open(filename, 'w') as f:
                f.write(content)
            
            print(f"Fixed {filename}")
            
        except Exception as e:
            print(f"Error fixing {filename}: {e}")

if __name__ == "__main__":
    fix_double_imports()
    print("All double imports fixed!")
