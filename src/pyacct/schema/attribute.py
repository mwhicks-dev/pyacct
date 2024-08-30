from pydantic import BaseModel

class AttributeDto(BaseModel):
    key: str
    value: str | None