from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from run_pipeline import run_pipeline

app = FastAPI()

@app.get("/")
def root():
    return {"message": "HarambeeCore backend is running."}

@app.get("/simulate")
def simulate(request: Request):
    mode = request.query_params.get("mode", "historical")  # default to 'historical'
    result = run_pipeline(mode)

    if not result:
        return {"error": "Simulation failed or no data returned."}

    response = {
        "summary": result.get("summary", {}),
        "milestones": result.get("milestones", []),
        "contracts": result.get("contracts", []),
        "gaps": result.get("gaps", []),
        "alerts": result.get("alerts", []),
        "payments": result.get("payments", [])
    }

    # Add live metadata if present
    for key in ["live_price", "open_price", "delta", "milestone_price", "milestone_direction", "message", "error"]:
        if key in result:
            response[key] = result[key]

    return JSONResponse(content=response)
