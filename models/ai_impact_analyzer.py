import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from models.base_analyzer import BaseAnalyzer


class AIImpactAnalyzer(BaseAnalyzer):
    """
    Child class of BaseAnalyzer.
    Assigned to: Flores, Aivan
    Dataset: ai_student_impact_dataset-1.csv

    OOP concepts used here:
    - Inheritance: this class extends BaseAnalyzer
    - Method overriding: clean_data() overrides the parent version
    - super().__init__(): calls the parent constructor
    """

    def __init__(self):
        # Call parent constructor with the CSV filename
        super().__init__('ai_student_impact_dataset-1.csv')

    def clean_data(self):
        """
        Custom cleaning for this dataset.
        Since the dataset has no missing values, this mostly
        just calls the parent clean and confirms the data is ready.
        """
        if self.df is None:
            return
        # Call parent's clean_data first
        super().clean_data()
        # Remove duplicate rows just in case
        self.df.drop_duplicates(inplace=True)

    def generate_charts(self):
        """
        Generates all charts for the dashboard.
        Returns a list of saved chart filenames.
        Each chart is saved as a PNG in static/charts/.
        """
        if self.df is None:
            return []

        charts = []

        # Chart 1: Students per Major Category (bar chart)
        charts.append(self._chart_major_category())

        # Chart 2: Burnout Risk Level distribution (pie chart)
        charts.append(self._chart_burnout_risk())

        # Chart 3: Average Weekly GenAI Hours by Year of Study (bar chart)
        charts.append(self._chart_genai_hours_by_year())

        # Chart 4: Pre vs Post Semester GPA comparison (bar chart)
        charts.append(self._chart_gpa_comparison())

        # Chart 5: Primary Use Case of AI tools (horizontal bar)
        charts.append(self._chart_primary_use_case())

        # Chart 6: Prompt Engineering Skill Level (pie chart)
        charts.append(self._chart_skill_level())

        # Remove any None values (charts that failed to save)
        return [c for c in charts if c is not None]

    # ── Individual Chart Methods ──────────────────────────────────────────

    def _chart_major_category(self):
        """Bar chart: Number of students per major."""
        try:
            counts = self.df['Major_Category'].value_counts()

            fig, ax = plt.subplots(figsize=(8, 5))
            bars = ax.bar(counts.index, counts.values,
                          color=['#4e79a7','#f28e2b','#e15759','#76b7b2','#59a14f'],
                          edgecolor='white')

            # Add count labels on top of each bar
            for bar in bars:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 30,
                        str(int(bar.get_height())),
                        ha='center', va='bottom', fontsize=10, fontweight='bold')

            ax.set_title('Number of Students per Major Category', fontsize=14, pad=15)
            ax.set_xlabel('Major Category', fontsize=11)
            ax.set_ylabel('Number of Students', fontsize=11)
            ax.set_ylim(0, counts.values.max() + 500)
            ax.grid(axis='y', linestyle='--', alpha=0.5)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            fig.tight_layout()

            return self.save_chart(fig, 'chart_major_category.png')
        except Exception as e:
            print(f"[Chart Error] Major category: {e}")
            return None

    def _chart_burnout_risk(self):
        """Pie chart: Burnout risk level distribution."""
        try:
            counts = self.df['Burnout_Risk_Level'].value_counts()
            colors = {'High': '#e15759', 'Medium': '#f28e2b', 'Low': '#59a14f'}
            color_list = [colors.get(k, '#aaa') for k in counts.index]

            fig, ax = plt.subplots(figsize=(6, 6))
            wedges, texts, autotexts = ax.pie(
                counts.values,
                labels=counts.index,
                autopct='%1.1f%%',
                colors=color_list,
                startangle=90,
                wedgeprops=dict(edgecolor='white', linewidth=2)
            )
            for t in autotexts:
                t.set_fontsize(11)
                t.set_fontweight('bold')

            ax.set_title('Burnout Risk Level Distribution', fontsize=14, pad=20)
            fig.tight_layout()

            return self.save_chart(fig, 'chart_burnout_risk.png')
        except Exception as e:
            print(f"[Chart Error] Burnout risk: {e}")
            return None

    def _chart_genai_hours_by_year(self):
        """Bar chart: Average weekly GenAI hours per year of study."""
        try:
            order = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
            avg = self.df.groupby('Year_of_Study')['Weekly_GenAI_Hours'].mean()
            avg = avg.reindex([y for y in order if y in avg.index])

            fig, ax = plt.subplots(figsize=(8, 5))
            bars = ax.bar(avg.index, avg.values,
                          color='#4e79a7', edgecolor='white')

            for bar in bars:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.1,
                        f'{bar.get_height():.1f} hrs',
                        ha='center', va='bottom', fontsize=10)

            ax.set_title('Average Weekly GenAI Hours by Year of Study', fontsize=14, pad=15)
            ax.set_xlabel('Year of Study', fontsize=11)
            ax.set_ylabel('Avg Weekly GenAI Hours', fontsize=11)
            ax.grid(axis='y', linestyle='--', alpha=0.5)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            fig.tight_layout()

            return self.save_chart(fig, 'chart_genai_hours.png')
        except Exception as e:
            print(f"[Chart Error] GenAI hours: {e}")
            return None

    def _chart_gpa_comparison(self):
        """Grouped bar chart: Average Pre vs Post GPA per major."""
        try:
            grouped = self.df.groupby('Major_Category')[['Pre_Semester_GPA', 'Post_Semester_GPA']].mean()

            x = np.arange(len(grouped.index))
            width = 0.35

            fig, ax = plt.subplots(figsize=(9, 5))
            bars1 = ax.bar(x - width/2, grouped['Pre_Semester_GPA'],
                           width, label='Pre-Semester GPA', color='#4e79a7', edgecolor='white')
            bars2 = ax.bar(x + width/2, grouped['Post_Semester_GPA'],
                           width, label='Post-Semester GPA', color='#f28e2b', edgecolor='white')

            ax.set_title('Average Pre vs Post Semester GPA by Major', fontsize=14, pad=15)
            ax.set_xlabel('Major Category', fontsize=11)
            ax.set_ylabel('Average GPA', fontsize=11)
            ax.set_xticks(x)
            ax.set_xticklabels(grouped.index)
            ax.legend()
            ax.set_ylim(0, 4.5)
            ax.grid(axis='y', linestyle='--', alpha=0.5)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            fig.tight_layout()

            return self.save_chart(fig, 'chart_gpa_comparison.png')
        except Exception as e:
            print(f"[Chart Error] GPA comparison: {e}")
            return None

    def _chart_primary_use_case(self):
        """Horizontal bar chart: How students primarily use AI."""
        try:
            counts = self.df['Primary_Use_Case'].value_counts()

            fig, ax = plt.subplots(figsize=(9, 5))
            bars = ax.barh(counts.index[::-1], counts.values[::-1],
                           color='#76b7b2', edgecolor='white')

            for bar in bars:
                ax.text(bar.get_width() + 30,
                        bar.get_y() + bar.get_height() / 2,
                        str(int(bar.get_width())),
                        va='center', fontsize=10)

            ax.set_title('Primary Use Case of AI Tools Among Students', fontsize=14, pad=15)
            ax.set_xlabel('Number of Students', fontsize=11)
            ax.grid(axis='x', linestyle='--', alpha=0.5)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            fig.tight_layout()

            return self.save_chart(fig, 'chart_use_case.png')
        except Exception as e:
            print(f"[Chart Error] Use case: {e}")
            return None

    def _chart_skill_level(self):
        """Pie chart: Prompt engineering skill level distribution."""
        try:
            counts = self.df['Prompt_Engineering_Skill'].value_counts()
            colors = ['#59a14f', '#f28e2b', '#e15759']

            fig, ax = plt.subplots(figsize=(6, 6))
            wedges, texts, autotexts = ax.pie(
                counts.values,
                labels=counts.index,
                autopct='%1.1f%%',
                colors=colors,
                startangle=90,
                wedgeprops=dict(edgecolor='white', linewidth=2)
            )
            for t in autotexts:
                t.set_fontsize(11)
                t.set_fontweight('bold')

            ax.set_title('Prompt Engineering Skill Level', fontsize=14, pad=20)
            fig.tight_layout()

            return self.save_chart(fig, 'chart_skill_level.png')
        except Exception as e:
            print(f"[Chart Error] Skill level: {e}")
            return None
