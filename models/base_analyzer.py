import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Needed for Flask — no display/GUI
import matplotlib.pyplot as plt
import os
from config import Config


class BaseAnalyzer:
    """
    Parent class for the AI Student Impact analyzer.
    OOP concept: other classes can inherit (extend) this class.
    Common methods like loading, cleaning, and saving charts are defined here
    so we don't have to repeat the same code.
    """

    def __init__(self, filename):
        self.filename = filename
        self.filepath = os.path.join(Config.DATA_FOLDER, filename)
        self.df = None  # Will store the loaded DataFrame

    def load_data(self):
        """Load the CSV file. Returns True if successful, False if not found."""
        try:
            self.df = pd.read_csv(self.filepath)
            return True
        except FileNotFoundError:
            print(f"[ERROR] File not found: {self.filepath}")
            return False
        except Exception as e:
            print(f"[ERROR] Could not load {self.filename}: {e}")
            return False

    def clean_data(self):
        """
        Basic data cleaning.
        - Removes completely empty rows
        - Fills missing numbers with column average
        - Fills missing text with 'Unknown'
        Child classes can override this method if they need custom cleaning.
        """
        if self.df is None:
            return

        before = self.df.isnull().sum().sum()

        # Remove rows where ALL values are empty
        self.df.dropna(how='all', inplace=True)

        # Fill missing numbers with the average
        for col in self.df.select_dtypes(include=[np.number]).columns:
            self.df[col] = self.df[col].fillna(self.df[col].mean())

        # Fill missing text with 'Unknown'
        for col in self.df.select_dtypes(include=['object']).columns:
            self.df[col] = self.df[col].fillna('Unknown')

        after = self.df.isnull().sum().sum()
        print(f"[CLEAN] {self.filename}: {before} missing values fixed.")

    def get_summary(self):
        """Returns basic stats about the dataset as a dictionary."""
        if self.df is None:
            return {}
        return {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'columns': self.df.columns.tolist(),
        }

    def save_chart(self, fig, chart_name):
        """Saves a matplotlib chart as PNG inside static/charts/."""
        try:
            path = os.path.join(Config.CHART_FOLDER, chart_name)
            fig.savefig(path, bbox_inches='tight', dpi=110)
            plt.close(fig)
            return chart_name
        except Exception as e:
            print(f"[ERROR] Could not save chart {chart_name}: {e}")
            plt.close(fig)
            return None
