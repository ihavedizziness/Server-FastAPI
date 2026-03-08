from fastapi import APIRouter

from app.schemas.stats import ServerStats
from app.services.stats import get_server_stats

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get(
    "",
    response_model=ServerStats,
    summary="Server resource stats",
    description="Returns live CPU, RAM, disk, network I/O, uptime, and load average.",
)
def server_stats() -> ServerStats:
    return get_server_stats()
