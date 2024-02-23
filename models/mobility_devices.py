from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship
from models.mobility_device_types import Mobility_Device_Type
from models.users import User
from models.profiles import Profile
from models.admins import Admin

class Mobility_Device(Base):

    __tablename__ = "mobility_devices"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    code = Column(String, nullable=True)
    name = Column(String, nullable=True)
    device_type_id = Column(BigInteger, default=0)
    model = Column(String, nullable=True)
    registration_number = Column(String, nullable=True)
    vin = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    conversion_date = Column(String, nullable=True)
    front_image = Column(String, nullable=True)
    left_image = Column(String, nullable=True)
    right_image = Column(String, nullable=True)
    back_image = Column(String, nullable=True)
    temp_transaction_id = Column(BigInteger, default=0)
    battery_collection_status = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    updated_by = Column(BigInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_mobility_device(db: Session, user_id: int = 0, code: str = None, name: str = None, device_type_id: int = 0, model: str = None, registration_number: str = None, vin: str = None, latitude: str = None, longitude: str = None, conversion_date: str = None, front_image: str = None, left_image: str = None, right_image: str = None, back_image: str = None, temp_transaction_id: int = 0, battery_collection_status: int = 0, created_by: int=0, status: int = 0):
    mob = Mobility_Device(user_id=user_id, code=code, name=name, device_type_id=device_type_id, model=model, registration_number=registration_number, vin=vin, latitude=latitude, longitude=longitude, conversion_date=conversion_date, front_image=front_image, left_image=left_image, right_image=right_image, back_image=back_image, temp_transaction_id=temp_transaction_id, battery_collection_status=battery_collection_status, status=status, created_by=created_by, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(mob)
    db.commit()
    db.refresh(mob)
    return mob

def update_mobility_device(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Mobility_Device).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_mobility_device(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Mobility_Device).filter_by(id = id).update(values)
    db.commit()
    return True

def get_query(db: Session):
    profiles = aliased(Profile)
    admins = aliased(Admin)
    subquery_profiles = db.query(func.concat(profiles.first_name, ' ', profiles.other_name, ' ', profiles.last_name)).filter(profiles.user_id == Mobility_Device.user_id).as_scalar()
    subquery_admins = db.query(admins.username).filter(admins.id == Mobility_Device.created_by).as_scalar()
    subquery_profiles_addr = db.query(profiles.address).filter(profiles.user_id == Mobility_Device.user_id).as_scalar()
    return db.query(Mobility_Device.id, Mobility_Device.user_id, Mobility_Device.code, Mobility_Device.name, Mobility_Device.device_type_id, Mobility_Device.model, Mobility_Device.registration_number, Mobility_Device.vin, Mobility_Device.latitude, Mobility_Device.longitude, Mobility_Device.conversion_date, Mobility_Device.front_image, Mobility_Device.left_image, Mobility_Device.right_image, Mobility_Device.back_image, Mobility_Device.temp_transaction_id, Mobility_Device.battery_collection_status, Mobility_Device.status, Mobility_Device.created_at, Mobility_Device_Type.name.label('type_name'), Mobility_Device_Type.code.label('type_code'), Mobility_Device_Type.description.label('type_description'), Mobility_Device_Type.number_of_wheels, Mobility_Device_Type.number_of_batteries, User.username, User.email, User.phone_number, subquery_profiles.label('customer_full_name'), subquery_profiles_addr.label('customer_address'), subquery_admins.label('created_by')).join(Mobility_Device_Type, Mobility_Device_Type.id == Mobility_Device.device_type_id).join(User, User.id == Mobility_Device.user_id)

def get_single_mobility_device_by_id(db: Session, id: int=0):
    main_query = get_query(db=db)
    return main_query.filter(Mobility_Device.id == id).first()

def get_all_user_mobility_device(db: Session, user_id: int=0):
    main_query = get_query(db=db)
    return main_query.filter(and_(Mobility_Device.user_id == user_id, Mobility_Device.deleted_at == None)).order_by(desc(Mobility_Device.id)).all()

def get_single_mobility_devices_by_user_id(db: Session, user_id: int=0):
    main_query = get_query(db=db)
    return main_query.filter(and_(Mobility_Device.user_id == user_id, Mobility_Device.deleted_at == None)).order_by(desc(Mobility_Device.id))

def get_single_mobility_devices_by_user_id_and_status(db: Session, user_id: int=0, status: int=0):
    main_query = get_query(db=db)
    return main_query.filter(and_(Mobility_Device.user_id == user_id, Mobility_Device.status == status, Mobility_Device.deleted_at == None)).order_by(desc(Mobility_Device.id))

def get_single_mobility_devices_by_type(db: Session, type_id: int=0):
    main_query = get_query(db=db)
    return main_query.filter(and_(Mobility_Device.device_type_id == type_id, Mobility_Device.deleted_at == None)).order_by(desc(Mobility_Device.id))

def get_single_mobility_devices_by_type_id_and_status(db: Session, type_id: int=0, status: int=0):
    main_query = get_query(db=db)
    return main_query.filter(and_(Mobility_Device.device_type_id == type_id, Mobility_Device.status == status, Mobility_Device.deleted_at == None)).order_by(desc(Mobility_Device.id))

def get_single_mobility_devices_by_status(db: Session, status: int=0):
    main_query = get_query(db=db)
    return main_query.filter(and_(Mobility_Device.status == status, Mobility_Device.deleted_at == None)).order_by(desc(Mobility_Device.id))

def get_all_mobility_devices(db: Session):
    main_query = get_query(db=db)
    return main_query.filter(Mobility_Device.deleted_at == None).order_by(desc(Mobility_Device.id))

def search_mobility_devices(db: Session, query: str = None):
    main_query = get_query(db=db)
    return main_query.filter(and_(or_(Mobility_Device.code.like('%' + str(query) + '%'), Mobility_Device.name.like('%' + str(query) + '%'), Mobility_Device.vin.like('%' + str(query) + '%'), Mobility_Device.registration_number.like('%' + str(query) + '%'), Mobility_Device.model.like('%' + str(query) + '%')), Mobility_Device.deleted_at == None)).order_by(desc(Mobility_Device.id))

def count_mobility_devices(db: Session):
    return db.query(Mobility_Device).count()