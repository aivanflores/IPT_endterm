import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__)

# Path to the JSON file where admin credentials are stored
ADMIN_FILE = os.path.join(os.path.dirname(__file__), '..', 'admin.json')


def load_admin():
    """
    Reads admin credentials from admin.json.
    This way, if the password was changed in Account Management,
    login will always use the updated password.
    """
    try:
        with open(ADMIN_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default fallback if file doesn't exist
        return {'username': 'admin', 'password': 'admin123'}
    except Exception as e:
        print(f"[ERROR] Could not read admin.json: {e}")
        return {'username': 'admin', 'password': 'admin123'}


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Already logged in? Go to dashboard
    if 'user' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Please fill in both fields.', 'error')
        else:
            # Load credentials fresh from file every login attempt
            admin = load_admin()

            if username == admin['username'] and password == admin['password']:
                session['user'] = username
                flash('Welcome back!', 'success')
                return redirect(url_for('dashboard.index'))
            else:
                flash('Wrong username or password.', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))