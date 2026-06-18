import sqlite3

def create_database():

    conn = sqlite3.connect(
    'database.db',
    timeout=10
)

    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

create_database()

print("Database Created Successfully")

conn = sqlite3.connect(
    'database.db',
    timeout=10
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS quizzes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS questions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER,
    question TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    correct_answer TEXT
)
""")

conn.commit()
conn.close()