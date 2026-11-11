from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreate(BaseModel):
    name : str
    email : EmailStr
    password : str = Field(min_length=8)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id : int
    name : str
    email : EmailStr

class LoginRequest(BaseModel):
    email : EmailStr
    password : str

class TokenResponse(BaseModel):
    access_token : str
    token_type : str = "bearer"