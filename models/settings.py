from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class Setting(Base):

    __tablename__ = "settings"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    email_notification = Column(SmallInteger, default=0)
    sms_notification = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_setting(db: Session, user_id: int=0, email_notification: int=0, sms_notification: int = 0):
    sett = Setting(user_id=user_id, email_notification=email_notification, sms_notification=sms_notification, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(sett)
    db.commit()
    db.refresh(sett)
    return sett

def update_setting(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Setting).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_setting(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Setting).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_setting_by_id(db: Session, id: int=0):
    return db.query(Setting).filter_by(id = id).first()

def get_single_setting_by_user_id(db: Session, user_id: int=0):
    return db.query(Setting).filter_by(user_id = user_id).first()

def get_settings(db: Session):
    return db.query(Setting).filter(Setting.deleted_at == None).all()

def count_settings(db: Session):
    return db.query(Setting).count()