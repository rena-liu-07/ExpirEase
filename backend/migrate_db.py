import sqlite3
import os

# Connect to database
db_path = os.path.join(os.path.dirname(__file__), "foodapp.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check current schema
cursor.execute("PRAGMA table_info(food)")
current_schema = cursor.fetchall()
print("Current food table schema:")
for row in current_schema:
    print(f"  {row}")

# Check if category column exists
has_category = any(row[1] == 'category' for row in current_schema)

if not has_category:
    print("\nAdding category column...")
    try:
        cursor.execute('ALTER TABLE food ADD COLUMN category TEXT DEFAULT "Unknown"')
        conn.commit()
        print("✅ Successfully added category column")
    except sqlite3.OperationalError as e:
        print(f"❌ Error adding column: {e}")
else:
    print("\n✅ Category column already exists")

# Show updated schema
cursor.execute("PRAGMA table_info(food)")
updated_schema = cursor.fetchall()
print("\nUpdated food table schema:")
for row in updated_schema:
    print(f"  {row}")

conn.close()
print("\n🎉 Database migration complete!")