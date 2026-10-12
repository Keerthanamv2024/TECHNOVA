"""
TechNova – IT Company Profile Website
Backend Application (Flask + SQLite)
Author: TechNova Team / College Web Programming Project
"""

import os
import re
import sqlite3
from datetime import datetime
from functools import wraps
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
    abort
)

app = Flask(__name__)

# Security & Application Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'technova-secure-college-session-key-2026')
DATABASE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'technova.db')

# Admin Authentication Credentials (configured via environment variables or safe defaults)
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')


def get_db_connection():
    """
    Establish a connection to the SQLite database.
    row_factory enables dict-like attribute access on records.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Automatically creates the 'enquiries' table if it does not already exist.
    """
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS enquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


# Initialize database upon module import so tables exist immediately
init_db()


def login_required(f):
    """
    Decorator to protect admin routes against unauthorized access.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Access restricted. Please log in with admin credentials.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


def validate_contact_data(name, email, subject, message):
    """
    Server-side validation for enquiry submissions.
    Returns (is_valid: bool, error_message: str).
    """
    if not name or len(name.strip()) < 2:
        return False, "Please enter your full name (minimum 2 characters)."

    # Standard RFC-compliant simplified email pattern
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not email or not re.match(email_regex, email.strip()):
        return False, "Please enter a valid email address (e.g., student@example.com)."

    if not subject or len(subject.strip()) < 3:
        return False, "Please enter a message subject (minimum 3 characters)."

    if not message or len(message.strip()) < 10:
        return False, "Please enter a message body (minimum 10 characters)."

    return True, ""


# -------------------------------------------------------------
# Public Routes
# -------------------------------------------------------------

@app.route('/')
def index():
    """
    Serve the single-page TechNova IT company profile.
    """
    return render_template('index.html')


@app.route('/contact', methods=['POST'])
def contact():
    """
    Handle contact form submissions.
    Supports both traditional POST form submissions and asynchronous AJAX requests.
    Validates data, stores in SQLite using parameterized queries, and returns feedback.
    """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json

    if request.is_json:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
    else:
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

    is_valid, error_msg = validate_contact_data(name, email, subject, message)

    if not is_valid:
        if is_ajax:
            return jsonify({'success': False, 'message': error_msg}), 400
        flash(error_msg, 'danger')
        return redirect(url_for('index') + '#contact')

    try:
        with get_db_connection() as conn:
            # Parameterized query protects against SQL injection
            conn.execute(
                '''
                INSERT INTO enquiries (name, email, subject, message)
                VALUES (?, ?, ?, ?)
                ''',
                (name, email, subject, message)
            )
            conn.commit()

        success_msg = f"Thank you, {name}! Your message has been received. Our IT consulting team will get back to you shortly."

        if is_ajax:
            return jsonify({'success': True, 'message': success_msg}), 200

        flash(success_msg, 'success')
        return redirect(url_for('index') + '#contact')

    except Exception as e:
        server_error = "An error occurred while saving your message. Please try again later."
        if is_ajax:
            return jsonify({'success': False, 'message': server_error}), 500
        flash(server_error, 'danger')
        return redirect(url_for('index') + '#contact')


# -------------------------------------------------------------
# Admin Authentication & Dashboard Routes
# -------------------------------------------------------------

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """
    Handle admin authentication.
    GET: display login form.
    POST: verify credentials and initialize session.
    """
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['admin_user'] = username
            flash(f"Welcome back, {username}! You are now logged in.", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid administrator credentials. Please check and try again.", "danger")

    return render_template('admin_login.html')


@app.route('/admin')
@login_required
def admin_dashboard():
    """
    Protected dashboard displaying all enquiries stored in SQLite.
    Jinja2 automatically escapes variables to prevent Cross-Site Scripting (XSS).
    """
    with get_db_connection() as conn:
        enquiries = conn.execute(
            'SELECT * FROM enquiries ORDER BY created_at DESC'
        ).fetchall()

    return render_template('admin.html', enquiries=enquiries, admin_user=session.get('admin_user'))


@app.route('/admin/delete/<int:enquiry_id>', methods=['POST'])
@login_required
def delete_enquiry(enquiry_id):
    """
    Delete an enquiry record by ID.
    Protected by login_required.
    """
    with get_db_connection() as conn:
        conn.execute('DELETE FROM enquiries WHERE id = ?', (enquiry_id,))
        conn.commit()

    flash(f"Enquiry #{enquiry_id} has been deleted successfully.", "info")
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/logout')
def admin_logout():
    """
    Log out the administrator and clear the session.
    """
    session.clear()
    flash("You have been safely logged out.", "info")
    return redirect(url_for('admin_login'))


# -------------------------------------------------------------
# Custom Error Handlers
# -------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404


if __name__ == '__main__':
    # Local development server
    port = int(os.getenv('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
