from sqlalchemy import Column, DateTime, Integer, Float, String
from sqlalchemy.orm import relationship

from database import Base


class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), index=True)
    cpu_usage = Column(Float, index=True)
    memory_usage = Column(Float, index=True)
    timestamp = Column(DateTime)
