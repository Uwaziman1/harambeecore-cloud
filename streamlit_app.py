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

elif mode == "live":
    data = get_live_gold_data()
    if not data:
        return {
            "error": "Failed to fetch live gold data",
            "live_price": None,
            "open_price": None,
            "milestone_price": None,
            "message": "Could not reach GoldAPI."
        }

    price = data["price"]
    open_price = data["open_price"]
    delta = round(price - open_price, 2)

    milestone_price = get_current_milestone(price, interval=30)
    state = load_state()
    last_milestone = state.get("last_milestone", 0)

    if milestone_price == last_milestone:
        direction = "neutral"
        return {
            "live_price": price,
            "open_price": open_price,
            "delta": delta,
            "milestone_price": milestone_price,
            "milestone_direction": direction,
            "message": f"No milestone change. Still at ${milestone_price}"
        }

    direction = "progress" if milestone_price > last_milestone else "delay"
    save_state(milestone_price, direction)

    df = pd.DataFrame(create_live_dataframe(price))
    df["Date"] = pd.to_datetime(df["Date"])

    milestone_log = simulate_milestones(df, step=30)
    contracts = generate_contracts(milestone_log)
    gaps = analyze_gaps(milestone_log)
    alerts = generate_alert_log(contracts)
    payments = generate_payment_batch(contracts)
    summary = summarize_project(milestone_log, contracts)

    contracts["Gap Context"] = [f"Live Snapshot - {direction}"]

    return {
        "milestones": milestone_log,
        "contracts": contracts,
        "gaps": gaps,
        "alerts": alerts,
        "payments": payments,
        "summary": summary,
        "live_price": price,
        "open_price": open_price,
        "delta": delta,
        "milestone_price": milestone_price,
        "milestone_direction": direction,
        "message": f"{'New milestone' if direction == 'progress' else 'Delay'} detected at ${milestone_price}"
    }
