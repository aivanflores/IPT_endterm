import os

class Config:
    SECRET_KEY = 'group9-secret-key-2026'

    # Path to the data folder (where your CSV lives)
    DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data')

    # Path where generated chart images are saved
    CHART_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'charts')

    @staticmethod
    def init_app(app):
        # Create folders if they don't exist yet
        os.makedirs(Config.CHART_FOLDER, exist_ok=True)
        os.makedirs(Config.DATA_FOLDER, exist_ok=True)
