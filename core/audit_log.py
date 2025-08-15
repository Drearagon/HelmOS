from datetime import datetime
from pathlib import Path

LOG_PATH = Path("var/audit.log")
MAX_SIZE = 5 * 1024 * 1024  # 5MB


def _rotate_if_needed():
    if LOG_PATH.exists() and LOG_PATH.stat().st_size > MAX_SIZE:
        for i in range(4, 0, -1):
            src = LOG_PATH.with_suffix(f".log.{i}")
            dst = LOG_PATH.with_suffix(f".log.{i+1}")
            if src.exists():
                dst.write_bytes(src.read_bytes())
        LOG_PATH.with_suffix(".log.1").write_bytes(LOG_PATH.read_bytes())
        LOG_PATH.unlink(missing_ok=True)


def log(actor: str, action: str, reason: str = ""):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _rotate_if_needed()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {actor}: {action}"
    if reason:
        line += f" | reason: {reason}"
    line += "\n"
    with LOG_PATH.open("a") as f:
        f.write(line)
