"""
AuditLog Model
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class AuditLog(Base):
    """
    AuditLog
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    action = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)

    user = relationship("User", back_populates="audit_logs")
