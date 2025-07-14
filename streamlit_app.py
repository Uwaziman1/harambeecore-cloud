import streamlit as st
import pandas as pd
from run_pipeline import run_pipeline

st.set_page_config(page_title="HarambeeCore Pilot Dashboard", layout="wide")

# Kenyan flag theme colors
PRIMARY = "#006600"   # Green
SECONDARY = "#FF0000" # Red
ACCENT = "#000000"     # Black
BG = "#FFFFFF"         # White

st.markdown(f"""
    <style>
        .block-container {{
            padding: 2rem;
            background-color: {BG};
        }}
        .title-text {{
            color: {PRIMARY};
            font-weight: 700;
        }}
        .caption-text {{
            color: {SECONDARY};
        }}
    </style>
""", unsafe_allow_html=True)

st.title("\U0001F4D8 HarambeeCore Pilot Dashboard")
st.caption("Audit-level transparency powered by immutable ledgers")

if st.button("\U0001F680 Run Simulation"):
    result = run_pipeline()
    if isinstance(result, dict) and result.get("milestones") is not None:
        tabs = st.tabs(["Summary", "Milestones", "Contracts", "Gaps", "Alerts", "Payments"])

        with tabs[0]:
            st.subheader("\U0001F4CB Project Summary")
            for k, v in result["summary"].items():
                st.markdown(f"**{k}:** {v}")

        with tabs[1]:
            st.subheader("🧱 Milestones")
            st.dataframe(result["milestones"])
            st.download_button("Download Milestones", result["milestones"].to_csv(index=False), file_name="milestones.csv")

        with tabs[2]:
            st.subheader("📜 Contract Validations")
            st.dataframe(result["contracts"])
            st.download_button("Download Contracts", result["contracts"].to_csv(index=False), file_name="contracts.csv")

        with tabs[3]:
            st.subheader("⚠️ Gap Analysis")
            st.dataframe(result["gaps"])
            st.download_button("Download Gaps", result["gaps"].to_csv(index=False), file_name="gap_analysis.csv")

        with tabs[4]:
            st.subheader("\U0001F514 Alert Log")
            st.dataframe(result["alerts"])
            st.download_button("Download Alerts", result["alerts"].to_csv(index=False), file_name="alerts.csv")

        with tabs[5]:
            st.subheader("\U0001F4B8 Payment Batch")
            st.dataframe(result["payments"])
            st.download_button("Download Payments", result["payments"].to_csv(index=False), file_name="payment_batch.csv")

        try:
            st.image("gap/milestone_plot.png", caption="Kilimani Bridge Construction Timeline (Gold-Pegged)")
        except Exception as e:
            st.warning(f"Chart unavailable: {e}")

    else:
        st.warning("Simulation did not return results. Check for errors in the pipeline.")
