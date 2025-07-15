from fastapi import FastAPI
from run_pipeline import run_pipeline

app = FastAPI()

@app.get("/")
def root():
    return {"message": "HarambeeCore backend is running."}

@app.get("/simulate")
def simulate():
    result = run_pipeline()

    if not result:
        return {"error": "Simulation failed or no data returned."}

    return {
        "summary": result.get("summary", {}),
        "milestones": result.get("milestones", []),
        "contracts": result.get("contracts", []),
        "gaps": result.get("gaps", []),
        "alerts": result.get("alerts", []),
        "payments": result.get("payments", [])
    }
