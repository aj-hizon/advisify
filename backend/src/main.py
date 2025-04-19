import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.routers.recommend import recommend_router

load_dotenv()

HOST = os.getenv("HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", 5000))

version = "v1"

app = FastAPI(
    title="Advisify",
    description="A RESTful API for student-class enrollment",
    version=version,
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend_router)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=BACKEND_PORT)
