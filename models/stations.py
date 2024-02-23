from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class Station(Base):

    __tablename__ = "stations"
     
    id = Column(BigInteger, primary_key=True, index=True)
    code = Column(String, nullable=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    image = Column(Text, nullable=True)
    autonomy_charge = Column(String, nullable=True)
    autonomy_charge_time = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    updated_by = Column(BigInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_station(db: Session, code: str = None, name: str = None, description: str = None, address: str = None, city: str = None, state: str = None, image: str = None, autonomy_charge: str = None, autonomy_charge_time: str = None, latitude: str = None, longitude: str = None, status: int = 0, created_by: int = 0, updated_by: int = 0):
    stat = Station(code=code, name=name, description=description, address=address, city=city, state=state, image=image, autonomy_charge=autonomy_charge, autonomy_charge_time=autonomy_charge_time, latitude=latitude, longitude=longitude, status=status, created_by=created_by, updated_by=updated_by, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat

def update_station(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Station).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_station(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Station).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_station_by_id(db: Session, id: int=0):
    return db.query(Station).filter_by(id = id).first()

def get_single_station_by_code(db: Session, code: str=None):
    return db.query(Station).filter(Station.code == code).first()

def get_all_stations(db: Session):
    return db.query(Station).filter(Station.deleted_at == None).order_by(desc(Station.id))

def search_stations(db: Session, query: str = None):
    return db.query(Station).filter(and_(or_(Station.name.like('%' + query + '%'), Station.code.like('%' + query + '%'), Station.address.like('%' + query + '%'), Station.city.like('%' + query + '%'), Station.state.like('%' + query + '%')), Station.deleted_at == None)).order_by(desc(Station.id))

def count_stations(db: Session):
    return db.query(Station).count()