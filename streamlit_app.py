import streamlit as st
import pandas as pd
from run_pipeline import run_pipeline

st.set_page_config(page_title="HarambeeCore Pilot Dashboard", layout="wide")

st.title("📘 HarambeeCore Pilot Dashboard")
st.caption("Audit-level transparency powered by immutable ledgers")

if st.button("Run Simulation"):
    contracts = run_pipeline()
    if not contracts.empty:
        st.subheader("🧱 Milestones")
        st.dataframe(contracts[["Date", "Price", "Milestone"]])

        st.subheader("📜 Contract Validations")
        contracts["Contract ID"] = [f"SC-{i+1:03d}" for i in range(len(contracts))]
        contracts["Triggered"] = True
        contracts["Amount"] = "To be released upon verification"
        contracts["Recipient"] = "Contractor ABC Ltd"
        contracts["Gap Context"] = ["None", "Pre-Crisis Boom + Commodities Rise", "", "", ""][:len(contracts)]

        st.dataframe(contracts[["Contract ID", "Milestone", "Triggered", "Date", "Amount", "Recipient", "Gap Context"]])

        try:
            st.image("gap/milestone_plot.png", caption="Kilimani Bridge Construction Timeline (Gold-Pegged)")
        except Exception as e:
            st.warning(f"Plot could not be loaded: {e}")
    else:
        st.error("Simulation failed. Check logs or data file.")

