from pydantic import BaseModel,EmailStr,validator


class UserCreate(BaseModel):
    first_name: str
    email: EmailStr
    password: str
    phone: str
    profile_picture_path:str
    @validator('first_name')
    def get_first_name(cls, first_name):
        return first_name.split()[0]