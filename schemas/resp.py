from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    detail: Optional[str] = None
    
    class Config:
        orm_mode = True

