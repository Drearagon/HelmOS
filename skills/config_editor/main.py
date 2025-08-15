import yaml
from core.skill_api import endpoint
from core.policy_engine import POLICY_PATH

@endpoint("config.policy.get")
def get():
    return yaml.safe_load(POLICY_PATH.read_text())

@endpoint("config.policy.set")
def set_value(key: str, value: str):
    data = yaml.safe_load(POLICY_PATH.read_text())
    data[key] = yaml.safe_load(value)
    POLICY_PATH.write_text(yaml.safe_dump(data))
    return "Policy updated."
