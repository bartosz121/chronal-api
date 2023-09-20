import humps
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=humps.camelize)


class Message(BaseModel):
    msg: str
