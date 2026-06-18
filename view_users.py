import sqlite3

conn = sqlite3.connect(
    'database.db',
    timeout=10
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM users")

users = cursor.fetchall()

for user in users:
    print(user)

conn.close()