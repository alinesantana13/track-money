from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    name: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserProfileResponse(BaseModel):
    email: str
    name: str

    class Config:
        from_attributes = True
