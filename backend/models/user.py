from pydantic import BaseModel, EmailStr, Field, BeforeValidator
from typing import Optional, Annotated
from datetime import datetime

# Helper for Mongo ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
