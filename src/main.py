from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import ValidationError

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/telemetry', response_model=schemas.Request)
def telemetry_request(request: schemas.Request, db: Session = Depends(get_db)):
    try:
        return crud.create_request(db=db, request=request)
    except ValidationError as e:
        print(e)


@app.get('/requests', response_model=list[schemas.Request])
def read_requests(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)):
    requests = crud.get_requests(db=db, skip=skip, limit=limit)
    return requests


@app.get('/requests/{device_id}', response_model=list[schemas.Request])
def read_requests_by_device(
        device_id: str,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)):
    device_requests = crud.get_requests_by_device(
        db=db, device_id=device_id, skip=skip, limit=limit)
    if device_requests is None:
        raise HTTPException(status_code=404, detail='Device not found')
    return device_requests
