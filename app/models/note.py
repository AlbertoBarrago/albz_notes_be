from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Note {self.title}>"
