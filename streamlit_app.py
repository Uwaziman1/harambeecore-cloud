from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai
import os
import requests
from io import BytesIO
from fpdf import FPDF
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 30 minutes
st_autorefresh(interval=1800 * 1000, key="auto_refresh")

# Page Setup
st.set_page_config(page_title="HarambeeCore Pilot Dashboard", layout="wide")

PRIMARY = "#006600"
ACCENT = "#000000"

# Styles
st.markdown(f"""
    <style>
        html, body, [class*="css"] {{
            color: {ACCENT};
            background-color: #FFFFFF;
            font-family: 'Segoe UI', sans-serif;
        }}
        h1, h2, h3 {{ color: {PRIMARY}; }}
        .stTabs [role="tab"] {{ font-weight: bold; font-size: 16px; color: {PRIMARY}; }}
        .stDownloadButton button {{ background-color: {PRIMARY}; color: white; }}
    </style>
""", unsafe_allow_html=True)

# Fetch Live Price for Header
def fetch_live_price():
    headers = {
        "x-access-token": os.getenv("GOLDAPI_KEY"),
        "Content-Type": "application/json"
    }
    try:
        r = requests.get("https://www.goldapi.io/api/XAU/USD", headers=headers)
        if r.status_code == 200:
            data = r.json()
            return round(data.get("price", 0.0), 2)
        else:
            return None
    except Exception as e:
        print(f"Live price fetch failed: {e}")
        return None

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
        return BytesIO(pdf.output(dest="S").encode("latin-1", errors="ignore"))
    except Exception as e:
        print(f"PDF generation failed: {e}")
        return BytesIO()

# GPT API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Page Header
st.title("HarambeeCore Pilot Dashboard")
st.caption("Audit-level transparency powered by immutable ledgers")

# Always show live XAUUSD price
live_price = fetch_live_price()
if live_price:
    st.metric("Live XAUUSD Price", f"${live_price}")
else:
    st.warning("Live XAUUSD price not available.")

# Mode Toggle
mode = st.radio("Choose Mode", ["Historical Mode", "Live XAUUSD"], horizontal=True)

# Tabs
tabs = st.tabs(["About", "GPT Explorer", "Contact"])

with tabs[0]:
    st.header("About HarambeeCore Dashboard")
    st.markdown("""
The HarambeeCore Dashboard simulates how public finance milestones (such as contracts and payments) could be tracked transparently using real-time gold price data (XAUUSD).

- In **Historical Mode**, milestones are triggered from 2004–2024 data.
- In **Live Mode**, real-time gold price is used to simulate project events when $30 milestones are crossed.
""")

with tabs[1]:
    st.header("GPT Explorer")
    prompt = st.text_area("Ask the GPT-powered analyst (e.g. What happened in 2008?)")
    if prompt:
        if openai.api_key:
            with st.spinner("Getting response..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a financial analyst interpreting historical macroeconomic events."},
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

# === Historical Mode ===
if mode == "Historical Mode":
    if st.button("Run Historical Simulation"):
        with st.spinner("Simulating with historical data..."):
            response = requests.get("https://harambeecore-cloud.onrender.com/simulate")
            result = response.json() if response.status_code == 200 else {}

        if result.get("summary"):
            summary = result["summary"]
            contracts = pd.DataFrame(result["contracts"])
            milestones = pd.DataFrame(result["milestones"])
            gaps = pd.DataFrame(result["gaps"])
            alerts = pd.DataFrame(result["alerts"])
            payments = pd.DataFrame(result["payments"])

            st.subheader("Summary")
            col1, col2 = st.columns(2)
            for i, (k, v) in enumerate(summary.items()):
                (col1 if i % 2 == 0 else col2).metric(label=k, value=str(v))
            buffer = generate_pdf(summary, contracts)
            st.download_button("Download PDF Report", data=buffer.getvalue(), file_name="harambeecore_report.pdf", mime="application/pdf")

            st.subheader("Contracts")
            st.dataframe(contracts, use_container_width=True)

            st.subheader("Milestones")
            st.dataframe(milestones, use_container_width=True)

            st.subheader("Gaps")
            st.dataframe(gaps, use_container_width=True)

            st.subheader("Alerts")
            st.dataframe(alerts, use_container_width=True)

            st.subheader("Payments")
            st.dataframe(payments, use_container_width=True)
        else:
            st.warning("Simulation did not return results. Check backend or data source.")

# === Live Mode ===
elif mode == "Live XAUUSD":
    response = requests.get("https://harambeecore-cloud.onrender.com/simulate?mode=live")
    result = response.json() if response.status_code == 200 else {}

    live_price_backend = result.get("live_price")
    milestone_price = result.get("milestone_price")
    message = result.get("message", "Milestone check complete.")

    st.subheader("Live Simulation Result")
    col1, col2 = st.columns(2)
    col1.metric("Live Price (Backend)", live_price_backend if live_price_backend else "Unavailable")
    col2.metric("Triggered Milestone", milestone_price if milestone_price else "N/A")
    st.info(message)

    if result.get("summary"):
        summary = result["summary"]
        contracts = pd.DataFrame(result["contracts"])

        st.subheader("Live Summary")
        col1, col2 = st.columns(2)
        for i, (k, v) in enumerate(summary.items()):
            (col1 if i % 2 == 0 else col2).metric(label=k, value=str(v))

        st.subheader("Live Contracts")
        st.dataframe(contracts, use_container_width=True)
