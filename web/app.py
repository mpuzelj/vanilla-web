from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import psycopg2
import uuid
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, email, is_admin):
        self.id = id
        self.email = email
        self.is_admin = is_admin

    def get_id(self):
        return str(self.id)

def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, is_admin FROM users WHERE id = %s", (user_id,))
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

app.config['MAIL_SERVER'] = 'mailhog'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        verification_token = str(uuid.uuid4())
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (email, password, is_admin, is_active, verification_token) VALUES (%s, %s, %s, %s, %s)",
                (email, hashed_pw, False, False, verification_token)
            )
            conn.commit()
            # Send verification email
            verify_url = url_for('verify', token=verification_token, _external=True)
            msg = Message(
                "Verify your email",
                sender="noreply@vanilla-web.local",
                recipients=[email]
            )
            msg.body = f"Welcome! Please verify your email by clicking this link: {verify_url}"
            mail.send(msg)
            flash('Registration successful! Please check your email to verify your account.')
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            if 'duplicate key value violates unique constraint' in str(e):
                flash('Registration failed: Email address already registered.')
            else:
                flash('Registration failed: ' + str(e))
        finally:
            cur.close()
            conn.close()
    return render_template('register.html')

@app.route('/verify/<token>')
def verify(token):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_active = TRUE WHERE verification_token = %s", (token,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Email verified! You can now log in.')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, email, password, is_admin, login_count, is_active FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        if user and bcrypt.check_password_hash(user[2], password):
            if not user[5]:  # is_active
                flash('Please verify your email before logging in.')
            else:
                cur.execute("UPDATE users SET login_count = COALESCE(login_count, 0) + 1 WHERE id = %s", (user[0],))
                conn.commit()
                user_obj = User(user[0], user[1], user[3])
                login_user(user_obj)
                cur.close()
                conn.close()
                return redirect(url_for('admin' if user[3] else 'index'))
        else:
            flash('Invalid credentials')
        cur.close()
        conn.close()
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
    cur.execute("SELECT login_count FROM users WHERE email = %s", ('admin@admin.com',))
    result = cur.fetchone()
    login_count = result[0] if result else 0
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