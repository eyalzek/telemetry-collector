from sqlalchemy import Column, DateTime, Integer, Float, String
from sqlalchemy.future import select

from database import Base, db


class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), index=True)
    cpu_usage = Column(Float, index=True)
    memory_usage = Column(Float, index=True)
    timestamp = Column(DateTime)

    @classmethod
    async def create(cls, **kwargs):
        request = cls(**kwargs)
        db.add(request)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return request

    @classmethod
    async def get_all(cls, skip: int = 0, limit: int = 100):
        query = select(cls)
        requests = await db.execute(query)
        requests = requests.offset(skip).limit(limit).all()
        return requests

    @classmethod
    async def get_all_by_device(
            cls,
            device_id: str,
            skip: int = 0,
            limit: int = 100):
        query = select(cls).where(cls.device_id == device_id)
        requests = await db.execute(query)
        requests = requests.offset(skip).limit(limit).all()
        return requests
