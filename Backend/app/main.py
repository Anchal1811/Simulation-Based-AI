from fastapi import FastAPI
from app.simulator.engine import generate_data

app = FastAPI(title="Causal AI API")

@app.get("/")
def read_root():
    return {"status": "Active", "message": "Backend is running!"}

@app.get("/test-data")
def test_data():
    # This just tests if the simulator works
    df = generate_data(n=5)
    return df.to_dict(orient="records")