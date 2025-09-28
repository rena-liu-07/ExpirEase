import sqlite3
import os

# Check if database exists
db_path = "foodapp.db"
if os.path.exists(db_path):
    print(f"Database file exists: {db_path}")
    
    # Connect and check tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables in database: {tables}")
    
    # Check if food table has data
    try:
        cursor.execute("SELECT COUNT(*) FROM food")
        count = cursor.fetchone()[0]
        print(f"Number of items in food table: {count}")
        
        if count > 0:
            cursor.execute("SELECT name, category, expire_days FROM food LIMIT 5")
            samples = cursor.fetchall()
            print(f"Sample data: {samples}")
    except Exception as e:
        print(f"Error checking food table: {e}")
    
    conn.close()
else:
    print(f"Database file does not exist: {db_path}")