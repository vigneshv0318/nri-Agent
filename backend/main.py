from fastapi import FastAPI
from api import auth, vision, voice, culture
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
import database
database.init_db()

app = FastAPI(title="Ammachi Backend")

# Allow CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, tags=["Auth"])
app.include_router(vision.router, prefix="/vision", tags=["Vision"])
app.include_router(voice.router, prefix="/voice", tags=["Voice"])
app.include_router(culture.router, prefix="/culture", tags=["Culture"])

@app.get("/")
def read_root():
    return {"message": "Ammachi API is running!"}
