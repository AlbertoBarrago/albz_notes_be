from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str  # This will be used during registration

class UserOut(UserBase):
    user_id: int
    created_at: datetime

    model_config = {"env_file": ".env"}