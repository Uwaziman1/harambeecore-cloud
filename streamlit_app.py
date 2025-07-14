import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai
import os
from run_pipeline import run_pipeline

st.set_page_config(page_title="HarambeeCore Pilot Dashboard", layout="wide")

PRIMARY = "#006600"   # Green
SECONDARY = "#FF0000" # Red
ACCENT = "#000000"     # Black

st.markdown(f"""
    <style>
        html, body, [class*="css"]  {{
            color: {ACCENT};
            background-color: #FFFFFF;
            font-family: 'Segoe UI', sans-serif;
        }}
        h1, h2, h3 {{
            color: {PRIMARY};
        }}
        .stTabs [role="tab"] {{
            font-weight: bold;
            font-size: 16px;
            color: {PRIMARY};
        }}
        .stDownloadButton button {{
            background-color: {PRIMARY};
            color: white;
        }}
    </style>
""", unsafe_allow_html=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("\U0001F4D8 HarambeeCore Pilot Dashboard")
st.caption("Audit-level transparency powered by immutable ledgers")

if st.button("\U0001F680 Run Simulation"):
    with st.spinner("Simulating bridge progress and contracts..."):
        result = run_pipeline()

    if isinstance(result, dict) and result.get("milestones") is not None:
        tabs = st.tabs(["Summary", "Milestones", "Contracts", "Gaps", "Alerts", "Payments", "GPT Explorer"])

        with tabs[0]:
            st.header("\U0001F4CB Project Summary")
            col1, col2 = st.columns(2)
            with col1:
                for k, v in list(result["summary"].items())[:3]:
                    st.metric(label=k, value=str(v))
            with col2:
                for k, v in list(result["summary"].items())[3:]:
                    st.metric(label=k, value=str(v))

        with tabs[1]:
            st.header("🧱 Milestones")
            milestone_df = result["milestones"]
            milestone_filter = st.multiselect("Filter by Milestone:", milestone_df["Milestone"].unique())
            if milestone_filter:
                milestone_df = milestone_df[milestone_df["Milestone"].isin(milestone_filter)]
            st.dataframe(milestone_df, use_container_width=True)
            st.download_button("Download Milestones", milestone_df.to_csv(index=False), file_name="milestones.csv")
            st.line_chart(milestone_df.set_index("Date")["Price"])

        with tabs[2]:
            st.header("📜 Contract Validations")
            contract_df = result["contracts"]
            contract_filter = st.multiselect("Filter by Gap Context:", contract_df["Gap Context"].unique())
            if contract_filter:
                contract_df = contract_df[contract_df["Gap Context"].isin(contract_filter)]
            st.dataframe(contract_df, use_container_width=True)
            st.download_button("Download Contracts", contract_df.to_csv(index=False), file_name="contracts.csv")
            st.bar_chart(contract_df["Price"])

        with tabs[3]:
            st.header("⚠️ Gap Analysis")
            gap_df = result["gaps"]
            min_gap, max_gap = float(gap_df["Gap"].min()), float(gap_df["Gap"].max())
            selected_range = st.slider("Filter Gap Range:", min_gap, max_gap, (min_gap, max_gap))
            gap_df = gap_df[(gap_df["Gap"] >= selected_range[0]) & (gap_df["Gap"] <= selected_range[1])]
            st.dataframe(gap_df, use_container_width=True)
            st.download_button("Download Gaps", gap_df.to_csv(index=False), file_name="gap_analysis.csv")
            st.line_chart(gap_df.set_index("Date")["Gap"])

        with tabs[4]:
            st.header("\U0001F514 Alert Log")
            st.dataframe(result["alerts"], use_container_width=True)
            st.download_button("Download Alerts", result["alerts"].to_csv(index=False), file_name="alerts.csv")

        with tabs[5]:
            st.header("\U0001F4B8 Payment Batch")
            payment_df = result["payments"]
            recipient_filter = st.selectbox("Filter by Recipient:", payment_df["Recipient"].unique())
            payment_df = payment_df[payment_df["Recipient"] == recipient_filter]
            st.dataframe(payment_df, use_container_width=True)
            st.download_button("Download Payments", payment_df.to_csv(index=False), file_name="payment_batch.csv")
            st.bar_chart(payment_df.set_index("Date")["Amount"])

        with tabs[6]:
            st.header("\U0001F916 GPT Explorer")
            st.info("Type any question about the dataset below.")
            prompt = st.text_area("Ask the GPT-powered analyst (e.g. What happened in 2008?)")
            if prompt and openai.api_key:
                with st.spinner("Generating response from GPT..."):
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a financial analyst simulating a gold-pegged contract monitoring system."},
                                {"role": "user", "content": prompt}
                            ]
                        )
                        answer = response["choices"][0]["message"]["content"]
                        st.success("Response:")
                        st.write(answer)
                    except Exception as e:
                        st.error(f"OpenAI API error: {e}")
            elif prompt:
                st.warning("Missing OpenAI API key. Please set OPENAI_API_KEY as a Streamlit secret.")

        try:
            st.image("gap/milestone_plot.png", caption="Kilimani Bridge Construction Timeline (Gold-Pegged)")
        except Exception as e:
            st.warning(f"Chart unavailable: {e}")

    else:
        st.warning("Simulation did not return results. Check for errors in the pipeline.")
