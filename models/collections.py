from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, cast
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class Collection(Base):

    __tablename__ = "collections"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    mobility_device_id = Column(BigInteger, default=0)
    station_id = Column(BigInteger, default=0)
    battery_id = Column(BigInteger, default=0)
    batteries = Column(String, nullable=True)
    date_of_collection = Column(String, nullable=True)
    due_date = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_collections(db: Session, user_id: int = 0, mobility_device_id: int = 0, station_id: int = 0, battery_id: int = 0, batteries: str = None, date_of_collection: str = None, due_date: str = None, status: int = 0):
    coll = Collection(user_id=user_id, mobility_device_id=mobility_device_id, station_id=station_id, battery_id=battery_id, batteries=batteries, date_of_collection=date_of_collection, due_date=due_date, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(coll)
    db.commit()
    db.refresh(coll)
    return coll

def update_collection(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Collection).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_collection(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Collection).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_collection_by_id(db: Session, id: int=0):
    return db.query(Collection).filter_by(id = id).first()

def get_all_collections(db: Session):
    return db.query(Collection).all()

def get_all_user_active_collections(db: Session, user_id: int = 0):
    return db.query(Collection).filter(Collection.user_id == user_id).all()

def get_active_user_battery_collection(db: Session, user_id: int = 0, battery_id: int = 0):
    return db.query(Collection).filter(and_(Collection.user_id == user_id, Collection.battery_id == battery_id, Collection.status == 0)).first()