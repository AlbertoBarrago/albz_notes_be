from pydantic import BaseModel

class TokenRequest(BaseModel):
    grant_type: str
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
