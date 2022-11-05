from chronal_api.core.config import get_config

config = get_config()


def create_router_prefix(name: str) -> str:
    """
    Adds `name` to `config.API_PREFIX`
    """
    return config.API_PREFIX + name
