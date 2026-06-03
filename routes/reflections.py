from flask import Blueprint, render_template, session, redirect, url_for, flash
from functools import wraps

reflections_bp = Blueprint('reflections', __name__)

# Each member fills in their own reflection here
MEMBERS = [
    {
        'name': 'Flores, Aivan',
        'role': 'App Setup + Dashboard Route + Flask login protection',
        'learned': [
            'Effective time management in coding is a skill in itself.',
            'Do not be afraid to try your own approach when solving a problem.',
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
            'I learned how to use Python for data analytics by applying data cleaning, filtering, and transformation techniques.',
            'I discovered how to use libraries such as Pandas and NumPy for data manipulation and analysis.',
            'I gained experience working with control structures and functions to process and manage data efficiently.',
            'I learned how to handle datasets, including identifying and managing missing values to improve data quality.',
            'I developed skills in creating charts and graphs using Matplotlib to visualize and present data effectively.',
            'I became familiar with the basics of Object-Oriented Programming and how it helps organize programs into reusable components.',
        ],
        'realization': (
            'I realized that data analytics is not just about making charts and dashboards. '
            'It is also about preparing and processing data. During the course some topics were tough for me, '
            'like Object-Oriented Programming. And there were times when I needed extra practice to understand it. '
            'Despite this, I learned that programming is a skill that improves through patience, trial and error, '
            'and continuous learning. This subject helped me appreciate how data can be transformed into meaningful '
            'information and how technology can be used to support better decision-making.'
        ),
    },
    {
        'name': 'Bilog, Kathleen Shane Caburobias',
        'role': 'Base Analyzer Class (OOP)',
        'learned': [
            'I learned how to use Pandas to clean and organize data, including handling missing values before analysis.',
            'I learned how OOP helps make programs more organized, reusable, and easier to maintain.',
            'I learned how to create charts and visualizations using Matplotlib to make data easier to understand and interpret.',
        ],
        'realization': (
            'I realized that data analysis is not just about writing code. '
            'It also involves preparing data properly and presenting it clearly '
            'to generate meaningful insights.'
        ),
    },
    {
        'name': 'Petrola, Jefferson',
        'role': 'HTML Templates and Navigation',
        'learned': [
            '',
            '',
            '',
        ],
        'realization': (
            ''
            ''
            ''
        ),
    },
    {
        'name': 'Revilla, Ladesma Archilyn Bangcaya',
        'role': 'Account Management Page',
        'learned': [
            '',
            '',
            '',
        ],
        'realization': (
            ''
            ''
            ''
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