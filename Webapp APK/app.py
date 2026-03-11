
# app.py



# app.py
# technical: Flask app with safe DB migration to add username/category; session-based login.
# spoken: main backend file — starts server, ensures DB columns exist, and adds simple name-login.

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
# technical: secret key required for Flask sessions (store small per-user info)
# spoken: keeps track of who is logged in. Change this to something secret for real use.
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret-for-localhost')

DB_PATH = 'todo.db'  # spoken: same DB file you already have

# ----------------- Database utilities -----------------
def get_conn():
    # technical: open a DB connection, returns sqlite3.Connection
    # spoken: use this whenever we talk to the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_tables_and_columns():
    """
    technical: create tasks table if missing and add username/category columns if absent.
    spoken: safely update your DB so each task can be tied to a user and a category — won't delete your data.
    """
    conn = get_conn()
    c = conn.cursor()
    # create table if it doesn't exist (basic shape)
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            done INTEGER DEFAULT 0
        )
    ''')
    conn.commit()

    # check which columns exist (PRAGMA)
    c.execute("PRAGMA table_info(tasks)")
    cols = [row['name'] for row in c.fetchall()]

    # If table existed before without 'category' or 'name', PRAGMA ensures columns presence above,
    # but if older DB has different columns, we add missing ones with ALTER TABLE.
    # (SQLite ALTER TABLE ADD COLUMN is safe for existing tables.)
    if 'name' not in cols:
        c.execute("ALTER TABLE tasks ADD COLUMN name TEXT")
    if 'category' not in cols:
        c.execute("ALTER TABLE tasks ADD COLUMN category TEXT")
    if 'done' not in cols:
        c.execute("ALTER TABLE tasks ADD COLUMN done INTEGER DEFAULT 0")

    conn.commit()
    conn.close()

# initialize DB safely when app starts
ensure_tables_and_columns()

# ----------------- Authentication (simple name-based) -----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    # technical: handle GET (show form) and POST (process name)
    # spoken: user types their name — we store it in session and treat them as "logged in"
    if request.method == 'POST':
        name = request.form.get('username', '').strip()
        if not name:
            flash('Please enter a name.')
            return redirect(url_for('login'))
        session['username'] = name  # spoken: now backend knows who you are
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # technical: clear session for username
    # spoken: logs out the user (forget who they are)
    session.pop('username', None)
    return redirect(url_for('login'))

# ----------------- Main routes (user-scoped) -----------------
def require_login():
    # technical: helper returning username or None
    # spoken: quick check to see if someone is logged in
    return session.get('username')

@app.route('/')
def index():
    # technical: main page; load tasks only for current user
    # spoken: if you're not logged in, send you to /login; otherwise show your tasks
    username = require_login()
    if not username:
        return redirect(url_for('login'))

    conn = get_conn()
    c = conn.cursor()
    # fetch tasks only for this username
    c.execute('SELECT * FROM tasks WHERE category IS NOT NULL AND (username = ? OR username IS NULL OR username = "") ORDER BY id DESC', (username,))
    # Note: existing tasks without username (older entries) will be visible to everyone until assigned;
    # we'll assign username when creating new tasks.
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks, username=username)

@app.route('/add', methods=['POST'])
def add():
    # technical: add a task; uses 'category' from form or default; associates with session username
    # spoken: when user submits the add form, we save the task with their name so only they see it later
    username = require_login()
    if not username:
        return redirect(url_for('login'))

    task_name = request.form.get('task', '').strip()
    category = request.form.get('category', 'General').strip()
    if not task_name:
        flash('Task cannot be empty')
        return redirect(url_for('index'))

    conn = get_conn()
    c = conn.cursor()
    c.execute('INSERT INTO tasks (name, category, done, username) VALUES (?, ?, ?, ?)', (task_name, category, 0, username))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    # technical: flip done state — only if task belongs to current user (safety)
    # spoken: check/uncheck a task; we make sure you can only toggle your own tasks
    username = require_login()
    if not username:
        return redirect(url_for('login'))

    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT username, done FROM tasks WHERE id=?', (task_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        flash('Task not found')
        return redirect(url_for('index'))

    owner = row['username']
    if owner not in (None, '', username):
        # technical: prevent toggling others' tasks
        conn.close()
        flash('Not authorized')
        return redirect(url_for('index'))

    new_done = 0 if row['done'] else 1
    c.execute('UPDATE tasks SET done=? WHERE id=?', (new_done, task_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    # technical: delete row if belongs to user (safety)
    # spoken: user clicks delete — we remove task if it's theirs
    username = require_login()
    if not username:
        return redirect(url_for('login'))

    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT username FROM tasks WHERE id=?', (task_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        flash('Task not found')
        return redirect(url_for('index'))

    owner = row['username']
    if owner not in (None, '', username):
        conn.close()
        flash('Not authorized to delete')
        return redirect(url_for('index'))

    c.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# ----------------- Run -----------------
if __name__ == '__main__':
    # technical: start server; debug mode helps while developing
    # spoken: run python app.py and open http://127.0.0.1:5000
    app.run(debug=True)