import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai
import os
from run_pipeline import run_pipeline
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="HarambeeCore Pilot Dashboard", layout="wide")

PRIMARY = "#006600"
SECONDARY = "#FF0000"
ACCENT = "#000000"

st.markdown(f"""
    <style>
        html, body, [class*="css"]  {{
            color: {ACCENT};
            background-color: #FFFFFF;
            font-family: 'Segoe UI', sans-serif;
        }}
        h1, h2, h3 {{ color: {PRIMARY}; }}
        .stTabs [role="tab"] {{ font-weight: bold; font-size: 16px; color: {PRIMARY}; }}
        .stDownloadButton button {{ background-color: {PRIMARY}; color: white; }}
        .tag-chip {{ background-color: #eee; color: #000; font-size: 0.8rem; padding: 3px 8px; margin: 0 4px; border-radius: 5px; display: inline-block; }}
        .status-ok {{ background-color: #28a745; color: white; }}
        .status-warn {{ background-color: #ffc107; color: black; }}
        .status-error {{ background-color: #dc3545; color: white; }}
    </style>
""", unsafe_allow_html=True)

def generate_pdf(summary, contracts):
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 102, 0)
    pdf.cell(0, 10, "HarambeeCore™ Simulation Report", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Summary", ln=True)
    pdf.set_font("Arial", size=10)
    for k, v in summary.items():
        pdf.cell(0, 8, f"{k}: {v}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Contracts", ln=True)
    pdf.set_font("Arial", size=10)
    col_width = pdf.w / 4.5
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(col_width, 8, "Milestone", border=1, fill=True)
    pdf.cell(col_width, 8, "Price", border=1, fill=True)
    pdf.cell(col_width, 8, "Gap Context", border=1, fill=True)
    pdf.ln(8)
    for _, row in contracts.iterrows():
        pdf.cell(col_width, 8, str(row['Milestone']), border=1)
        pdf.cell(col_width, 8, str(row['Price']), border=1)
        pdf.cell(col_width, 8, str(row['Gap Context']), border=1)
        pdf.ln(8)

    buffer = BytesIO()
    buffer.write(pdf.output(dest="S").encode("latin-1"))
    buffer.seek(0)
    return buffer

openai.api_key = os.getenv("OPENAI_API_KEY")

# Remaining app logic continues unchanged...
