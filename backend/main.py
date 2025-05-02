# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from fastapi import FastAPI
from api.diary import router as diary_router
from db.database import engine
from db.base import Base

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(diary_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


#mqtt_client.start()




