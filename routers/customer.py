from fastapi import APIRouter, Request, Depends, HTTPException
from database.db import get_session
from sqlalchemy.orm import Session
from database.schema import ErrorResponse, UserResponseModel
from modules.customers.cust import get_customer_info, get_customer_info_by_phone_number, get_customer_info_by_email, get_customer_info_by_username

router = APIRouter(
    prefix="/customer",
    tags=["v1_customer"]
)

@router.get("/by_id/{id}", response_model=UserResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_id(db: Session = Depends(get_session), id: int = 0):
    return get_customer_info(db=db, user_id=id)

@router.get("/by_phone_number/{phone_number}", response_model=UserResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_phone_number(db: Session = Depends(get_session), phone_number: str = None):
    return get_customer_info_by_phone_number(db=db, phone_number=phone_number)

@router.get("/by_email/{email}", response_model=UserResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_email(db: Session = Depends(get_session), email: str = None):
    return get_customer_info_by_email(db=db, email=email)

@router.get("/by_username/{username}", response_model=UserResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_username(db: Session = Depends(get_session), username: str = None):
    return get_customer_info_by_username(db=db, username=username)
