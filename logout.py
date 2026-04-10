import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db

def render(token=""):
    if token:
        db.logout(token)
    return "logged_out"
