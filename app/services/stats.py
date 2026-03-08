import time

import psutil

from app.schemas.stats import NetworkIO, ServerStats


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
    )
