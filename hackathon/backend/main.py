import os
from pathlib import Path
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pickle
import pandas as pd
from pydantic import BaseModel
from setup import (
    filter_columns,
    clean_short_open_numerical_cols,
    clean_data,
    create_pipeline,
    CreateYPipeline,
    FeatureCombination,
    FeatureManager,
    ModelManager,
    HyperOptCombination,
    HyperOptManager,
    HyperOptResultDict,
    TrialParamWrapper,
    calculate_metric,
    EarlyStoppingCallback,
    get_existing_trials_info,
    save_hyper_result,
    optimize_model_and_save,
    create_objective,
    engineer_combinations_wrapper,
    hyperopt,
    load_hyper_opt_results,
    setup_analysis,
    save_singular_best,
)
import cloudpickle

app = FastAPI()
router = APIRouter(prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],  # Allow frontend to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.on_event("startup")
def load_model():
    global model
    try:
        model = cloudpickle.load(
            open(Path(os.getcwd()) / "estimator_cloudpickle.pkl", "rb")
        )
        print("Model loaded successfully with cloudpickle")
    except Exception as e:
        print("Failed to load model with cloudpickle", e)

    try:
        model = joblib.load(Path(os.getcwd()) / "estimator_joblib.pkl")
        print("Model loaded successfully with joblib")

    except Exception as e:
        print("Failed to load model with joblib", e)

    try:
        model = pickle.load(open(Path(os.getcwd()) / "estimator_pickle.pkl", "rb"))
        print("Model loaded successfully with pickle")
    except Exception as e:
        print("Failed to load model with pickle", e)


@router.get("/")
async def root():
    return {"message": "API is running"}


all_features = [
    "age",
    "smell_intensity",
    "sleep_hours",
    "timestamp",
    "gender",
    "height",
    "weight",
    "hydration_level",
    "activity_level",
    "meds_affecting_gut",
    "fiber_grams",
    "fat_grams",
    "spiciness",
    "weekly_greasy_meals",
    "dairy_freq",
    "processed_servings",
    "fv_servings",
    "toilet_method",
    "stool_consistency",
    "stool_color",
    "weekly_bms",
    "caffeinated_beverages_per_day",
]


class User(BaseModel):
    name: str
    age: int


class PredictionRequest(BaseModel):
    answers: dict
    # age: int
    # smell_intensity: int
    # sleep_hours: int
    # gender: str
    # height: int
    # weight: int
    # hydration_level: int
    # activity_level
    # meds_affecting_gut
    # fiber_grams
    # fat_grams
    # spiciness
    # weekly_greasy_meals
    # dairy_freq
    # processed_servings
    # fv_servings
    # toilet_method
    # stool_consistency
    # stool_color
    # weekly_bms
    # caffeinated_beverages_per_day


@app.post("/api/v1/user")
async def user(user: User):
    return {"message": f"Received user {user.name} aged {user.age}"}


@router.post("/predict")
async def predict(req: PredictionRequest):
    print("Received request:", req)
    df = pd.DataFrame([req.answers])

    pred = model.predict(df)
    return {"message": f"Received request {req}", "result": int(pred.tolist()[0])}


app.include_router(router)
