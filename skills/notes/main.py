from core.skill_api import endpoint
from ai.hippocampus.memory import append_memory, read_memory
NOTES_PREFIX = "[note] "
@endpoint("notes.add")
def add(text: str):
    append_memory(NOTES_PREFIX + text); return "Added note."
@endpoint("notes.list")
def list_notes():
    data = read_memory()
    notes = [line for line in data.splitlines() if line.startswith(NOTES_PREFIX)]
    return "\n".join(notes) if notes else "(no notes)"
