from pydantic import BaseModel, Field


class NetworkIO(BaseModel):
    bytes_sent: int
    bytes_recv: int
    mb_sent: float
    mb_recv: float


class ServerStats(BaseModel):
    cpu_percent: float = Field(..., description="CPU usage %")
    cpu_count: int = Field(..., description="Number of logical CPU cores")
    load_avg_1: float = Field(..., description="Load average 1 min")
    load_avg_5: float = Field(..., description="Load average 5 min")
    load_avg_15: float = Field(..., description="Load average 15 min")

    ram_total_mb: float
    ram_used_mb: float
    ram_available_mb: float
    ram_percent: float

    disk_total_gb: float
    disk_used_gb: float
    disk_free_gb: float
    disk_percent: float

    net: NetworkIO

    uptime_seconds: int
    process_count: int
