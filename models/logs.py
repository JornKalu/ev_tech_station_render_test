from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class Log(Base):

    __tablename__ = "logs"
     
    id = Column(BigInteger, primary_key=True, index=True)
    admin_id = Column(BigInteger, default=0)
    user_id = Column(BigInteger, default=0)
    battery_id = Column(BigInteger, default=0)
    station_id = Column(BigInteger, default=0)
    mobility_device_id = Column(BigInteger, default=0)
    user_device_id = Column(BigInteger, default=0)
    slot_id = Column(BigInteger, default=0)
    transaction_id = Column(BigInteger, default=0)
    request_log_id = Column(BigInteger, default=0)
    slot_number = Column(Integer, default=0)
    battery_charge = Column(Integer, default=0)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_log(db: Session, admin_id: int = 0, user_id: int = 0, battery_id: int = 0, station_id: int = 0, mobility_device_id: int = 0, user_device_id: int = 0, slot_id: int = 0, transaction_id: int = 0, request_log_id: int = 0, slot_number: int = 0, battery_charge: int = 0, latitude: str = None, longitude: str = None, status: int = 0):
    log = Log(admin_id=admin_id, user_id=user_id, battery_id=battery_id, station_id=station_id, mobility_device_id=mobility_device_id, user_device_id=user_device_id, slot_id=slot_id, transaction_id=transaction_id, request_log_id=request_log_id, slot_number=slot_number, battery_charge=battery_charge, latitude=latitude, longitude=longitude, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def update_log(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Log).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_log(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Log).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_log_by_id(db: Session, id: int=0):
    return db.query(Log).filter_by(id = id).first()

def get_logs_by_user_id(db: Session, user_id: int=0):
    return db.query(Log).filter(and_(Log.user_id == user_id, Log.deleted_at == None)).all()

def get_logs_by_user_id_and_status(db: Session, user_id: int=0, status: int=0):
    return db.query(Log).filter(and_(Log.user_id == user_id, Log.status == status, Log.deleted_at == None)).all()

def get_logs_by_station_id(db: Session, station_id: int=0):
    return db.query(Log).filter(and_(Log.station_id == station_id, Log.deleted_at == None)).all()

def get_logs_by_station_id_and_status(db: Session, station_id: int=0, status: int=0):
    return db.query(Log).filter(and_(Log.station_id == station_id, Log.status == status, Log.deleted_at == None)).all()

def get_logs_by_mobility_device_id(db: Session, mobility_device_id: int=0):
    return db.query(Log).filter(and_(Log.mobility_device_id == mobility_device_id, Log.deleted_at == None)).all()

def get_logs_by_mobility_device_id_and_status(db: Session, mobility_device_id: int=0, status: int=0):
    return db.query(Log).filter(and_(Log.mobility_device_id == mobility_device_id, Log.status == status, Log.deleted_at == None)).all()

def get_logs_by_user_device_id(db: Session, user_device_id: int=0):
    return db.query(Log).filter(and_(Log.user_device_id == user_device_id, Log.deleted_at == None)).all()

def get_logs_by_user_device_id_and_status(db: Session, user_device_id: int=0, status: int=0):
    return db.query(Log).filter(and_(Log.user_device_id == user_device_id, Log.status == status, Log.deleted_at == None)).all()

def get_all_logs(db: Session):
    return db.query(Log).filter(Log.deleted_at == None).all()

def count_logs(db: Session):
    return db.query(Log).count()