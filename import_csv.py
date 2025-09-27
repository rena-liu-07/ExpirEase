import sqlite3
import csv
import os

# ---------- 配置路径 ----------
BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "foodapp.db")
CSV_FILE = os.path.join(BASE_DIR, "food_data.csv")

# ---------- 连接数据库 ----------
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# ---------- 确保表存在 ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS food_catalog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    default_expire_days INTEGER
)
""")
conn.commit()

# ---------- 导入 CSV ----------
imported_count = 0
with open(CSV_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["name"].strip()
        days = int(row["default_expire_days"])
        try:
            cursor.execute(
                "INSERT INTO food_catalog (name, default_expire_days) VALUES (?, ?)",
                (name, days)
            )
            imported_count += 1
        except sqlite3.IntegrityError:
            # 已存在的食物就跳过
            pass

conn.commit()
conn.close()

print(f"✅ 导入完成，总共导入 {imported_count} 条食物到 food_catalog 表！")

