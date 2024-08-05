from pydantic import BaseModel

class IdDto(BaseModel):
    id: int

class UsernameDto(BaseModel):
    username: str

class PasswordDto(BaseModel):
    password: str
    password_confirmation: str

class AccountCreate(UsernameDto, PasswordDto):
    pass

class AccountRead(UsernameDto, IdDto):
    pass