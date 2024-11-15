from sqlalchemy import Column, String, Integer, DateTime

from app.db.models import Base


class RateLimit(Base):
    """
    Rate Limit Model
    """
    __tablename__ = "rate_limits"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(255), index=True)  # IP or user_id
    requests = Column(Integer, default=0)
    timestamp = Column(DateTime)
