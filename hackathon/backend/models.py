from pydantic import BaseModel
from typing import Literal

class PredictionRequest(BaseModel):
    timestamp: str  # or datetime
    gender: Literal["Male","Female","Other"]
    age: int
    height_cm: float
    weight_kg: float
    hydration_level: Literal[
        "Poor (rarely drink water)",
        "Moderate (1–2 liters/day)",
        "Good (2–3 liters/day)",
        "Excellent (3+ liters/day)"
    ]
    activity_level: Literal[
        "Low (mostly sedentary)",
        "Moderate (light exercise a few days a week)",
        "High (exercise 5+ days a week or physical job)"
    ]
    meds_affecting_gut: bool  # map Yes/No
    fiber_grams: float
    fat_grams: float
    spiciness: Literal["Not spicy","Mild","Medium","Hot","Extremely spicy"]
    weekly_greasy_meals: int
    dairy_freq: Literal["Yes","No","Occasionally"]
    processed_servings: int
    fv_servings: int
    toilet_method: Literal[
        "1-ply paper","2-ply paper","3-ply paper","Wet wipes","Bidet/water","Other"
    ]
    stool_consistency: Literal[
        "Hard and lumpy","Firm and smooth","Soft","Sticky or mushy","Watery"
    ]
    stool_color: Literal[
        "Brown","Yellow","Green","Black","Red or bloody","Other"
    ]
    smell_intensity: int  # e.g. 1–5 scale
    weekly_bms: int
    sheets_per_bm: int
