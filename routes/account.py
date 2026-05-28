from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps

account_bp = Blueprint('account', __name__)

# Admin info stored in a dictionary (simple, no database needed)
admin_info = {
    'username': 'admin',
    'password': 'admin123',
    'full_name': 'Administrator',
    'email': 'admin@group9.com'
}


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
    Assigned to: Revilla, Ladesma Archilyn Bangcaya
    """
    global admin_info

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
                flash('Profile updated!', 'success')

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
                flash('Password changed successfully!', 'success')

    return render_template('account.html', admin=admin_info)
