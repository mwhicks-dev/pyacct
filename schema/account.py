from pydantic import BaseModel

class IdDto(BaseModel):
    id: int

class UsernameDto(BaseModel):
    username: str

class PasswordSet(BaseModel):
    password: str
    password_confirmation: str

class AccountCreate(UsernameDto, PasswordSet):
    pass

class AccountRead(UsernameDto, IdDto):
    pass