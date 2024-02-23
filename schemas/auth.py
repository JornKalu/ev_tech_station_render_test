from typing import Optional, List
from pydantic import BaseModel, EmailStr, constr
# from schemas.battery import BatteryModel

class UserProfileModel(BaseModel):
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    nationality: Optional[str] = None
    bvn: Optional[str] = None
    nin: Optional[str] = None
    drivers_licence_number: Optional[str] = None
    drivers_licence_photo: Optional[str] = None
    passport: Optional[str] = None
    signature: Optional[str] = None
    nok_first_name: Optional[str] = None
    nok_other_name: Optional[str] = None
    nok_last_name: Optional[str] = None
    nok_phone_number: Optional[str] = None
    nok_email: Optional[str] = None
    nok_address: Optional[str] = None
    nok_city: Optional[str] = None
    nok_state: Optional[str] = None
    nok_postal_code: Optional[str] = None
    id_verification_type: Optional[int] = 0
    id_status: Optional[int] = 0
    status: Optional[int] = 0

    class Config:
        orm_mode = True

class UserSettingModel(BaseModel):
    email_notification: Optional[int] = 0
    sms_notification: Optional[int] = 0

    class Config:
        orm_mode = True

class UserWalletModel(BaseModel):
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    balance: Optional[float] = 0
    status: Optional[int] = 0

    class Config:
        orm_mode = True

class UserDeviceModel(BaseModel):
    name: Optional[str] = None
    mac_address: Optional[str] = None
    imei: Optional[str] = None
    fbt: Optional[str] = None
    status: Optional[int] = 0

    class Config:
        orm_mode = True

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
    battery_type_name: Optional[str] = None
    battery_type_fee: Optional[float] = None
    created_at: str

    class Config:
        orm_mode = True

class MobilityDeviceModel(BaseModel):
    id: int
    user_id: int
    device_type_id: int
    code: Optional[str] = None
    name: Optional[str] = None
    model: Optional[str] = None
    registration_number: Optional[str] = None
    vin: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    conversion_date: Optional[str] = None
    front_image: Optional[str] = None
    left_image: Optional[str] = None
    right_image: Optional[str] = None
    back_image: Optional[str] = None
    battery_collection_status: Optional[int] = 0
    status: Optional[int] = 0
    fee: Optional[float] = 0
    created_at: Optional[str] = None
    type_name: Optional[str] = None
    type_code: Optional[str] = None
    type_description: Optional[str] = None
    number_of_wheels: Optional[int] = None
    number_of_batteries: Optional[int] = None
    created_by: Optional[str] = None
    batteries: Optional[List[BatteryModel]] = None

    class Config:
        orm_mode = True

class UserModel(BaseModel):
    id: int
    username: str
    phone_number: str
    email: str
    profile: Optional[UserProfileModel] = None
    setting: Optional[UserSettingModel] = None
    wallet: Optional[UserWalletModel] = None
    user_device: Optional[UserDeviceModel] = None
    mobility_devices: Optional[List[MobilityDeviceModel]] = None
    pin_available: Optional[bool] = None
    collection_arrears: Optional[float] = 0

    class Config:
        orm_mode = True

class UserResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[UserModel] = None

    class Config:
        orm_mode = True
        