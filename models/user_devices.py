from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class User_Device(Base):

    __tablename__ = "user_devices"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    mac_address = Column(String, nullable=True)
    imei = Column(String, nullable=True)
    fbt = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_user_device(db: Session, user_id: int = 0, name: str = None, mac_address: str = None, imei: str = None, fbt: str = None, status: int = 0):
    ud = User_Device(user_id=user_id, name=name, mac_address=mac_address, imei=imei, fbt=fbt, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(ud)
    db.commit()
    db.refresh(ud)
    return ud

def update_user_device(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(User_Device).filter_by(id = id).update(values)
    db.commit()
    return True

def update_user_active_device(db: Session, user_id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(User_Device).filter(and_(User_Device.user_id == user_id, User_Device.status == 1)).update(values)
    db.commit()
    return True

def delete_user_device(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(User_Device).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_user_device_by_id(db: Session, id: int=0):
    return db.query(User_Device).filter_by(id = id).first()

def get_single_user_device_by_user_id(db: Session, user_id: int=0):
    return db.query(User_Device).filter(and_(User_Device.user_id == user_id, User_Device.deleted_at == None)).all()

def get_single_user_device_by_user_id_and_status(db: Session, user_id: int=0, status: int=0):
    return db.query(User_Device).filter(and_(User_Device.user_id == user_id, User_Device.status == status, User_Device.deleted_at == None)).all()

def get_user_active_device(db: Session, user_id: int=0):
    return db.query(User_Device).filter(and_(User_Device.user_id == user_id, User_Device.status == 1)).first()

def get_all_user_devices(db: Session):
    return db.query(User_Device).filter(User_Device.deleted_at == None).all()

def get_user_device_by_imei_and_address(db: Session, mac_address: str = None, imei: str = None):
    return db.query(User_Device).filter(and_(User_Device.imei == imei, User_Device.mac_address == mac_address)).first()

def get_user_device_by_fbt(db: Session, user_id: int = 0, fbt: str = None):
    return db.query(User_Device).filter(and_(User_Device.fbt == fbt, User_Device.user_id == user_id)).first()