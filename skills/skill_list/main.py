from core.skill_api import endpoint, registry


@endpoint("skills.list")
def list_skills():
    """Return a sorted list of registered skill endpoints."""
    return registry.list_endpoints()
