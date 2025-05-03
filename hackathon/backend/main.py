from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import pickle

app = FastAPI()
router = APIRouter(prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.on_event("startup")
def load_model():
    global model
    model = pickle.load(open("estimator.pkl", "wb"))


@router.get("/")
async def root():
    return {"message": "API is running"}


all_features = [
    "age",
    "smell_intensity",
    "sleep_hours",
    "timestamp",
    "gender",
    "height_cm",
    "weight_kg",
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


@router.post("/predict", response_model=dict)
async def predict(req):

    answers = req.answers
    feature_vector = []
    for feat in all_features:
        val = answers.get(feat, 0)
        try:
            val = float(val)
        except:
            pass
        feature_vector.append(val)

    pred = model.predict([feature_vector])
    return {"prediction ": pred.tolist()}


app.include_router(router)
