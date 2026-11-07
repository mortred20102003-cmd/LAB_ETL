import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from datetime import datetime

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "YOUR_PASSWORD_HERE",
    "host": "localhost",
    "port": "5432"
}

def fetch_data(query):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Database error: {e}")
        return None

def create_chart(df, title, filename):
    if df is None or df.empty:
        return None
    plt.figure(figsize=(8, 4))
    plt.bar(df.iloc[:, 0], df.iloc[:, 1], color='skyblue')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Student Stress Analysis Summary', 0, 1, 'C')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'C')

def generate_pdf():
    print("Fetching data from database...")
    
    # Query: Average Anxiety Level per Stress Category
    q1 = """
    SELECT d.level_name, ROUND(AVG(f.anxiety_level), 2) as avg_anxiety
    FROM dw_stress1.fact_student_stress f 
    JOIN dw_stress1.dim_stress_level d ON f.level_key = d.level_key 
    GROUP BY d.level_name 
    ORDER BY avg_anxiety DESC;
    """
    df_stress = fetch_data(q1)

    if df_stress is None:
        print("Failed to fetch data. Check your database connection.")
        return

    print("Generating chart...")
    chart1 = create_chart(df_stress, "Average Anxiety Level by Stress Category", "chart_stress.png")

    print("Building PDF...")
    pdf = PDFReport()
    pdf.add_page()
    
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, "Data Quality & ETL Summary:\n\n"
                          "- Extracted Student Stress dataset from Kaggle.\n"
                          "- Loaded 1100 rows of survey responses.\n"
                          "- Designed Star Schema with dim_stress_level and fact_student_stress.\n"
                          "- Analyzed anxiety levels across Low, Moderate, and High stress groups.")
    pdf.ln(10)

    if chart1 and os.path.exists(chart1):
        pdf.image(chart1, x=15, w=180)

    output_path = "reports/Stress_Analysis_Report.pdf"
    pdf.output(output_path)
    print(f"✅ Success! PDF saved to {output_path}")

    if chart1 and os.path.exists(chart1): os.remove(chart1)

if __name__ == "__main__":
    generate_pdf()