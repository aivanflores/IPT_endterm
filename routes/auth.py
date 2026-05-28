from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__)

# Simple admin credentials — no database needed
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'


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
        elif username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
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
