from .router import router


# FIXME check if there some other way to do that without this
def get_path_for(name: str, **kwargs) -> str:
    return router.url_path_for(name, **kwargs)
