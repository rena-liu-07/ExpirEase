import sqlite3

conn = sqlite3.connect('foodapp.db')
cursor = conn.cursor()

# Check for test foods
cursor.execute('SELECT name, category, date_added, expire_days FROM food WHERE name LIKE "%Test%" ORDER BY date_added DESC LIMIT 5')
rows = cursor.fetchall()

print('Recent test foods:')
for row in rows:
    print(f'  {row[0]} ({row[1]}) - added {row[2]}, expires in {row[3]} days')

# Check total count
cursor.execute('SELECT COUNT(*) FROM food')
total = cursor.fetchone()[0]
print(f'\nTotal foods in database: {total}')

conn.close()
