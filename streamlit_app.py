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
        milestone = str(row.get('Milestone', 'N/A'))
        price = str(row.get('Price', 'N/A'))
        context = str(row.get('Gap Context', 'N/A'))
        pdf.cell(col_width, 8, milestone, border=1)
        pdf.cell(col_width, 8, price, border=1)
        pdf.cell(col_width, 8, context, border=1)
        pdf.ln(8)

    try:
        pdf_bytes = pdf.output(dest="S").encode("latin-1", errors="ignore")
        buffer = BytesIO(pdf_bytes)
        return buffer
    except Exception as e:
        print(f"PDF generation failed: {e}")
        return BytesIO()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("HarambeeCore Pilot Dashboard")
st.caption("Audit-level transparency powered by immutable ledgers")

if st.button("Run Simulation"):
    with st.spinner("Simulating bridge progress and contracts..."):
        result = run_pipeline()

    if isinstance(result, dict) and result.get("milestones") is not None:
        tabs = st.tabs(["About", "Summary", "Milestones", "Contracts", "Gaps", "Alerts", "Payments", "GPT Explorer", "Contact"])

        with tabs[0]:
            st.header("About HarambeeCore Dashboard")
            st.markdown("""
The HarambeeCore Dashboard is a live prototype that demonstrates how technology can bring real-time transparency to public finance.

Using historical XAUUSD (gold price) data from 2004, the system tracks price movements and triggers milestones whenever prices cross significant thresholds — every $100 and $1,000 mark. These milestones simulate public fund events (like disbursements, audits, or allocations).

Each milestone automatically:
- Generates a smart contract
- Sends real-time alerts via email or WhatsApp to simulate notifications to key departments

This prototype showcases how automated, rule-based financial monitoring can replace manual oversight, reduce corruption, and empower citizens with visibility into fund movements.

HarambeeCore is the foundation for HarambeeCoin, a blockchain-based ecosystem designed to rebuild trust in governance through accountability, automation, and people-first design.
""")

        else:
        st.warning("Simulation did not return results. Check for errors in the pipeline.")

        with tabs[1]:
            st.subheader("Summary tab will appear here once data is ready.")

        with tabs[2]:
            st.subheader("Milestones tab will appear here once data is ready.")

        with tabs[3]:
            st.subheader("Contracts tab will appear here once data is ready.")

        with tabs[4]:
            st.subheader("Gap analysis tab will appear here once data is ready.")

        with tabs[5]:
            st.subheader("Alerts tab will appear here once data is ready.")

        with tabs[6]:
            st.subheader("Payments tab will appear here once data is ready.")

        with tabs[7]:
            st.subheader("GPT Explorer tab will appear here once data is ready.")

        with tabs[8]:
            st.subheader("Contact tab will appear here once data is ready.")
