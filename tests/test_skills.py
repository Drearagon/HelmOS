import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.skill_api import autoload_skills, registry


def test_system_info():
    autoload_skills(Path(__file__).resolve().parents[1])
    res = registry.call("system.info.get")
    assert res.ok


def test_skill_list():
    autoload_skills(Path(__file__).resolve().parents[1])
    res = registry.call("skills.list")
    assert res.ok
    assert "system.info.get" in res.data
