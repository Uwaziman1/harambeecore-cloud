from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "HarambeeCore backend is running."}

@app.get("/simulate")
def simulate():
    return {
        "summary": {"Milestones": 10, "Contracts": 5},
        "milestones": [{"Milestone": "Test", "Price": 1000}],
        "contracts": [{"Milestone": "Test", "Price": 1000, "Gap Context": "Demo"}],
        "gaps": [],
        "alerts": [],
        "payments": []
    }

