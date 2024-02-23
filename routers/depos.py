from fastapi import APIRouter, Request, Depends, HTTPException
from modules.payments.deposit import complete_flutterwave_deposit, complete_paystack_deposit
from database.schema import FluttewaveDeposit, DepositResponseModel, ErrorResponse
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/deposits",
    tags=["v1_deposits"]
)

@router.post("/flutterwave", response_model=DepositResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def flutterwave_deposit(fields: FluttewaveDeposit, db: Session = Depends(get_session)):
    req = complete_flutterwave_deposit(db=db, user_id=fields.user_id, station_id=fields.station_id, transaction_id=fields.transaction_id)
    return req

@router.post("/paystack", response_model=DepositResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def paystack_deposit(fields: FluttewaveDeposit, db: Session = Depends(get_session)):
    req = complete_paystack_deposit(db=db, user_id=fields.user_id, station_id=fields.station_id, transaction_id=fields.transaction_id)
    return req
