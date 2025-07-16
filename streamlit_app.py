import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai
import os
import requests
from io import BytesIO
from fpdf import FPDF

# Page Setup
st.set_page_config(page_title="HarambeeCore Pilot Dashboard", layout="wide")

PRIMARY = "#006600"
SECONDARY = "#FF0000"
ACCENT = "#000000"

# Styles
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

# PDF Export
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
    pdf.cell(0, 10, "Contracts", ln=True)
    pdf.set_font("Arial", size=10)
    col_width = pdf.w / 4.5
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(col_width, 8, "Milestone", border=1, fill=True)
    pdf.cell(col_width, 8, "Price", border=1, fill=True)
    pdf.cell(col_width, 8, "Gap Context", border=1, fill=True)
    pdf.ln(8)
    contracts_df = pd.DataFrame(contracts)
    for _, row in contracts_df.iterrows():
        pdf.cell(col_width, 8, str(row.get("Milestone", "N/A")), border=1)
        pdf.cell(col_width, 8, str(row.get("Price", "N/A")), border=1)
        pdf.cell(col_width, 8, str(row.get("Gap Context", "N/A")), border=1)
        pdf.ln(8)

    try:
        pdf_bytes = pdf.output(dest="S").encode("latin-1", errors="ignore")
        buffer = BytesIO(pdf_bytes)
        return buffer
    except Exception as e:
        print(f"PDF generation failed: {e}")
        return BytesIO()

# OpenAI GPT API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Title and Mode
st.title("HarambeeCore Pilot Dashboard")
st.caption("Audit-level transparency powered by immutable ledgers")

mode = st.radio("Choose Mode", ["Historical Mode", "Live XAUUSD (Phase 2)"], horizontal=True)

# Always-visible tabs
tabs = st.tabs(["About", "GPT Explorer", "Contact"])

with tabs[0]:
    st.header("About HarambeeCore Dashboard")
    st.markdown("""
The HarambeeCore Dashboard demonstrates how real-time tech can bring transparency to public finance.

Using either historical or live gold price data (XAUUSD), the system tracks price movements and triggers milestones at every $30 interval. These milestones simulate public fund events (like disbursements or audits), and automatically generate smart contracts, alerts, and payments.

HarambeeCore is the foundation for HarambeeCoin, a blockchain ecosystem designed to rebuild trust in governance.
""")

with tabs[1]:
    st.header("GPT Explorer")
    prompt = st.text_area("Ask the GPT-powered analyst (e.g. What happened in 2008?)")
    if prompt:
        if openai.api_key:
            with st.spinner("Getting response from GPT..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a financial analyst helping users interpret historical market-linked events."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    st.success(response["choices"][0]["message"]["content"])
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Missing OpenAI API key.")

with tabs[2]:
    st.header("Contact")
    st.markdown("""
**Email:** mbuguawian@gmail.com  
**Sponsor:** [GitHub Sponsors](https://github.com/sponsors/uwaziman1)  
**Foundation:** HarambeeCore™ RZ77191
""")

# Historical Mode
if mode == "Historical Mode":
    if st.button("Run Historical Simulation"):
        with st.spinner("Simulating with historical data..."):
            response = requests.get("https://harambeecore-cloud.onrender.com/simulate")
            result = response.json() if response.status_code == 200 else {}

        if result.get("milestones"):
            summary = result["summary"]
            contracts = pd.DataFrame(result["contracts"])
            milestones = pd.DataFrame(result["milestones"])
            gaps = pd.DataFrame(result["gaps"])
            alerts = pd.DataFrame(result["alerts"])
            payments = pd.DataFrame(result["payments"])

            sim_tabs = st.tabs(["Summary", "Milestones", "Contracts", "Gaps", "Alerts", "Payments"])

            with sim_tabs[0]:
                st.header("Summary")
                col1, col2 = st.columns(2)
                for i, (k, v) in enumerate(summary.items()):
                    (col1 if i % 2 == 0 else col2).metric(label=k, value=str(v))
                buffer = generate_pdf(summary, contracts)
                st.download_button("Download PDF Report", data=buffer.getvalue(), file_name="harambeecore_report.pdf", mime="application/pdf")

            with sim_tabs[1]:
                st.header("Milestones")
                milestones["Date"] = pd.to_datetime(milestones["Date"], errors="coerce")
                st.dataframe(milestones, use_container_width=True)

            with sim_tabs[2]:
                st.header("Contracts")
                st.dataframe(contracts, use_container_width=True)

            with sim_tabs[3]:
                st.header("Gaps")
                st.dataframe(gaps, use_container_width=True)

            with sim_tabs[4]:
                st.header("Alerts")
                st.dataframe(alerts, use_container_width=True)

            with sim_tabs[5]:
                st.header("Payments")
                st.dataframe(payments, use_container_width=True)

        else:
            st.warning("No milestones returned. Check backend or data source.")

# Live Mode
elif mode == "Live XAUUSD (Phase 2)":
    if st.button("Check Live Price"):
        with st.spinner("Fetching live XAUUSD data..."):
            response = requests.get("https://harambeecore-cloud.onrender.com/simulate?mode=live")
            result = response.json() if response.status_code == 200 else {}

        if result.get("error"):
            st.error(result["error"])
        elif result.get("summary"):
            st.success(f"Live XAUUSD Price: {result['live_price']}")
            st.info(f"Triggered Milestone: {result['milestone_price']}")

            summary = result["summary"]
            contracts = pd.DataFrame(result["contracts"])

            live_tabs = st.tabs(["Summary", "Contracts"])

            with live_tabs[0]:
                st.header("Live Summary")
                col1, col2 = st.columns(2)
                for i, (k, v) in enumerate(summary.items()):
                    (col1 if i % 2 == 0 else col2).metric(label=k, value=str(v))

            with live_tabs[1]:
                st.header("Live Contracts")
                st.dataframe(contracts, use_container_width=True)
        else:
            st.warning("Live pipeline returned no data.")
