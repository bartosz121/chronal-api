from pydantic import BaseModel


class ResourceUrl(BaseModel):
    resource_url: str


class ExceptionModel(BaseModel):
    detail: str
