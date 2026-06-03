from flask import Blueprint, render_template, session, redirect, url_for, flash
from functools import wraps

reflections_bp = Blueprint('reflections', __name__)

# Each member fills in their own reflection here
MEMBERS = [
    {
        'name': 'Flores, Aivan',
        'role': 'App Setup + Dashboard Route + Flask login protection',
        'learned': [
            'Effective time management in coding is a skill in itself. Something as simple as writing reusable code instead of repeating the same lines over and over can save you a significant amount of time, and that lesson extends far beyond just programming.',
            'Do not be afraid to try your own approach when solving a problem. Even if it takes longer, the process of figuring things out on your own builds a deeper understanding that no shortcut can give you.',
            'Honesty will always be the better choice in an academic setting. Regardless of the score, knowing that you gave your honest best effort is something no grade can take away from you.',
        ],
        'realization': (
            'We are all human, we make mistakes, and we are each gifted in different ways. '
            'Some people are naturally strong at coding, while others shine in design, communication, or other areas. '
            'If you ever find yourself in a room where you feel out of place or not at your best, '
            'perhaps it is not a reflection of your worth, it simply means you have not yet found '
            'the right space where your true strengths can be seen. '
            'Everyone has something remarkable to offer; it is just a matter of finding where that something belongs.'
        ),
    },
    {
        'name': 'David, Lealyn Rubias',
        'role': 'Login Page',
        'learned': [
            'I learned how Flask sessions work to keep a user logged in across different pages.',
            'I learned how to handle HTML form submissions using request.form in Flask.',
            'I learned how to display flash messages to give feedback to the user.',
        ],
        'realization': (
            'I realized that even a simple login page involves a lot of small details — '
            'checking for empty fields, showing the right error message, and redirecting '
            'the user properly. Good user experience starts at the login screen.'
        ),
    },
    {
        'name': 'Bilog, Kathleen Shane Caburobias',
        'role': 'Base Analyzer Class (OOP)',
        'learned': [
            'I learned how to write a parent class in Python using OOP principles.',
            'I learned what inheritance means — child classes can reuse methods from the parent.',
            'I learned how method overriding works when a child class replaces a parent method.',
        ],
        'realization': (
            'I realized that OOP makes code much easier to manage when a project grows bigger. '
            'Instead of copying and pasting the same cleaning code everywhere, we write it once '
            'in BaseAnalyzer and every other class just inherits it automatically.'
        ),
    },
    {
        'name': 'Petrola, Jefferson',
        'role': 'HTML Templates and Navigation',
        'learned': [
            'I learned how Jinja2 templating works — passing data from Python to HTML.',
            'I learned how to use template inheritance in Flask with base.html.',
            'I learned how to loop through data and display it in HTML using Jinja2 for loops.',
        ],
        'realization': (
            'I realized that the frontend and backend are closely connected in Flask. '
            'When the Python route sends data to the template, the HTML just displays it — '
            'which means clean Python code leads to a cleaner and easier-to-manage webpage.'
        ),
    },
    {
        'name': 'Revilla, Ladesma Archilyn Bangcaya',
        'role': 'Account Management Page',
        'learned': [
            'I learned how to handle two different form actions on a single Flask route.',
            'I learned how to validate user input like password length and matching passwords.',
            'I learned how to use a global dictionary to store and update account information.',
        ],
        'realization': (
            'I realized that account management, even without a real database, requires '
            'careful input validation. Every field needs to be checked before saving anything — '
            'otherwise users can accidentally break their own account settings.'
        ),
    },
]


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper


@reflections_bp.route('/reflections')
@login_required
def reflections():
    return render_template('reflections.html', members=MEMBERS)