from pathlib import Path
import yaml
from typing import List
POLICY_PATH = Path("configs/policies/default.yaml")
class Policy:
    def __init__(self, data: dict):
        self.allowed_paths: List[str] = data.get("allowed_paths", [])
        self.denied_paths: List[str] = data.get("denied_paths", [])
        self.allowed_commands: List[str] = data.get("allowed_commands", [])
        self.require_approval: bool = data.get("require_approval", False)
def load_policy() -> Policy:
    data = yaml.safe_load(POLICY_PATH.read_text())
    return Policy(data)
