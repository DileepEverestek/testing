from typing import Optional
from pydantic import BaseModel,EmailStr


#properties required during user creation
class create_new_user(BaseModel):
    username: str
    email : EmailStr
    hashed_password : str
    user_role: str


class user_login(BaseModel):
    email : str
    hashed_password : str


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token : str

class Refresh_Token(BaseModel):
    refresh_token1: str
    token_type: str
    access_token: str

class Del_Token(BaseModel):
    token_response : str
