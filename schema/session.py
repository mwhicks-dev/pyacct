import uuid
from typing import Annotated

from pydantic import BaseModel, UUID4, AfterValidator

class SessionDto(BaseModel):
    # ref: https://github.com/pydantic/pydantic/discussions/7023
    id = UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))]

class SessionCreate(BaseModel):
    username: str
    password: str
