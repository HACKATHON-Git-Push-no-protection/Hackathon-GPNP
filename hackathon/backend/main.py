from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import joblib

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
    # model = joblib.load("model.pkl") 

@router.get("/") 
async def root():
    return {"message": "API is running"}


@router.post("/predict")
async def predict(data):
    return {"prediction"}

app.include_router(router)