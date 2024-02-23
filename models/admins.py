from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Admin(Base):

    __tablename__ = "admins"
     
    id = Column(BigInteger, primary_key=True, index=True)
    role_id = Column(BigInteger, default=0)
    username = Column(String, unique=True, nullable=True)
    phone_number = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    email_verified_at = Column(TIMESTAMP(timezone=True), nullable=True)
    pin = Column(String, nullable=True)
    password = Column(String, nullable=True)
    remember_token = Column(String, nullable=True)
    fbt = Column(Text, nullable=True)
    first_name = Column(String, nullable=True)
    other_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    avatar = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    updated_by = Column(BigInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_admin(db: Session, role_id: int = 0, username: str = None, email: str = None, phone_number: str = None, email_verified_at: str = None, pin: str = None, password: str = None,  remember_token: str = None, fbt: str = None, status: int = 0, created_by: int = 0, updated_by: int = 0):
    admin = Admin(role_id=role_id, username=username, email=email, phone_number=phone_number, email_verified_at=email_verified_at, pin=pin, password=password,  remember_token=remember_token, fbt=fbt, status=status, created_by=created_by, updated_by=updated_by, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

def update_admin(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Admin).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_admin(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Admin).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_admin_by_id(db: Session, id: int=0):
    return db.query(Admin).filter_by(id = id).first()

def get_admins(db: Session):
    return db.query(Admin).filter(Admin.deleted_at == None).order_by(desc(Admin.id))

def admin_login(db: Session, field: str=None):
    return db.query(Admin).filter(and_(or_(Admin.email == field, Admin.username == field), Admin.deleted_at == None)).first()