from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr = Field(examples=["admin@example.com"])
    password: str = Field(min_length=6, examples=["secret123"])


class UserRead(BaseModel):
    id: int
    email: EmailStr

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr = Field(examples=["admin@example.com"])
    password: str = Field(examples=["secret123"])
