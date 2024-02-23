from typing import Optional, List, Any
from pydantic import BaseModel

class OpenSlotModel(BaseModel):
    mobility_device_id: int
    # station_id: int
    station_code: str
    slot_number: int

    class Config:
        orm_mode = True

class OpenSlotResponseModel(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True

class ManageSlotModel(BaseModel):
    battery_id: Optional[int] = 0
    slot_number: Optional[int] = 0
    is_ejected: Optional[int] = 0
    is_returned: Optional[int] = 0

    class Config:
        orm_mode = True


class ManageStationSlotModel(BaseModel):
    mobility_device_id: int
    # station_id: int
    station_code: str
    # slots: List[ManageSlotModel]
    slots: Optional[str] = None

    class Config:
        orm_mode = True

class ManageSlotStatusModel(BaseModel):
    station_id: int
    slot_number: int
    status: Optional[int] = None

    class Config:
        orm_mode = True

class StationSlotModel(BaseModel):
    id: Optional[int] = None
    station_id: Optional[int] = None
    battery_id: Optional[int] = None
    battery_code: Optional[str] = None
    slot_number: Optional[int] = None
    status: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True

class SyncStationSlotModel(BaseModel):
    station_id: int
    slot_number: Optional[int] = None
    allow_charge: Optional[int] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True


class StationModel(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    image: Optional[str] = None
    autonomy_charge: Optional[str] = None
    autonomy_charge_time: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    status: Optional[int] = None
    created_at: Optional[str] = None
    slots: List[StationSlotModel] = None

    class Config:
        orm_mode = True

class SyncStationModel(BaseModel):
    # id: int
    code: str
    initial_instruction: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    slots: Optional[str] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True

class SyncSlotDataResponseModel(BaseModel):
    slot_number: int
    allow_charge: Optional[int] = None
    battery_docked: Optional[int] = None
    battery_eject: Optional[int] = None
    battery_stop_charge: Optional[int] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True

class SyncStationDataResponseModel(BaseModel):
    id: int
    status: int
    slots: Optional[List[SyncSlotDataResponseModel]] = None

    class Config:
        orm_mode = True

class SyncStationResponseMode(BaseModel):
    status: bool
    message: str
    data: Optional[SyncStationDataResponseModel] = None

    class Config:
        orm_mode = True