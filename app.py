from flask import Flask, redirect, url_for
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Create needed folders on startup
    Config.init_app(app)

    # Register blueprints (routes)
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.account import account_bp
    from routes.reflections import reflections_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(reflections_bp)

    # Root URL goes to login
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
