from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    user_id: str
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    created_at: datetime

    model_config = {"env_file": ".env"}