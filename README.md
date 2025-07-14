🚀 **A Streamlit-hosted simulation for milestone-driven smart contracts pegged to gold price (XAUUSD).**

## 🔧 Features
- Milestone simulation from historical gold data
- Contract generation + triggered alerts
- Gap analysis based on price volatility
- Streamlit UI for stakeholder transparency

## 📁 Structure
```bash
harambeecore-cloud/
├── core/                      # Simulation modules
├── gap/                      # Raw CSV data (upload or commit)
├── tests/                    # Unit tests
├── run_pipeline.py           # Main orchestrator
├── streamlit_app.py          # Frontend dashboard
├── requirements.txt          # Dependencies
├── README.md                 # This file
```

## 🧪 To Run Locally
```bash
git clone https://github.com/Uwaziman1/harambeecore-cloud.git
cd harambeecore-cloud
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 🧠 Next Steps
- Add `XAUUSD_historical.csv` to `gap/`
- Use `;` separator and include `Date`, `Close` columns
- Optional: Add CI tests and `.env` secret configs

---

**Author:** Uwaziman1  |  copyright ‘Harambeecore™ Bridge
Simulation System’ (RZ77191)

