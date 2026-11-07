import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

# 1. Ask the user for the file name (or you can hardcode it)
file_name = input("Enter the exact file name in the data/ folder (e.g., new_data.csv): ")
file_path = os.path.join('data', file_name)

if not os.path.exists(file_path):
    print(f"❌ Error: {file_path} not found.")
    exit()

# 2. Load the data (handles both CSV and Excel)
print("Loading data...")
if file_name.endswith('.csv'):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')
elif file_name.endswith('.xlsx'):
    df = pd.read_excel(file_path)
else:
    print("❌ Unsupported file format. Use .csv or .xlsx")
    exit()

# 3. Calculate Data Quality Metrics
total_rows = len(df)
total_cols = len(df.columns)
duplicate_rows = df.duplicated().sum()

# Missing values per column
missing_data = df.isnull().sum()
missing_data = missing_data[missing_data > 0]

# Data types
dtypes = df.dtypes.astype(str)

# 4. Build the PDF
print("Generating PDF Report...")
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Automated Data Quality Profile', 0, 1, 'C')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', '', 12)

# Summary Section
pdf.multi_cell(0, 8, f"File Analyzed: {file_name}\n"
                      f"Total Rows: {total_rows}\n"
                      f"Total Columns: {total_cols}\n"
                      f"Duplicate Rows: {duplicate_rows}\n")
pdf.ln(10)

# Missing Values Section
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Missing Values by Column:', 0, 1)
pdf.set_font('Arial', '', 10)
if missing_data.empty:
    pdf.cell(0, 8, "No missing values found! (Clean dataset)", 0, 1)
else:
    for col, count in missing_data.items():
        pdf.cell(0, 8, f"- {col}: {count} missing values", 0, 1)
pdf.ln(10)

# Column Types Section
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Column Data Types:', 0, 1)
pdf.set_font('Arial', '', 10)
for col, dtype in dtypes.items():
    pdf.cell(0, 8, f"- {col}: {dtype}", 0, 1)

# Save the PDF
output_path = f"reports/Profile_{file_name.split('.')[0]}.pdf"
pdf.output(output_path)
print(f"✅ Success! Profile saved to {output_path}")