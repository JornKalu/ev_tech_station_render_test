from fastapi import APIRouter, Request, Depends, HTTPException
from modules.payments.trans import process_collection_payment
from database.schema import PaymentModel, DepositResponseModel, ErrorResponse
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/payment",
    tags=["v1_payments"]
)

@router.post("/", response_model=DepositResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def pay(fields: PaymentModel, db: Session = Depends(get_session)):
    req = process_collection_payment(db=db, user_id=fields.user_id, station_id=fields.station_id, mobility_device_id=fields.mobility_device_id, amount=fields.amount)
    return req
