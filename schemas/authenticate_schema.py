from pydantic import BaseModel


class AuthenticateCreate(BaseModel):
    username: str
    password: str


class AuthenticateRead(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
