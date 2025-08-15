import importlib
import pkgutil
from typing import Any, Callable, Dict, Optional

from pydantic import BaseModel


class Result(BaseModel):
    ok: bool = True
    data: Any = None
    error: Optional[str] = None


class SkillRegistry:
    def __init__(self) -> None:
        self._endpoints: Dict[str, Callable] = {}

    def register(self, fqid: str, fn: Callable) -> None:
        self._endpoints[fqid] = fn

    def call(self, fqid: str, **kwargs) -> Result:
        fn = self._endpoints.get(fqid)
        if not fn:
            return Result(ok=False, error=f"Unknown skill endpoint: {fqid}")
        try:
            return Result(ok=True, data=fn(**kwargs))
        except Exception as e:
            return Result(ok=False, error=str(e))

    def list_endpoints(self):
        return sorted(self._endpoints.keys())


registry = SkillRegistry()


def endpoint(fqid: str):
    def deco(fn):
        registry.register(fqid, fn)
        return fn

    return deco


def autoload_skills(root):
    pkg = "skills"
    for _, name, _ in pkgutil.iter_modules([str(root / pkg)]):
        importlib.import_module(f"{pkg}.{name}.main")
    return registry
