import streamlit as st
import pandas as pd
import requests
import openai
import os
from io import BytesIO
from fpdf import FPDF
from dotenv import load_dotenv

# Load secrets
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Page config
st.set_page_config(page_title="HarambeeCore Pilot Dashboard", layout="wide")

# Style
PRIMARY = "#006600"
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
    </style>
""", unsafe_allow_html=True)

# --- PDF Export Fix ---
def safe_text(text):
    return str(text).encode("latin1", "replace").decode("latin1")

def generate_pdf(summary, contracts):
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 102, 0)
    pdf.cell(0, 10, safe_text("HarambeeCore™ Simulation Report"), ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Summary", ln=True)
    pdf.set_font("Arial", size=10)
    for k, v in summary.items():
        pdf.cell(0, 8, safe_text(f"{k}: {v}"), ln=True)

    pdf.ln(5)
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
        pdf.cell(col_width, 8, safe_text(row.get("Milestone", "")), border=1)
        pdf.cell(col_width, 8, safe_text(row.get("Price", "")), border=1)
        pdf.cell(col_width, 8, safe_text(row.get("Gap Context", "")), border=1)
        pdf.ln(8)

    return BytesIO(pdf.output(dest="S").encode("latin1", "replace"))

# --- App Title ---
st.title("HarambeeCore Pilot Dashboard")
st.caption("Audit-level transparency powered by immutable ledgers")

# --- Mode Toggle ---
mode = st.selectbox("Choose Mode", ["Historical", "Live XAUUSD"])

# === HISTORICAL MODE ===
if mode == "Historical":
    if st.button("Run Historical Simulation"):
        with st.spinner("Running historical simulation..."):
            response = requests.get("https://harambeecore-cloud.onrender.com/simulate?mode=historical")
            result = response.json() if response.status_code == 200 else {}

        if result.get("summary"):
            summary = result["summary"]
            milestones = pd.DataFrame(result["milestones"])
            contracts = pd.DataFrame(result["contracts"])
            gaps = pd.DataFrame(result["gaps"])
            alerts = pd.DataFrame(result["alerts"])
            payments = pd.DataFrame(result["payments"])

            tabs = st.tabs(["Summary", "Milestones", "Contracts", "Gaps", "Alerts", "Payments", "GPT Explorer", "Contact"])

            with tabs[0]:
                st.header("Summary")
                col1, col2 = st.columns(2)
                for i, (k, v) in enumerate(summary.items()):
                    (col1 if i % 2 == 0 else col2).metric(k, str(v))
                buffer = generate_pdf(summary, contracts)
                st.download_button("Download PDF Report", buffer.getvalue(), "harambeecore_report.pdf", "application/pdf")

            with tabs[1]:
                st.header("Milestones")
                milestones["Date"] = pd.to_datetime(milestones["Date"], errors="coerce")
                st.dataframe(milestones, use_container_width=True)

            with tabs[2]:
                st.header("Contracts")
                st.dataframe(contracts, use_container_width=True)

            with tabs[3]:
                st.header("Gaps")
                st.dataframe(gaps, use_container_width=True)

            with tabs[4]:
                st.header("Alerts")
                st.dataframe(alerts, use_container_width=True)

            with tabs[5]:
                st.header("Payments")
                st.dataframe(payments, use_container_width=True)

            with tabs[6]:
                st.header("GPT Explorer")
                prompt = st.text_area("Ask the GPT-powered analyst")
                if prompt:
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a financial analyst."},
                                {"role": "user", "content": prompt}
                            ]
                        )
                        st.success(response["choices"][0]["message"]["content"])
                    except Exception as e:
                        st.error(f"OpenAI error: {e}")

            with tabs[7]:
                st.header("Contact")
                st.markdown("""
**Email:** mbuguawian@gmail.com  
**Sponsor:** [GitHub Sponsors](https://github.com/sponsors/uwaziman1)  
**Foundation:** HarambeeCore™ RZ77191
""")

        else:
            st.error("No data returned from simulation.")

# === LIVE MODE ===
elif mode == "Live XAUUSD":
    st.subheader("Live Market Status")

    try:
        response = requests.get("https://harambeecore-cloud.onrender.com/simulate?mode=live", timeout=15)
        result = response.json() if response.status_code == 200 else {}
    except Exception as e:
        st.error(f"Live fetch error: {e}")
        result = {}

    if result.get("live_price") is None:
        st.error("Live data unavailable.")
    else:
        # Live price metrics
        price = result["live_price"]
        open_price = result["open_price"]
        delta = result["delta"]
        milestone_price = result["milestone_price"]
        direction = result.get("milestone_direction", "neutral").upper()
        message = result.get("message", "Milestone check complete.")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Live Price", f"${price}")
        col2.metric("Open Price", f"${open_price}")
        col3.metric("Change Since Open", f"${delta}")
        col4.metric("Milestone", f"${milestone_price}")

        st.info(f"Milestone Direction: **{direction}** — {message}")

        if result.get("summary"):
            st.subheader("Live Summary")
            summary = result["summary"]
            contracts = pd.DataFrame(result.get("contracts", []))
            col1, col2 = st.columns(2)
            for i, (k, v) in enumerate(summary.items()):
                (col1 if i % 2 == 0 else col2).metric(k, str(v))

            st.subheader("Live Contracts")
            st.dataframe(contracts, use_container_width=True)
