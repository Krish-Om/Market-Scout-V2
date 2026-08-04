from fastapi import FastAPI
from app.routes import router as generation_router
from fastapi.middleware.cors import CORSMiddleware
from app.config import Config

app_desc = """
# TikTok Script Generation API
This API orchestrates a multi-step pipeline to generate TikTok scripts based on clothing descriptions and context notes. It leverages a Trend Spotter, Scriptwriter, and Guardrail QA Check to ensure high-quality script outputs.
"""
app = FastAPI(
    description=app_desc, title="TikTok Script Generation API", version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    Config.ORIGINS,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
