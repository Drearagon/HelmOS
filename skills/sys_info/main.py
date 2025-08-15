import platform
import shutil
import os

try:
    import psutil
except Exception:  # pragma: no cover - fallback if psutil missing
    psutil = None
from core.skill_api import endpoint


def _fmt_bytes(n):
    # human-readable
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024.0:
            return f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} PB"


@endpoint("sys.info.get")
def get():
    uname = platform.uname()
    total, used, free = shutil.disk_usage("/")
    mem = psutil.virtual_memory() if psutil else None
    gpu = os.environ.get("NVIDIA_VISIBLE_DEVICES") or (
        "detected" if shutil.which("nvidia-smi") else "none"
    )
    return (
        "System info:\n"
        f"- OS: {uname.system} {uname.release} ({uname.version})\n"
        f"- Kernel: {uname.release}\n"
        f"- CPU: {uname.processor or platform.machine()}\n"
        f"- RAM: {mem.total//(1024**3)} GB total, {mem.available//(1024**3)} GB free\n"
        if mem
        else "- RAM: (psutil not available)\n"
        f"- Disk: {_fmt_bytes(total)} total, {_fmt_bytes(free)} free\n"
        f"- Python: {platform.python_version()}\n"
        f"- GPU: {gpu}\n"
    )
