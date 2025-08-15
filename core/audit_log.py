from datetime import datetime
from pathlib import Path
LOG_PATH = Path("var/audit.log")
def log(actor: str, action: str, reason: str = ""):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {actor}: {action}"
    if reason: line += f" | reason: {reason}"
    line += "\n"
    LOG_PATH.write_text(LOG_PATH.read_text() + line if LOG_PATH.exists() else line)
