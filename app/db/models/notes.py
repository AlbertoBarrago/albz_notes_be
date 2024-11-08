"""
Notes model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class Note(Base):
    """
    Note Class
    """
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="notes")

    def __repr__(self):
        return f"<Note {self.title}>"
