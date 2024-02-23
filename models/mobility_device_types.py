from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class Mobility_Device_Type(Base):

    __tablename__ = "mobility_device_types"
     
    id = Column(BigInteger, primary_key=True, index=True)
    battery_type_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    code = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    number_of_wheels = Column(Integer, default=0)
    number_of_batteries = Column(Integer, default=0)
    number_required_without_return = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    updated_by = Column(BigInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_mobility_device_type(db: Session, battery_type_id: int = 0, name: str = None, code: str = None, description: str = None, number_of_wheels: int = 0, number_of_batteries: int = 0, number_required_without_return: int = 0, created_by: int = 0):
    mob = Mobility_Device_Type(name=name, battery_type_id=battery_type_id, code=code, description=description, number_of_wheels=number_of_wheels, number_of_batteries=number_of_batteries, number_required_without_return=number_required_without_return, created_by=created_by, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(mob)
    db.commit()
    db.refresh(mob)
    return mob

def update_mobility_device_type(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Mobility_Device_Type).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_mobility_device_type(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Mobility_Device_Type).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_mobility_device_type_by_id(db: Session, id: int=0):
    return db.query(Mobility_Device_Type).filter_by(id = id).first()

def get_all_mobility_device_types(db: Session):
    return db.query(Mobility_Device_Type).filter(Mobility_Device_Type.deleted_at == None).order_by(desc(Mobility_Device_Type.id))

def count_mobility_device_types(db: Session):
    return db.query(Mobility_Device_Type).count()
