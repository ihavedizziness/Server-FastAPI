from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routers import download, internet, stats, upload

BASE_DIR = Path(__file__).parent.parent  # project root
STATIC_DIR = BASE_DIR / "static"


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description=(
            "Measure download speed from the server, upload speed to the server, "
            "and the server's own internet connection speed."
        ),
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(download.router)
    app.include_router(upload.router)
    app.include_router(internet.router)
    app.include_router(stats.router)

    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def index() -> str:
        return (STATIC_DIR / "index.html").read_text(encoding="utf-8")

    return app


app = create_app()
