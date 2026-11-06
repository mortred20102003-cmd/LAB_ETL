import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from datetime import datetime

# 1. DATABASE CONFIGURATION
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "YOUR_PASSWORD_HERE",
    "host": "localhost",
    "port": "5432"
}

def fetch_data(query):
    """Fetches data from PostgreSQL and returns a pandas DataFrame."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Database error: {e}")
        return None

def create_chart(df, title, filename):
    """Creates a bar chart and saves it as an image."""
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
        self.cell(0, 10, 'ETL Pipeline & Data Quality Summary', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'C')

def generate_pdf():
    print("Fetching data from database...")
    
    # Query 1: Average Area per Date Fruit Class
    q1 = """
    SELECT c.class_name, ROUND(AVG(f.area), 2) as avg_area
    FROM dw.fact_date_fruit f 
    JOIN dw.dim_class c ON f.class_key = c.class_key 
    GROUP BY c.class_name 
    ORDER BY avg_area DESC;
    """
    df_company = fetch_data(q1)

    # Query 2: Count of fruits per class
    q2 = """
    SELECT c.class_name, COUNT(*) as total_count
    FROM dw.fact_date_fruit f
    JOIN dw.dim_class c ON f.class_key = c.class_key
    GROUP BY c.class_name
    ORDER BY total_count DESC;
    """
    df_fuel = fetch_data(q2)

    if df_company is None or df_fuel is None:
        print("Failed to fetch data. Check your database connection.")
        return

    print("Generating charts...")
    chart1 = create_chart(df_company, "Average Area by Date Fruit Class", "chart_class.png")
    chart2 = create_chart(df_fuel, "Total Count per Date Fruit Class", "chart_count.png")

    print("Building PDF...")
    pdf = PDFReport()
    pdf.add_page()
    
    # Add Summary Text
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, "Data Quality & ETL Summary:\n\n"
                          "- Extracted dataset from Kaggle (Date Fruit Datasets).\n"
                          "- Loaded 898 rows of image-extracted features.\n"
                          "- Loaded data into a Star Schema (fact_date_fruit, dim_class).\n"
                          "- Classified 7 different varieties of date fruits.")
    pdf.ln(10)

    # Add Charts
    if chart1 and os.path.exists(chart1):
        pdf.image(chart1, x=15, w=180)
        pdf.ln(10)
    
    if chart2 and os.path.exists(chart2):
        pdf.image(chart2, x=15, w=180)

    # Save PDF
    output_path = "reports/Date_Fruit_Report.pdf"
    pdf.output(output_path)
    print(f"✅ Success! PDF saved to {output_path}")

    # Clean up temporary chart images
    if chart1 and os.path.exists(chart1): os.remove(chart1)
    if chart2 and os.path.exists(chart2): os.remove(chart2)

if __name__ == "__main__":
    generate_pdf()