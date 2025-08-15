import os
import platform
import shutil
import subprocess
import sys

from core.skill_api import endpoint


def _read_meminfo():
    info = {}
    try:
        with open("/proc/meminfo") as fh:
            for line in fh:
                key, val = line.split(":", 1)
                info[key] = val.strip()
    except FileNotFoundError:
        pass
    return info


def _read_uptime():
    try:
        with open("/proc/uptime") as fh:
            up = float(fh.read().split()[0])
            return int(up)
    except Exception:
        return 0


@endpoint("system.info.get")
def get():
    mem = _read_meminfo()
    uptime = _read_uptime()
    gpus = []
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            text=True,
        )
        for line in out.strip().splitlines():
            name, memory = [s.strip() for s in line.split(",", 1)]
            gpus.append({"name": name, "memory_total": memory})
    except Exception:
        pass
    disk = shutil.disk_usage("/")
    return {
        "os": platform.platform(),
        "python": sys.version.split()[0],
        "cpu_count": os.cpu_count(),
        "ram_total": mem.get("MemTotal"),
        "ram_available": mem.get("MemAvailable"),
        "disk_total": disk.total,
        "disk_free": disk.free,
        "uptime_seconds": uptime,
        "gpus": gpus,
    }
