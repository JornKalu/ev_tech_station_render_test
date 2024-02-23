from fastapi import APIRouter, Request, Depends, HTTPException
from database.db import get_session
from database.schema import BatteryModel, ErrorResponse
from modules.batteries.battery import retrieve_batteries_by_station
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/battery",
    tags=["v1_bat"]
)

@router.get("/get_all/{station_id}", response_model=Page[BatteryModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, db: Session = Depends(get_session), station_id: int = 0):
    return retrieve_batteries_by_station(db=db, station_id=station_id)
