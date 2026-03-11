from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import get_settings
from app.routers import download, internet, stats, upload

BASE_DIR = Path(__file__).parent.parent  # project root
STATIC_DIR = BASE_DIR / "static"


TAGS_METADATA = [
    {
        "name": "Download",
        "description": (
            "Stream random bytes **from the server** to the client. "
            "The client measures how fast it receives the data."
        ),
    },
    {
        "name": "Upload",
        "description": (
            "Send binary data **to the server**. "
            "The server measures elapsed time and returns the upload speed in Mbps."
        ),
    },
    {
        "name": "Internet Speed",
        "description": (
            "Run a full **speedtest-cli** test on the server itself. "
            "Returns the server's own ping, download speed, upload speed, and ISP info. "
            "Takes approximately 30 seconds."
        ),
    },
    {
        "name": "Stats",
        "description": (
            "Live server resource metrics: CPU, RAM, disk, network I/O, uptime, "
            "process count, and GPU utilization/VRAM. Refreshes on every request."
        ),
    },
]


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description=(
            "## Stats Server\n\n"
            "A self-hosted server for measuring network performance:\n\n"
            "- **Download** — how fast clients can pull data from this server\n"
            "- **Upload** — how fast clients can push data to this server\n"
            "- **Internet Speed** — the server's own connection to the internet\n"
            "- **Stats** — live CPU, RAM, disk, network, and GPU metrics\n\n"
            "Interactive docs are available here. "
            "The web UI is served at [`/`](/)."
        ),
        version="1.0.0",
        openapi_tags=TAGS_METADATA,
        docs_url="/docs",
        redoc_url="/redoc",
        contact={
            "name": "Stats Server",
            "url": "https://github.com/ihavedizziness/Server-FastAPI",
        },
        license_info={
            "name": "MIT",
        },
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

    Instrumentator().instrument(app).expose(app, include_in_schema=False)

    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def index() -> str:
        return (STATIC_DIR / "index.html").read_text(encoding="utf-8")

    return app


app = create_app()
