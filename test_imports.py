import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Testing imports from backend/app.py...")

try:
    from flask import Flask, request, jsonify
    print("✓ Flask imports OK")
except Exception as e:
    print(f"✗ Flask import error: {e}")
    
try:
    from flask_cors import CORS
    print("✓ CORS import OK")
except Exception as e:
    print(f"✗ CORS import error: {e}")

try:
    import sqlite3
    print("✓ sqlite3 import OK")
except Exception as e:
    print(f"✗ sqlite3 import error: {e}")

try:
    from datetime import datetime, timedelta
    print("✓ datetime import OK")
except Exception as e:
    print(f"✗ datetime import error: {e}")

# Test if app.py can be imported
try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
    import app
    print("✓ backend/app.py imports OK")
    print(f"  Flask app object: {app.app}")
except Exception as e:
    print(f"✗ backend/app.py import error: {e}")
    import traceback
    traceback.print_exc()
