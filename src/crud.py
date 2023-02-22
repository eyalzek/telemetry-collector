from sqlalchemy.orm import Session

import models
import schemas


def get_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Request).offset(skip).limit(limit).all()


def get_requests_by_device(
        db: Session,
        device_id: str,
        skip: int = 0,
        limit: int = 100):
    return db.query(models.Request).filter(
        models.Request.device_id == device_id).offset(
        skip).limit(limit).all()


def create_request(db: Session, request: schemas.Request):
    req = models.Request(**request.dict())
    db.add(req)
    db.commit()
    db.refresh(req)
    return req
