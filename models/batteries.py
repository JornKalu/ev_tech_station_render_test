from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship
from models.logs import Log
# from models.profiles import Profile
# from models.users import User
# from models.stations import Station
# from models.mobility_devices import Mobility_Device
# from models.battery_types import Battery_Type
from models.stations_batteries import Station_Battery

class Battery(Base):

    __tablename__ = "batteries"
     
    id = Column(BigInteger, primary_key=True, index=True)
    type_id = Column(BigInteger, default=0)
    slot_id = Column(BigInteger, default=0)
    mobility_device_id = Column(BigInteger, default=0)
    code = Column(String, nullable=True)
    imei_code = Column(String, nullable=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    qr_code = Column(String, nullable=True)
    voltage = Column(String, nullable=True)
    temperature = Column(String, nullable=True)
    charge = Column(String, nullable=True)
    humidity = Column(String, nullable=True)
    electric_current = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    temp_host = Column(String, nullable=True)
    is_ejected = Column(SmallInteger, default=0)
    ejected_by = Column(BigInteger, default=0)
    temp_status = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    updated_by = Column(BigInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_battery(db: Session, type_id: int = 0, slot_id: int = 0, mobility_device_id: int = 0, code: str = None, imei_code: str = None, name: str = None, description: str = None, qr_code: str = None, voltage: str = None, temperature: str = None, charge: str = None, humidity: str = None, electric_current: str = None, latitude: str = None, longitude: str = None, temp_host: str = None, is_ejected: int = 0, ejected_by: int = 0, temp_status: int = None, status: int = 0, created_by: int = 0, updated_by: int = 0):
    bat = Battery(type_id=type_id, slot_id=slot_id, mobility_device_id=mobility_device_id, code=code, imei_code=imei_code, name=name, description=description, qr_code=qr_code, voltage=voltage, temperature=temperature, charge=charge, humidity=humidity, electric_current=electric_current, latitude=latitude, longitude=longitude, temp_host=temp_host, is_ejected=is_ejected, ejected_by=ejected_by, temp_status=temp_status, status=status, created_by=created_by, updated_by=updated_by, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(bat)
    db.commit()
    db.refresh(bat)
    return bat

def update_battery(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Battery).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_battery(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Battery).filter_by(id = id).update(values)
    db.commit()
    return True


def get_query(db: Session):
    # b = aliased(Battery)
    # # logs = aliased(Log)
    # profiles = aliased(Profile)
    # stations = aliased(Station)
    # mob_devices = aliased(Mobility_Device)
    # battery_type = aliased(Battery_Type)
    # stat_bat = aliased(Station_Battery)
    # # subquery_logs = db.query(logs.user_id).filter(logs.battery_id == b.id, logs.status == 1).as_scalar()
    # subquery_logs = db.query(mob_devices.user_id).filter(mob_devices.id == b.mobility_device_id).distinct().as_scalar()
    # # subquery_logs_station_id = db.query(logs.station_id).filter(logs.battery_id == b.id, logs.status == 1).as_scalar()
    # subquery_logs_slot_number = db.query(stat_bat.slot_number).filter(stat_bat.id == b.slot_id).as_scalar()
    # subquery_logs_station_id = db.query(stat_bat.station_id).filter(stat_bat.id == b.slot_id).distinct().as_scalar()
    # # subquery_logs_mobility_id = db.query(logs.mobility_device_id).filter(logs.battery_id == b.id, logs.status == 1).as_scalar()
    # subquery_profiles = db.query(func.concat(profiles.first_name, ' ', profiles.other_name, ' ', profiles.last_name)).filter(profiles.user_id == subquery_logs).as_scalar()
    # subquery_profiles_addr = db.query(profiles.address).filter(profiles.user_id == subquery_logs).as_scalar()
    # subquery_stations_name = db.query(stations.name).filter(stations.id == subquery_logs_station_id).as_scalar()
    # subquery_stations_addr = db.query(stations.address).filter(stations.id == subquery_logs_station_id).as_scalar()
    # subquery_mobility_code = db.query(mob_devices.code).filter(mob_devices.id == b.mobility_device_id).as_scalar()
    # subquery_mobility_name = db.query(mob_devices.name).filter(mob_devices.id == b.mobility_device_id).as_scalar()
    # subquery_mobility_device_type = db.query(mob_devices.device_type_id).filter(mob_devices.id == b.mobility_device_id).as_scalar()
    # subquery_mobility_model = db.query(mob_devices.model).filter(mob_devices.id == b.mobility_device_id).as_scalar()
    # subquery_mobility_reg = db.query(mob_devices.registration_number).filter(mob_devices.id == b.mobility_device_id).as_scalar()
    # subquery_mobility_vin = db.query(mob_devices.vin).filter(mob_devices.id == b.mobility_device_id).as_scalar()
    # subquery_b_type_name = db.query(battery_type.name).filter(battery_type.id == b.type_id).as_scalar()
    # subquery_b_type_fee = db.query(battery_type.fee).filter(battery_type.id == b.type_id).as_scalar()
    # subquery_b_type_collection_due_days = db.query(battery_type.collection_due_days).filter(battery_type.id == b.type_id).as_scalar()
    # subquery_b_type_collection_due_fees = db.query(battery_type.collection_due_fees).filter(battery_type.id == b.type_id).as_scalar()
    # return db.query(b.id, b.type_id, b.name, b.code, b.description, b.qr_code, b.voltage, b.temperature, b.charge, b.humidity, b.electric_current, b.latitude, b.longitude, b.status, b.created_at, subquery_profiles.label('customer_full_name'), subquery_profiles_addr.label('customer_address'), subquery_logs.label('customer_id'), subquery_stations_name.label('station_name'), subquery_stations_addr.label('station_address'), subquery_logs_station_id.label('station_id'), subquery_mobility_code.label('mobility_device_code'), subquery_mobility_name.label('mobility_device_name'), subquery_mobility_device_type.label('mobility_device_type'), subquery_mobility_model.label('mobility_device_model'), subquery_mobility_reg.label('mobility_device_registration_number'), subquery_mobility_vin.label('mobility_device_vin'), b.mobility_device_id, b.slot_id, subquery_b_type_name.label('battery_type_name'), subquery_b_type_fee.label('battery_type_fee')).select_from(b).distinct()
    return db.query(Battery)

def get_all_batteries(db: Session):
    # return db.query(Battery).filter(Battery.deleted_at == None).order_by(desc(Battery.id))
    main_query = get_query(db=db)
    return main_query.filter(Battery.deleted_at == None).order_by(desc(Battery.id))


def search_batteries(db: Session, query: str = None):
    # return db.query(Battery).filter(and_(or_(Battery.code.like('%' + str(query) + '%'), Battery.name.like('%' + str(query) + '%')), Battery.deleted_at == None)).order_by(desc(Battery.id))
    main_query = get_query(db=db)
    return main_query.filter(and_(or_(Battery.code.like('%' + str(query) + '%'), Battery.name.like('%' + str(query) + '%')), Battery.deleted_at == None)).order_by(desc(Battery.id))

def get_batteries_by_type(db: Session, type_id: int = 0):
    main_query = get_query(db=db)
    return main_query.filter(and_(Battery.type_id == type_id, Battery.deleted_at == None)).order_by(desc(Battery.id))

def get_batteries_by_status(db: Session, status: int = 0):
    main_query = get_query(db=db)
    return main_query.filter(and_(Battery.status == status, Battery.deleted_at == None)).order_by(desc(Battery.id))

def get_batteries_by_user_id(db: Session, user_id: int = 0):
    main_query = get_query(db=db)
    logs = aliased(Log)
    subquery = db.query(logs.battery_id).filter(logs.user_id == user_id).subquery()
    return main_query.filter(and_(Battery.id.in_(subquery), Battery.deleted_at == None)).order_by(desc(Battery.id)).all()

def get_batteries_by_user_id_and_status(db: Session, user_id: int = 0, status: int = 0):
    main_query = get_query(db=db)
    logs = aliased(Log)
    subquery = db.query(logs.battery_id).filter(logs.user_id == user_id).subquery()
    return main_query.filter(and_(Battery.id.in_(subquery), Battery.status == status, Battery.deleted_at == None)).order_by(desc(Battery.id)).all()

def get_batteries_by_station_id(db: Session, station_id: int = 0):
    main_query = get_query(db=db)
    # logs = aliased(Log)
    stat_bat = aliased(Station_Battery)
    # subquery = db.query(logs.battery_id).filter(logs.station_id == station_id).subquery()
    subquery = db.query(stat_bat.id).filter(stat_bat.station_id == station_id).subquery()
    return main_query.filter(and_(Battery.slot_id.in_(subquery), Battery.deleted_at == None)).order_by(desc(Battery.id))

def get_batteries_by_slot_id(db: Session, slot_id: int = 0):
    main_query = get_query(db=db)
    return main_query.filter(and_(Battery.slot_id == slot_id, Battery.deleted_at == None)).first()

def get_batteries_by_mobility_device_id(db: Session, mobility_device_id: int = 0):
    main_query = get_query(db=db)
    return main_query.filter(and_(Battery.mobility_device_id == mobility_device_id, Battery.deleted_at == None)).all()

def get_single_battery_by_id(db: Session, id: int=0):
    main_query = get_query(db=db)
    return main_query.filter_by(id = id).first()

def count_batteries(db: Session):
    return db.query(Battery).count()

def count_batteries_by_code(db: Session, code: str = None):
    return db.query(Battery).filter_by(code = code).count()

def check_if_battery_code_exists(db: Session, code: str = None):
    count = count_batteries_by_code(db=db, code=code)
    if count > 0:
        return True
    else:
        return False