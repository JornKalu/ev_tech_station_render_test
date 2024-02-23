from fastapi import APIRouter, Request, Depends, HTTPException
from database.db import get_session
from sqlalchemy.orm import Session
from modules.misc.req_test import store_get_request_data, store_post_request_data

router = APIRouter(
    prefix="/v1/test",
    tags=["v1_test"]
)

@router.get("/get_requests")
async def get_requests(request: Request, db: Session = Depends(get_session)):
    body = await request.body()
    return store_get_request_data(db=db, data=body)

@router.post("/post_requests")
async def post_requests(request: Request, db: Session = Depends(get_session)):
    body = await request.body()
    return store_post_request_data(db=db, data=body)