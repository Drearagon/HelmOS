from pathlib import Path
from typing import List

import yaml

POLICY_PATH = Path("configs/policies/default.yaml")


class Policy:
    def __init__(self, data: dict):
        self.allowed_paths: List[str] = data.get("allowed_paths", [])
        self.denied_paths: List[str] = data.get("denied_paths", [])
        self.allowed_commands: List[str] = data.get("allowed_commands", [])
        self.denied_commands: List[str] = data.get("denied_commands", [])
        self.require_approval: bool = data.get("require_approval", False)
        self.prompt_on_write: bool = data.get("prompt_on_write", False)


def load_policy() -> Policy:
    data = yaml.safe_load(POLICY_PATH.read_text())
    return Policy(data)
