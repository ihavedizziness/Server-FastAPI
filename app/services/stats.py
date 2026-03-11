import time

import psutil

from app.schemas.stats import GPUInfo, NetworkIO, ServerStats

try:
    import GPUtil as _gputil
except Exception:
    _gputil = None


def _get_gpu_info() -> list[GPUInfo]:
    if _gputil is None:
        return []
    try:
        gpus = _gputil.getGPUs()
    except Exception:
        return []
    result = []
    for gpu in gpus:
        mem_total = gpu.memoryTotal or 0
        mem_used = gpu.memoryUsed or 0
        mem_pct = round((mem_used / mem_total * 100), 1) if mem_total else 0.0
        result.append(GPUInfo(
            index=gpu.id,
            name=gpu.name,
            load_percent=round((gpu.load or 0) * 100, 1),
            memory_used_mb=round(mem_used, 1),
            memory_total_mb=round(mem_total, 1),
            memory_percent=mem_pct,
            temperature_c=round(gpu.temperature or 0, 1),
        ))
    return result


def get_server_stats() -> ServerStats:
    cpu = psutil.cpu_percent(interval=0.3)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()
    load = psutil.getloadavg()
    uptime = int(time.time() - psutil.boot_time())

    return ServerStats(
        cpu_percent=cpu,
        cpu_count=psutil.cpu_count(logical=True),
        load_avg_1=round(load[0], 2),
        load_avg_5=round(load[1], 2),
        load_avg_15=round(load[2], 2),
        ram_total_mb=round(ram.total / 1024 ** 2, 1),
        ram_used_mb=round(ram.used / 1024 ** 2, 1),
        ram_available_mb=round(ram.available / 1024 ** 2, 1),
        ram_percent=ram.percent,
        disk_total_gb=round(disk.total / 1024 ** 3, 1),
        disk_used_gb=round(disk.used / 1024 ** 3, 1),
        disk_free_gb=round(disk.free / 1024 ** 3, 1),
        disk_percent=disk.percent,
        net=NetworkIO(
            bytes_sent=net.bytes_sent,
            bytes_recv=net.bytes_recv,
            mb_sent=round(net.bytes_sent / 1024 ** 2, 1),
            mb_recv=round(net.bytes_recv / 1024 ** 2, 1),
        ),
        uptime_seconds=uptime,
        process_count=len(psutil.pids()),
        gpus=_get_gpu_info(),
    )
