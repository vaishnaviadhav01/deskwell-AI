from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from database import get_settings, init_db, save_settings
from schemas import Settings

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Code before 'yield' runs when the server starts."""
    init_db()
    yield


app = FastAPI(
    title="DeskWell AI",
    description="Smart Posture & Wellness Coach: local backend API",
    version="0.1.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", include_in_schema=False)
def home():
    
    return FileResponse(BASE_DIR / "templates" / "index.html")


@app.get("/api/health")
def health_check():
    #Simple endpoint to confirm the backend is running."""
    return {"status": "ok", "app": "DeskWell AI"}


@app.get("/api/settings", response_model=Settings)
def read_settings():
    #Return the saved settings
    return get_settings()


@app.put("/api/settings", response_model=Settings)
def update_settings(new_settings: Settings):

    """Validate and save new settings, then return what was saved."""

    save_settings(
        new_settings.nickname,
        new_settings.daily_goal_breaks,
        new_settings.coaching_mode,
        new_settings.sitting_interval_minutes,
    )
    return get_settings()