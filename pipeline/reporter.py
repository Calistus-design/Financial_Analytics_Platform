"""
PDF Reporting Module.

This module is responsible for generating a daily executive summary report
in PDF format. It takes the cleaned and transformed data, calculates key
summary metrics, generates a relevant visualization, and uses a Jinja2
template to render the final report.
"""
import os
import pandas as pd
from typing import List
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

# Define paths relative to this script's location
PIPELINE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.join(PIPELINE_DIR, '..')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')
CHART_PATH = os.path.join(REPORTS_DIR, 'daily_performance_chart.png')
TEMPLATE_PATH = PIPELINE_DIR

# Ensure the reports directory exists
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_pdf_report(clean_records: List[dict]):
    """
    Generates a polished PDF report from a list of clean stock data records.
    """
    if not clean_records:
        print("No data available to generate a report.")
        return

    df = pd.DataFrame(clean_records)
    df['date'] = pd.to_datetime(df['date'])
    
    # --- 1. Calculate Summary Metrics (same as before) ---
    latest_date = df['date'].max().strftime('%Y-%m-%d')
    num_symbols = df['symbol'].nunique()
    total_volume = df['volume'].sum()
    df['pct_change'] = (df['close'] - df['open']) / df['open'] * 100
    # Sort by pct_change to reliably find gainer/loser in case of duplicates
    df_sorted = df.sort_values('pct_change', ascending=False)
    top_gainer = df_sorted.iloc[0]
    top_loser = df_sorted.iloc[-1]
    
    summary_metrics = {
        "latest_date": latest_date,
        "num_symbols": num_symbols,
        "total_volume": f"{total_volume:,}",
        "top_gainer_symbol": top_gainer['symbol'],
        "top_gainer_pct": f"{top_gainer['pct_change']:.2f}%",
        "top_loser_symbol": top_loser['symbol'],
        "top_loser_pct": f"{top_loser['pct_change']:.2f}%"
    }
    
    # --- 2. Generate POLISHED Chart ---
    sns.set_theme(style="whitegrid") # Use a clean theme
    plt.figure(figsize=(10, 6))
    
    # Create a color palette: green for positive, red for negative
    colors = ['#28a745' if c >= 0 else '#dc3545' for c in df_sorted['pct_change']]
    
    ax = sns.barplot(data=df_sorted, x='symbol', y='pct_change', palette=colors)
    
    # Add value labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f%%')

    plt.title(f'Daily Performance (% Change) - {latest_date}', fontsize=16, weight='bold')
    plt.ylabel('% Change (Open to Close)', fontsize=12)
    plt.xlabel('Stock Symbol', fontsize=12)
    ax.axhline(0, color='grey', linewidth=0.8) # Add a zero line
    plt.tight_layout()
    plt.savefig(CHART_PATH, dpi=300) # Save with higher resolution
    plt.close()
    print(f"Polished chart saved to {CHART_PATH}")

    # --- 3. Render HTML from POLISHED Template ---
    env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
    template = env.get_template('report_template.html')
    html_out = template.render(
        metrics=summary_metrics, 
        chart_path=f"file:///{os.path.abspath(CHART_PATH)}"
    )
    
    # --- 4. Convert HTML to PDF with CSS ---
    # Add CSS for better styling
    css = CSS(string='''
        @page { size: A4; margin: 1in; }
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333; }
        h1 { color: #003366; border-bottom: 2px solid #003366; padding-bottom: 10px; }
        h2 { color: #444; }
        table { border-collapse: collapse; width: 60%; margin-bottom: 30px; }
        th, td { border: 1px solid #ccc; padding: 12px; text-align: left; }
        th { background-color: #f0f0f0; font-weight: bold; }
        img { max-width: 90%; height: auto; border: 1px solid #ddd; padding: 5px; }
    ''')
    report_filename = f"daily_summary_{latest_date}.pdf"
    report_path = os.path.join(REPORTS_DIR, report_filename)
    HTML(string=html_out).write_pdf(report_path, stylesheets=[css])
    print(f"Polished PDF report generated: {report_path}")

# Test function remains the same for creating the template and running the report
if __name__ == '__main__':
    template_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Daily Stock Market Summary</title>
    </head>
    <body>
        <h1>Daily Stock Market Summary: {{ metrics.latest_date }}</h1>
        <h2>Key Metrics</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Symbols Tracked</td><td>{{ metrics.num_symbols }}</td></tr>
            <tr><td>Total Volume</td><td>{{ metrics.total_volume }}</td></tr>
            <tr><td>Top Gainer</td><td>{{ metrics.top_gainer_symbol }} ({{ metrics.top_gainer_pct }})</td></tr>
            <tr><td>Top Loser</td><td>{{ metrics.top_loser_symbol }} ({{ metrics.top_loser_pct }})</td></tr>
        </table>
        <h2>Daily Performance Chart</h2>
        <img src="{{ chart_path }}" alt="Daily Performance Chart">
    </body>
    </html>
    """
    with open(os.path.join(TEMPLATE_PATH, 'report_template.html'), 'w') as f:
        f.write(template_content)
    
    sample_records = [
        {'symbol': 'GOOG', 'date': '2024-01-01', 'open': 130.0, 'high': 132.5, 'low': 129.5, 'close': 132.0, 'volume': 100000},
        {'symbol': 'AAPL', 'date': '2024-01-01', 'open': 170.0, 'high': 171.0, 'low': 169.0, 'close': 169.5, 'volume': 120000},
        {'symbol': 'MSFT', 'date': '2024-01-01', 'open': 300.0, 'high': 305.0, 'low': 299.0, 'close': 304.5, 'volume': 80000},
    ]
    generate_pdf_report(sample_records)