from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
import psycopg2
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, is_admin):
        self.id = id
        self.username = username
        self.is_admin = is_admin

    def get_id(self):
        return str(self.id)

def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, is_admin FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return User(user[0], user[1], user[2])
    return None

@app.route('/')
def index():
    return render_template('index.html')

bcrypt = Bcrypt(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)", (username, hashed_pw, False))
            conn.commit()
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            flash('Registration failed: ' + str(e))
        finally:
            cur.close()
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, password, is_admin, login_count FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        if user and bcrypt.check_password_hash(user[2], password):
            # Increment login_count if admin
            cur.execute("UPDATE users SET login_count = COALESCE(login_count, 0) + 1 WHERE id = %s", (user[0],))
            conn.commit()
            user_obj = User(user[0], user[1], user[3])
            login_user(user_obj)
            cur.close()
            conn.close()
            return redirect(url_for('admin' if user[3] else 'index'))
        else:
            cur.close()
            conn.close()
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT login_count FROM users WHERE username = %s", ('admin',))
    login_count = cur.fetchone()[0]
    cur.close()
    conn.close()
    pgadmin_email = os.environ['PGADMIN_DEFAULT_EMAIL']
    pgadmin_password = os.environ['PGADMIN_DEFAULT_PASSWORD']
    return render_template(
        'admin.html',
        login_count=login_count,
        pgadmin_email=pgadmin_email,
        pgadmin_password=pgadmin_password
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)