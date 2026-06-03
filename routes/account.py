import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps

account_bp = Blueprint('account', __name__)

# Path to the JSON file that stores admin info
ADMIN_FILE = os.path.join(os.path.dirname(__file__), '..', 'admin.json')


def load_admin():
    try:
        with open(ADMIN_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # If file doesn't exist yet, return the default admin account
        return {
            'username': 'admin',
            'password': 'admin123',
            'full_name': 'Administrator',
            'email': 'admin@group9.com'
        }
    except Exception as e:
        print(f"[ERROR] Could not read admin.json: {e}")
        return {}


def save_admin(data):
    try:
        with open(ADMIN_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"[ERROR] Could not save admin.json: {e}")
        return False


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper


@account_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """
    Account management page.
    Admin can update their name, email, and password.
    Changes are saved to admin.json so they persist after restart.
    Assigned to: Revilla, Ladesma Archilyn Bangcaya
    """
    # Always load fresh from file
    admin_info = load_admin()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_profile':
            new_name  = request.form.get('full_name', '').strip()
            new_email = request.form.get('email', '').strip()

            if not new_name or not new_email:
                flash('Name and email cannot be empty.', 'error')
            else:
                admin_info['full_name'] = new_name
                admin_info['email']     = new_email

                if save_admin(admin_info):
                    flash('Profile updated!', 'success')
                else:
                    flash('Could not save changes. Try again.', 'error')

        elif action == 'change_password':
            current = request.form.get('current_password', '').strip()
            new_pw  = request.form.get('new_password', '').strip()
            confirm = request.form.get('confirm_password', '').strip()

            if current != admin_info['password']:
                flash('Current password is incorrect.', 'error')
            elif len(new_pw) < 6:
                flash('New password must be at least 6 characters.', 'error')
            elif new_pw != confirm:
                flash('New passwords do not match.', 'error')
            else:
                admin_info['password'] = new_pw

                if save_admin(admin_info):
                    flash('Password changed successfully!', 'success')
                else:
                    flash('Could not save new password. Try again.', 'error')

        # Reload from file after saving so display is always fresh
        admin_info = load_admin()

    return render_template('account.html', admin=admin_info)