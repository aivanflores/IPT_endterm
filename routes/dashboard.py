from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.ai_impact_analyzer import AIImpactAnalyzer
from functools import wraps

dashboard_bp = Blueprint('dashboard', __name__)


def login_required(func):
    """Decorator: redirects to login if user is not logged in."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper


@dashboard_bp.route('/dashboard')
@login_required
def index():
    """
    Main dashboard page.
    Loads the AI Student Impact dataset, cleans it,
    gets the summary stats, and generates all charts.
    Assigned to: Flores, Aivan
    """
    analyzer = AIImpactAnalyzer()
    summary = {}
    charts = []
    extra_stats = {}
    error = None

    if analyzer.load_data():
        analyzer.clean_data()
        summary = analyzer.get_summary()
        charts = analyzer.generate_charts()

        # Extra stats to show on dashboard cards
        df = analyzer.df
        extra_stats = {
            'avg_genai_hours': round(df['Weekly_GenAI_Hours'].mean(), 2),
            'avg_post_gpa': round(df['Post_Semester_GPA'].mean(), 2),
            'avg_skill_retention': round(df['Skill_Retention_Score'].mean(), 2),
            'high_burnout_pct': round(
                (df['Burnout_Risk_Level'] == 'High').sum() / len(df) * 100, 1
            ),
        }
    else:
        error = "ai_student_impact_dataset-1.csv not found. Place it in the /data folder."

    return render_template('dashboard.html',
                           summary=summary,
                           charts=charts,
                           extra_stats=extra_stats,
                           error=error)
