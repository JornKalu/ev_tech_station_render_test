from fastapi import APIRouter, Request, Depends, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from database.schema import ErrorResponse, OpenSlotModel, OpenSlotResponseModel, ManageStationSlotModel, ManageSlotStatusModel, StationModel, SyncStationModel, SyncStationSlotModel, SyncStationResponseMode
from fastapi.encoders import jsonable_encoder
from modules.station.stat import process_station_request, get_single_station_info, sync_station_info, open_station_slot_for_charging, open_station_slot_for_charging_by_code, manage_station_slots, manage_station_slots_by_code, manage_slot_status, get_single_station_info_by_code, sync_station_info_by_code
import json

router = APIRouter(
    prefix="/station",
    tags=["v1_station"]
)

@router.get("/by_id/{station_id}", response_model=StationModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_id(db: Session = Depends(get_db), station_id: int = 0):
    return get_single_station_info(db=db, station_id=station_id)

@router.get("/by_code/{code}", response_model=StationModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_id(db: Session = Depends(get_db), code: str = None):
    return get_single_station_info_by_code(db=db, code=code)

@router.post("/open_slot", response_model=OpenSlotResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def open_slot(fields: OpenSlotModel, db: Session = Depends(get_db)):
    req = open_station_slot_for_charging_by_code(db=db, station_code=fields.station_code, mobility_device_id=fields.mobility_device_id, slot_number=fields.slot_number)
    return req

@router.post("/slot", response_model=OpenSlotResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def slot(fields: ManageStationSlotModel, db: Session = Depends(get_db)):
    slots = json.loads(fields.slots)
    req = manage_station_slots_by_code(db=db, station_code=fields.station_code, mobility_device_id=fields.mobility_device_id, slots=slots)
    return req

@router.post("/slot/update", response_model=OpenSlotResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def slot_update(fields: ManageSlotStatusModel, db: Session = Depends(get_db)):
    req = manage_slot_status(db=db, station_id=fields.station_id, slot_number=fields.slot_number, status=fields.status)
    return req

@router.post("/process")
async def process(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    return process_station_request(db=db, data=body)

@router.post("/sync")
async def sync(fields: SyncStationModel, db: Session = Depends(get_db)):
    slots = json.loads(fields.slots)
    original_values = json.dumps(jsonable_encoder(fields))
    req = sync_station_info_by_code(db=db, initial_instruction=fields.initial_instruction, station_code=fields.code, latitude=fields.latitude, longitude=fields.longitude, status=fields.status, slots=slots, original_values=original_values)
    return req