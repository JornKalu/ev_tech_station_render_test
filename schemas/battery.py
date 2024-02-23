from typing import Optional
from pydantic import BaseModel

class BatteryModel(BaseModel):
    id: int
    type_id: int
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    qr_code: Optional[str] = None
    voltage: Optional[str] = None
    temperature: Optional[str] = None
    charge: Optional[str] = None
    humidity: Optional[str] = None
    electric_current: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    status: Optional[int] = 0
    customer_id: Optional[int] = None
    customer_full_name: Optional[str] = None
    customer_address: Optional[str] = None
    station_name: Optional[str] = None
    station_address: Optional[str] = None
    station_id: Optional[int] = None
    mobility_device_code: Optional[str] = None
    mobility_device_name: Optional[str] = None
    mobility_device_type: Optional[int] = None
    mobility_device_model: Optional[str] = None
    mobility_device_registration_number: Optional[str] = None
    mobility_device_vin: Optional[str] = None
    mobility_device_id: Optional[int] = None
    battery_type_name: Optional[str] = None
    battery_type_fee: Optional[float] = None
    created_at: str

    class Config:
        orm_mode = True
