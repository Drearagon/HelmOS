from datetime import datetime
from pathlib import Path

LOG_PATH = Path("var/audit.log")
MAX_BYTES = 5 * 1024 * 1024
BACKUPS = 2


def _rotate():
    if LOG_PATH.exists() and LOG_PATH.stat().st_size > MAX_BYTES:
        for i in range(BACKUPS, 0, -1):
            src = LOG_PATH.with_suffix(f".log.{i}")
            dst = LOG_PATH.with_suffix(f".log.{i + 1}")
            if src.exists():
                if i == BACKUPS and dst.exists():
                    dst.unlink()
                src.rename(dst)
        LOG_PATH.rename(LOG_PATH.with_suffix(".log.1"))


def log(actor: str, action: str, reason: str = ""):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _rotate()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {actor}: {action}"
    if reason:
        line += f" | reason: {reason}"
    line += "\n"
    with LOG_PATH.open("a") as fh:
        fh.write(line)
