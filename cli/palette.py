import traceback
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from ai.cortex.main import handle

HIST = Path("var/history.txt")
HIST.parent.mkdir(parents=True, exist_ok=True)
ERR = Path("var/error.log")


def main():
    session = PromptSession(message=lambda: "HelmOS> ", history=FileHistory(str(HIST)))
    print("HelmOS — Keyboard Palette (type 'help' or 'exit')")
    while True:
        try:
            text = session.prompt()
        except KeyboardInterrupt:
            print("^C")
            continue
        try:
            out = handle(text)
        except Exception:
            ERR.parent.mkdir(parents=True, exist_ok=True)
            with ERR.open("a") as fh:
                fh.write(traceback.format_exc())
            print("Error: see var/error.log")
            continue
        if out == "__EXIT__":
            print("Bye.")
            break
        if out:
            print(out)


if __name__ == "__main__":
    main()
