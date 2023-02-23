from datetime import timezone
from sqlalchemy import Column, DateTime, Integer, Float, String, TypeDecorator
from sqlalchemy.future import select

from database import Base, db


# store timestamp as a TZ naive UTC datetime
class TZDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo:
                raise TypeError('tzinfo is required')
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.replace(tzinfo=timezone.utc)
        return value


class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), index=True)
    cpu_usage = Column(Float, index=True)
    memory_usage = Column(Float, index=True)
    timestamp = Column(TZDateTime)

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
        query = select(cls).offset(skip).limit(limit)
        requests = await db.execute(query)
        requests = requests.scalars().all()
        return requests

    @classmethod
    async def get_all_by_device(
            cls,
            device_id: str,
            skip: int = 0,
            limit: int = 100):
        query = select(cls).where(cls.device_id == device_id).offset(skip).limit(limit)
        requests = await db.execute(query)
        requests = requests.scalars().all()
        return requests
