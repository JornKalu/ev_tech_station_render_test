from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class Battery_Type(Base):

    __tablename__ = "battery_types"
     
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    voltage = Column(String, nullable=True)
    power = Column(String, nullable=True)
    fee = Column(Float, default=0)
    collection_due_days = Column(Integer, default=0)
    collection_due_fees = Column(Float, default=0)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    updated_by = Column(BigInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_battery_type(db: Session, name: str=None, description: str=None, voltage: str=None, power: str=None, fee: float=0, collection_due_days: int=0, collection_due_fees: float=0, status: int=0, created_by: int=0, updated_by: int=0):
    battery_type = Battery_Type(name=name, description=description, voltage=voltage, power=power, fee=fee, collection_due_days=collection_due_days, collection_due_fees=collection_due_fees, status=status, updated_by=updated_by, created_by=created_by, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(battery_type)
    db.commit()
    db.refresh(battery_type)
    return battery_type

def update_battery_type(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Battery_Type).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_battery_type(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Battery_Type).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_battery_type_by_id(db: Session, id: int=0):
    return db.query(Battery_Type).filter_by(id = id).first()

def get_all_battery_types(db: Session):
    return db.query(Battery_Type).filter(Battery_Type.deleted_at == None).order_by(desc(Battery_Type.id))

def count_battery_types(db: Session):
    return db.query(Battery_Type).count()