from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)

app.secret_key = "lms_secret_key"

def init_db():

    conn = sqlite3.connect(
        'database.db',
        timeout=30
    )

    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Assignments Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS assignments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        due_date TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT DEFAULT 'Pending'
    )
    ''')

    # Quizzes Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quizzes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
    ''')

    # Questions Table
    cursor.execute('''
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
    ''')

    cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    quiz_id INTEGER,
    score INTEGER,
    total INTEGER
)
""")

    conn.commit()
    conn.close()
init_db()
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(
    'database.db',
    timeout=30
)
        cursor = conn.cursor()

        cursor.execute(
            '''
            SELECT * FROM users
            WHERE email=? AND password=?
            ''',
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session['user_id'] = user[0]
            session['fullname'] = user[1]

            return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db', timeout=30)
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO users(fullname,email,password)
            VALUES(?,?,?)
            ''',
            (fullname, email, password)
        )

        conn.commit()

        user_id = cursor.lastrowid

        conn.close()

        session['user_id'] = user_id
        session['fullname'] = fullname

        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/assignments', methods=['GET', 'POST'])
def assignments():

    conn = sqlite3.connect(
    'database.db',
    timeout=30
)
    cursor = conn.cursor()

    if request.method == 'POST':

        title = request.form['title']
        due_date = request.form['due_date']
        priority = request.form['priority']

        cursor.execute(
            '''
            INSERT INTO assignments(title,due_date,priority)
            VALUES(?,?,?)
            ''',
            (title, due_date, priority)
        )

        conn.commit()

    # Search functionality
    search = request.args.get('search')

    if search:

        cursor.execute(
            '''
            SELECT * FROM assignments
            WHERE title LIKE ?
            ''',
            ('%' + search + '%',)
        )

    else:

        cursor.execute("SELECT * FROM assignments")

    assignments = cursor.fetchall()

    conn.close()

    return render_template(
        'assignments.html',
        assignments=assignments
    )

@app.route('/delete_assignment/<int:id>')
def delete_assignment(id):

    conn = sqlite3.connect(
    'database.db',
    timeout=30
)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM assignments WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('assignments'))

@app.route('/complete_assignment/<int:id>')
def complete_assignment(id):

    conn = sqlite3.connect(
    'database.db',
    timeout=30
)
    cursor = conn.cursor()

    cursor.execute(
        '''
        UPDATE assignments
        SET status='Completed'
        WHERE id=?
        ''',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('assignments'))

@app.route('/quizzes', methods=['GET', 'POST'])
def quizzes():

    conn = sqlite3.connect(
    'database.db',
    timeout=10
)
    cursor = conn.cursor()

    if request.method == 'POST':

        title = request.form['title']

        cursor.execute(
            '''
            INSERT INTO quizzes(title)
            VALUES(?)
            ''',
            (title,)
        )

        conn.commit()

    cursor.execute("SELECT * FROM quizzes")
    quizzes = cursor.fetchall()

    conn.close()

    return render_template(
        'quizzes.html',
        quizzes=quizzes
    )

@app.route('/add_question/<int:quiz_id>', methods=['GET', 'POST'])
def add_question(quiz_id):

    conn = sqlite3.connect(
    'database.db',
    timeout=30
)
    cursor = conn.cursor()

    if request.method == 'POST':

        question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_answer = request.form['correct_answer']

        cursor.execute(
            '''
            INSERT INTO questions
            (
                quiz_id,
                question,
                option1,
                option2,
                option3,
                option4,
                correct_answer
            )
            VALUES(?,?,?,?,?,?,?)
            ''',
            (
                quiz_id,
                question,
                option1,
                option2,
                option3,
                option4,
                correct_answer
            )
        )

        conn.commit()

    cursor.execute(
        "SELECT * FROM questions WHERE quiz_id=?",
        (quiz_id,)
    )

    questions = cursor.fetchall()

    conn.close()

    return render_template(
        'add_question.html',
        quiz_id=quiz_id,
        questions=questions
    )

@app.route('/take_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):

    conn = sqlite3.connect('database.db', timeout=30)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM questions WHERE quiz_id=?",
        (quiz_id,)
    )

    questions = cursor.fetchall()

    if request.method == 'POST':

        score = 0

        for question in questions:

            selected = request.form.get(
                f"question_{question['id']}"
            )

            if selected == question['correct_answer']:
                score += 1

        total = len(questions)
        percentage = round((score / total) * 100, 2)

        # SAVE RESULT TO DATABASE
        cursor.execute(
            """
            INSERT INTO quiz_results
            (user_id, quiz_id, score, total)
            VALUES (?, ?, ?, ?)
            """,
            (
                session['user_id'],
                quiz_id,
                score,
                total
            )
        )

        conn.commit()
        conn.close()

        return render_template(
        'quiz_result.html',
        score=score,
        total=total,
        percentage=percentage
    )

    conn.close()

    return render_template(
        'take_quiz.html',
        questions=questions
    )

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(
        'database.db',
        timeout=30
    )

    cursor = conn.cursor()

    # Assignment Statistics

    cursor.execute(
        "SELECT COUNT(*) FROM assignments"
    )
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM assignments WHERE status='Pending'"
    )
    pending = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM assignments WHERE status='Completed'"
    )
    completed = cursor.fetchone()[0]

    # Quiz Statistics

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM quiz_results
        WHERE user_id=?
        """,
        (session['user_id'],)
    )

    quizzes_taken = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT AVG(
            (CAST(score AS FLOAT) / total) * 100
        )
        FROM quiz_results
        WHERE user_id=?
        """,
        (session['user_id'],)
    )

    avg_score = cursor.fetchone()[0]

    if avg_score is None:
        avg_score = 0

    avg_score = round(avg_score, 2)

    conn.close()

    return render_template(
        'dashboard.html',
        total=total,
        pending=pending,
        completed=completed,
        quizzes_taken=quizzes_taken,
        avg_score=avg_score
    )

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)