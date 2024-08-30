from pydantic import BaseModel

from .attribute import AttributeDto

class IdDto(BaseModel):
    id: int

class UsernameDto(BaseModel):
    username: str

class PasswordDto(BaseModel):
    password: str
    password_confirmation: str

class AccountCreate(UsernameDto, PasswordDto):
    attributes: list[AttributeDto]

class AccountRead(UsernameDto, IdDto):
    pass