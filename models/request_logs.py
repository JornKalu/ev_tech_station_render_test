from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class Request_Log(Base):

    __tablename__ = "request_logs"
     
    id = Column(BigInteger, primary_key=True, index=True)
    server_type = Column(String, nullable=True)
    initial_instruction = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    name = Column(String, nullable=True)
    value = Column(String, nullable=True)
    response_value = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_request_log(db: Session, server_type: str = None, initial_instruction: str = None, ip_address: str = None, name: str = None, value: str = None, response_value: str = None):
    rl = Request_Log(server_type=server_type, initial_instruction=initial_instruction, ip_address=ip_address, name=name, value=value, response_value=response_value, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(rl)
    db.commit()
    db.refresh(rl)
    return rl

def update_request_log(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Request_Log).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_request_log_by_id(db: Session, id: int=0):
    return db.query(Request_Log).filter_by(id = id).first()

def get_all_request_logs(db: Session):
    return db.query(Request_Log).all()

def count_request_logs(db: Session):
    return db.query(Request_Log).count()