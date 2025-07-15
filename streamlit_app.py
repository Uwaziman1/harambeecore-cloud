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

        with tabs[1]:
            st.header("Summary")
            summary = result["summary"]
            col1, col2 = st.columns(2)
            for i, (k, v) in enumerate(summary.items()):
                (col1 if i % 2 == 0 else col2).metric(label=k, value=str(v))
            buffer = generate_pdf(result["summary"], result["contracts"])
            st.download_button("Download PDF Report", data=buffer.getvalue(), file_name="harambeecore_report.pdf", mime="application/pdf")

        with tabs[2]:
            st.header("Milestones")
            df = result["milestones"]
            st.dataframe(df, use_container_width=True)
            start_date, end_date = st.date_input("Filter by Date Range", [df["Date"].min(), df["Date"].max()])
            filtered_df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]
            st.line_chart(filtered_df.set_index("Date")["Price"], use_container_width=True)

        with tabs[3]:
            st.header("Contracts")
            contracts = result["contracts"]
            st.dataframe(contracts, use_container_width=True)
            st.bar_chart(contracts.set_index("Milestone")["Price"], use_container_width=True)

        with tabs[4]:
            st.header("Gaps")
            gaps = result["gaps"]
            st.dataframe(gaps, use_container_width=True)
            if not gaps.empty:
                st.line_chart(gaps.set_index("Date")["Gap"], use_container_width=True)

        with tabs[5]:
    st.header("Alerts")
    alerts = result["alerts"]
    st.dataframe(alerts, use_container_width=True)
    if not alerts.empty and "Date" in alerts.columns and "Alert" in alerts.columns:
        st.bar_chart(alerts.set_index("Date")["Alert"].astype(str).value_counts())

        with tabs[6]:
    st.header("Payments")
    payments = result["payments"]
    st.dataframe(payments, use_container_width=True)
    if not payments.empty and "Date" in payments.columns and "Amount" in payments.columns:
        st.line_chart(payments.set_index("Date")["Amount"])

        with tabs[7]:
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

        with tabs[8]:
            st.header("Contact")
            st.markdown("""
**Email:** mbuguawian@gmail.com  
**Sponsor:** [GitHub Sponsors](https://github.com/sponsors/uwaziman1)  
**Foundation:** HarambeeCore™ RZ77191
""")
    else:
        st.warning("Simulation did not return results. Check for errors in the pipeline.")
