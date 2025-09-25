import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# 1. READ DATA FROM A FILE
def read_data(file_path):
    """
    Reads data from a CSV file and returns a pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None

# 2. ANALYZE THE DATA
def analyze_data(df):
    """
    Performs a simple analysis on the DataFrame.
    Returns a dictionary of analysis results.
    """
    if df is None or df.empty:
        return {}
    
    analysis_results = {
        "Total Records": len(df),
        "Numerical Columns Summary": df.describe().to_string(),
        "Missing Values": df.isnull().sum().to_string(),
    }
    
    # You can add more complex analysis here
    # Example: Calculate a specific metric if certain columns exist
    if 'Sales' in df.columns and 'Profit' in df.columns:
        total_sales = df['Sales'].sum()
        total_profit = df['Profit'].sum()
        analysis_results["Total Sales"] = total_sales
        analysis_results["Total Profit"] = total_profit

    return analysis_results

# 3. GENERATE A PDF REPORT
def generate_report(analysis_results, output_filename="automated_report.pdf"):
    """
    Generates a PDF report using ReportLab.
    """
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("Automated Data Analysis Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Summary of Analysis
    story.append(Paragraph("<b>Analysis Summary:</b>", styles['Normal']))
    story.append(Spacer(1, 6))
    
    for key, value in analysis_results.items():
        if key in ["Total Records", "Total Sales", "Total Profit"]:
            p = Paragraph(f"<b>{key}:</b> {value}", styles['Normal'])
            story.append(p)
            story.append(Spacer(1, 6))
    
    # Detailed Data Information (e.g., table or text)
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Detailed Data Overview:</b>", styles['Heading2']))
    story.append(Spacer(1, 6))

    # Displaying summary of numerical columns and missing values as preformatted text
    code_style = styles['Code']
    for key in ["Numerical Columns Summary", "Missing Values"]:
        if key in analysis_results:
            story.append(Paragraph(f"<b>{key}:</b>", styles['Normal']))
            story.append(Paragraph(analysis_results[key], code_style))
            story.append(Spacer(1, 12))

    # Build the PDF
    doc.build(story)
    print(f"Report generated successfully: {output_filename}")

# Main execution block
if __name__ == "__main__":
    # Create a dummy CSV file for demonstration
    dummy_data = {
        'ProductID': [1, 2, 3, 4, 5],
        'Sales': [150.50, 200.75, 50.00, 320.25, 180.00],
        'Profit': [15.5, 25.0, 5.2, 45.8, 18.0],
        'Region': ['North', 'South', 'North', 'East', 'West']
    }
    df_dummy = pd.DataFrame(dummy_data)
    dummy_file_path = "sample_data.csv"
    df_dummy.to_csv(dummy_file_path, index=False)
    
    # --- Main Workflow ---
    file_to_process = dummy_file_path
    
    # 1. Read data
    data_frame = read_data(file_to_process)
    
    if data_frame is not None:
        # 2. Analyze data
        results = analyze_data(data_frame)
        
        # 3. Generate report
        generate_report(results)