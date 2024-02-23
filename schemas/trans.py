from typing import Optional
from pydantic import BaseModel

class FluttewaveDeposit(BaseModel):
    user_id: int
    station_id: Optional[int] = 0
    transaction_id: str

    class Config:
        orm_mode = True
        
class PaymentModel(BaseModel):
    user_id: int
    station_id: int
    mobility_device_id: int
    amount: float

    class Config:
        orm_mode = True
        
        
class DepositResponseModel(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True