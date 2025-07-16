import streamlit as st
import pandas as pd
import requests
import openai
import os
from io import BytesIO
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="HarambeeCore Pilot Dashboard", layout="wide")

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

# Title
st.title("HarambeeCore Pilot Dashboard")
st.caption("Audit-level transparency powered by immutable ledgers")

# Mode Toggle
mode = st.radio("Choose Mode", ["Historical", "Live XAUUSD"], horizontal=True)

# === HISTORICAL ===
if mode == "Historical":
    if st.button("Run Historical Simulation"):
        with st.spinner("Simulating..."):
            res = requests.get("https://harambeecore-cloud.onrender.com/simulate?mode=historical")
            result = res.json() if res.status_code == 200 else {}

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
                st.dataframe(milestones)
                if not milestones.empty and "Price" in milestones.columns:
                    st.line_chart(milestones.set_index("Date")["Price"])

            with tabs[2]:
                st.header("Contracts")
                st.dataframe(contracts)
                if not contracts.empty and "Price" in contracts.columns:
                    st.bar_chart(contracts.set_index("Milestone")["Price"])

            with tabs[3]:
                st.header("Gaps")
                gaps["Date"] = pd.to_datetime(gaps["Date"], errors="coerce")
                st.dataframe(gaps)
                if not gaps.empty:
                    st.line_chart(gaps.set_index("Date")["Gap"])

            with tabs[4]:
                st.header("Alerts")
                alerts["Date"] = pd.to_datetime(alerts["Date"], errors="coerce")
                st.dataframe(alerts)

            with tabs[5]:
                st.header("Payments")
                payments["Date"] = pd.to_datetime(payments["Date"], errors="coerce")
                st.dataframe(payments)

            with tabs[6]:
                st.header("GPT Explorer")
                prompt = st.text_area("Ask the GPT-powered analyst")
                if prompt:
                    try:
                        gpt = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a financial analyst."},
                                {"role": "user", "content": prompt}
                            ]
                        )
                        st.success(gpt["choices"][0]["message"]["content"])
                    except Exception as e:
                        st.error(f"OpenAI error: {e}")

            with tabs[7]:
                st.header("Contact")
                st.markdown("""
**Email:** mbuguawian@gmail.com  
**Sponsor:** [GitHub Sponsors](https://github.com/sponsors/uwaziman1)  
**Foundation:** HarambeeCore™ RZ77191
""")

# === LIVE MODE ===
if mode == "Live XAUUSD":
    st.subheader("Live Market Status")
    try:
        r = requests.get("https://harambeecore-cloud.onrender.com/simulate?mode=live", timeout=10)
        data = r.json() if r.status_code == 200 else {}
    except Exception as e:
        st.error(f"Live fetch failed: {e}")
        data = {}

    if data.get("live_price"):
        st.metric("Live Price", f"${data['live_price']}")
        st.metric("Open Price", f"${data['open_price']}")
        st.metric("Change Since Open", f"${data['delta']}")
        st.metric("Current Milestone", f"${data['milestone_price']}")
        st.info(f"Milestone Direction: {data['milestone_direction']}")
        st.success(data["message"])

        if data.get("summary"):
            st.subheader("Live Snapshot Summary")
            for k, v in data["summary"].items():
                st.metric(k, str(v))
    else:
        st.error("Live data unavailable.")
