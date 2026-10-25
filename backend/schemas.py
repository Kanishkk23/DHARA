from datetime import datetime

from pydantic import BaseModel, Field


class LocationInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class EnvironmentalInput(BaseModel):
    rainfall_mm: float = Field(..., ge=0)
    rainfall_24h_mm: float = Field(..., ge=0)
    river_level_m: float = Field(..., ge=0)
    river_level_change_m: float = Field(...)
    temperature_c: float = Field(...)
    humidity_percent: float = Field(..., ge=0, le=100)


class FloodRiskRequest(BaseModel):
    location: LocationInput
    environmental: EnvironmentalInput


class FloodRiskResponse(BaseModel):
    location: str
    latitude: float
    longitude: float

    risk_score: float = Field(..., ge=0, le=100)
    risk_level: str

    rainfall_24h_mm: float
    river_level_m: float
    river_level_change_m: float

    prediction_probability: float = Field(..., ge=0, le=1)

    recommendation: str
    model_inference_ms: float = 3.2
    class_probabilities: dict = Field(default_factory=dict)
    xai_top_factors: list = Field(default_factory=list)
    multi_horizon: dict = Field(default_factory=dict)
    cascading_failures: list = Field(default_factory=list)
    ensemble_architecture: str = "Stacking Blended Ensemble (Random Forest + Gradient Boosting)"

    generated_at: datetime