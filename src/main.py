from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

import models
import schemas
from database import db

db.init()

app = FastAPI()


@app.on_event('startup')
async def startup():
    await db.create_all()


@app.on_event('shutdown')
async def shutdown():
    await db.close()


@app.post('/telemetry', response_model=schemas.Request)
async def telemetry_request(request: schemas.Request):
    try:
        request = await models.Request.create(**request.dict())
        return request
    except ValidationError as e:
        print(e)


@app.get('/requests', response_model=list[schemas.Request])
async def read_requests(
        skip: int = 0,
        limit: int = 100):
    requests = await models.Request.get_all(skip=skip, limit=limit)
    return requests


@app.get('/requests/{device_id}', response_model=list[schemas.Request])
async def read_requests_by_device(
        device_id: str,
        skip: int = 0,
        limit: int = 100):
    device_requests = await models.Request.get_all_by_device(
        device_id=device_id, skip=skip, limit=limit)
    if device_requests is None:
        raise HTTPException(status_code=404, detail='Device not found')
    return device_requests
