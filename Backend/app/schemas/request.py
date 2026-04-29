from pydantic import BaseModel

class InterventionRequest(BaseModel):
    treatment_value: int  # 0 or 1
    sample_size: int = 1000

class PredictionResponse(BaseModel):
    causal_estimate: float
    method_used: str
    confidence_interval: list[float]