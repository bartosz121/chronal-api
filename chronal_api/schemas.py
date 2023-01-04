import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    """
    orjson.dumps() returns bytes; decode to match standard json.dumps()
    """
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ResourceUrl(ORJSONModel):
    resource_url: str


class ExceptionModel(ORJSONModel):
    detail: str
