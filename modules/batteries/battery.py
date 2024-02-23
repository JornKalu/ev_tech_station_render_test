from typing import Any
from database.model import update_battery, get_batteries_by_station_id
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate


def retrieve_batteries_by_station(db: Session, station_id: int=0):
    data = get_batteries_by_station_id(db=db, station_id=station_id)
    return paginate(data)

