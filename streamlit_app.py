import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai
import os
from run_pipeline import run_pipeline
from fpdf import FPDF
from io import BytesIO
import os
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

from fpdf import FPDF
from io import BytesIO

def generate_pdf(summary, contracts):
    pdf = FPDF("P", "mm", "A4")

    # Load DejaVuSans from same directory as script
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.add_page()
    pdf.set_text_color(0, 102, 0)
    pdf.cell(0, 10, "HarambeeCore™ Simulation Report", ln=True, align="C")
    pdf.ln(5)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("DejaVu", size=10)
    pdf.cell(0, 10, "Summary", ln=True)
    for k, v in summary.items():
        pdf.cell(0, 8, f"{k}: {v}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 10, "Contracts", ln=True)
    col_width = pdf.w / 4.5
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(col_width, 8, "Milestone", border=1, fill=True)
    pdf.cell(col_width, 8, "Price", border=1, fill=True)
    pdf.cell(col_width, 8, "Gap Context", border=1, fill=True)
    pdf.ln(8)

    for _, row in contracts.iterrows():
        milestone = str(row.get("Milestone", "N/A"))
        price = str(row.get("Price", "N/A"))
        context = str(row.get("Gap Context", "N/A"))
        pdf.cell(col_width, 8, milestone, border=1)
        pdf.cell(col_width, 8, price, border=1)
        pdf.cell(col_width, 8, context, border=1)
        pdf.ln(8)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer



openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("\U0001F4D8 HarambeeCore Pilot Dashboard")
st.caption("Audit-level transparency powered by immutable ledgers")

if st.button("\U0001F680 Run Simulation"):
    with st.spinner("Simulating bridge progress and contracts..."):
        result = run_pipeline()

    if isinstance(result, dict) and result.get("milestones") is not None:
        tabs = st.tabs(["Summary", "Milestones", "Contracts", "Gaps", "Alerts", "Payments", "GPT Explorer", "Contact"])

        with tabs[0]:
            st.header("\U0001F4CB Project Summary")
            col1, col2 = st.columns(2)
            with col1:
                for k, v in list(result["summary"].items())[:3]:
                    st.metric(label=k, value=str(v))
            with col2:
                for k, v in list(result["summary"].items())[3:]:
                    st.metric(label=k, value=str(v))
            buffer = generate_pdf(result["summary"], result["contracts"])
            st.download_button(
                label="📄 Download PDF Report",
                data=buffer.getvalue(),
                file_name="harambeecore_report.pdf",
                mime="application/pdf"
            )
