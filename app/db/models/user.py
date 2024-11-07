from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from sqlalchemy.orm import relationship

from app.db.models import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    notes = relationship("Note", back_populates="user")

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)

    def set_password(self, plain_password: str):
        self.hashed_password = pwd_context.hash(plain_password)
