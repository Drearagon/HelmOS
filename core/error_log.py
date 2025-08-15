from datetime import datetime
from pathlib import Path
import traceback
from typing import Union

LOG_PATH = Path("var/error.log")


def log(err: Union[Exception, str]) -> None:
    """Append an error message or exception traceback to the log."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a") as f:
        if isinstance(err, Exception):
            tb = "".join(traceback.format_exception(type(err), err, err.__traceback__))
            f.write(f"[{now}] {tb}\n")
        else:
            f.write(f"[{now}] {err}\n")
