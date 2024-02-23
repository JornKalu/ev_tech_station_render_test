from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime
from sqlalchemy.orm import relationship


class Profile(Base):

    __tablename__ = "profiles"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    first_name = Column(String, nullable=True)
    other_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    bvn = Column(String, nullable=True)
    nin = Column(String, nullable=True)
    drivers_licence_number = Column(String, nullable=True)
    drivers_licence_photo = Column(Text, nullable=True)
    passport = Column(Text, nullable=True)
    signature = Column(Text, nullable=True)
    nok_first_name = Column(String, nullable=True)
    nok_other_name = Column(String, nullable=True)
    nok_last_name = Column(String, nullable=True)
    nok_phone_number = Column(String, nullable=True)
    nok_email = Column(String, nullable=True)
    nok_address = Column(String, nullable=True)
    nok_city = Column(String, nullable=True)
    nok_state = Column(String, nullable=True)
    nok_postal_code = Column(String, nullable=True)
    id_verification_type = Column(Integer, default=0)
    id_status = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_profile(db: Session, user_id: int=0):
    profile = Profile(user_id=user_id, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def update_profile(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Profile).filter_by(id = id).update(values)
    db.commit()
    return True

def update_profile_by_user_id(db: Session, user_id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Profile).filter_by(user_id = user_id).update(values)
    db.commit()
    return True

def delete_profile(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Profile).filter_by(id = id).update(values)
    db.commit()
    return True

def get_profile_by_user_id(db: Session, user_id: int = 0):
    return db.query(Profile).filter(Profile.user_id == user_id).first()