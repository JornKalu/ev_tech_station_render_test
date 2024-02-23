from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship
from settings.constants import TRANSACTION_TYPES


class Transaction(Base):

    __tablename__ = "transactions"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    wallet_id = Column(BigInteger, default=0)
    log_id = Column(BigInteger, default=0)
    station_id = Column(BigInteger, default=0)
    mobility_device_id = Column(BigInteger, default=0)
    reference = Column(String, nullable=True)
    external_reference = Column(String, nullable=True)
    external_source = Column(String, nullable=True)
    transaction_type = Column(Integer, default=0)
    amount = Column(Float, default=0)
    fee = Column(Float, default=0)
    total_amount = Column(Float, default=0)
    balance = Column(Float, default=0)
    battery_quantity = Column(Integer, default=0)
    battery_quantity_taken = Column(Integer, default=0)
    battery_taken_status = Column(SmallInteger, default=0)
    is_battery = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    misc_data = Column(String, nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_transaction(db: Session, user_id: int = 0, wallet_id: int = 0, log_id: int = 0, station_id: int = 0, mobility_device_id: int = 0, reference: str = None, external_reference: str = None, external_source: str = None, transaction_type: int = 0, amount: float = 0, fee: float = 0, total_amount: float = 0, balance: float = 0, battery_quantity: int = 0, battery_quantity_taken: int = 0, battery_taken_status: int = 0, is_battery: int = 0, status: int = 0, misc_data: str = None):
    trans = Transaction(user_id=user_id, wallet_id=wallet_id, log_id=log_id, station_id=station_id, mobility_device_id=mobility_device_id, reference=reference, external_reference=external_reference, external_source=external_source, transaction_type=transaction_type, amount=amount, fee=fee, total_amount=total_amount, balance=balance, battery_quantity=battery_quantity, battery_quantity_taken=battery_quantity_taken, battery_taken_status=battery_taken_status, is_battery=is_battery, status=status, misc_data=misc_data, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(trans)
    db.commit()
    db.refresh(trans)
    return trans

def create_deposit_transaction(db: Session, user_id: int = 0, wallet_id: int = 0, log_id: int = 0, station_id: int = 0, mobility_device_id: int = 0, reference: str = None, external_reference: str = None, external_source: str = None, amount: float = 0, fee: float = 0, total_amount: float = 0, balance: float = 0, battery_quantity: int = 0, battery_quantity_taken: int = 0, battery_taken_status: int = 0, is_battery: int = 0, status: int = 0, misc_data: str = None):
    return create_transaction(db=db, user_id=user_id, wallet_id=wallet_id, log_id=log_id, station_id=station_id, mobility_device_id=mobility_device_id, reference=reference, external_reference=external_reference, external_source=external_source, transaction_type=TRANSACTION_TYPES['DEPOSIT'], amount=amount, fee=fee, total_amount=total_amount, balance=balance, battery_quantity=battery_quantity, battery_quantity_taken=battery_quantity_taken, battery_taken_status=battery_taken_status, is_battery=is_battery, status=status, misc_data=misc_data)

def create_collection_transaction(db: Session, user_id: int = 0, wallet_id: int = 0, log_id: int = 0, station_id: int = 0, mobility_device_id: int = 0, reference: str = None, external_reference: str = None, external_source: str = None, amount: float = 0, fee: float = 0, total_amount: float = 0, balance: float = 0, battery_quantity: int = 0, battery_quantity_taken: int = 0, battery_taken_status: int = 0, is_battery: int = 0, status: int = 0, misc_data: str = None):
    return create_transaction(db=db, user_id=user_id, wallet_id=wallet_id, log_id=log_id, station_id=station_id, mobility_device_id=mobility_device_id, reference=reference, external_reference=external_reference, external_source=external_source, transaction_type=TRANSACTION_TYPES['COLLECTION'], amount=amount, fee=fee, total_amount=total_amount, balance=balance, battery_quantity=battery_quantity, battery_quantity_taken=battery_quantity_taken, battery_taken_status=battery_taken_status, is_battery=is_battery, status=status, misc_data=misc_data)

def update_transaction(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Transaction).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_transaction(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Transaction).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_transaction_by_id(db: Session, id: int=0):
    return db.query(Transaction).filter_by(id = id).first()

def get_single_transaction_by_reference(db: Session, reference: str=None):
    return db.query(Transaction).filter_by(reference = reference).first()

def get_single_transaction_by_external_reference(db: Session, external_reference: str=None):
    return db.query(Transaction).filter_by(external_reference = external_reference).first()

def get_transactions_by_user_id(db: Session, user_id: int=0):
    return db.query(Transaction).filter(and_(Transaction.user_id == user_id, Transaction.deleted_at == None)).all()

def get_transactions_by_user_id_and_status(db: Session, user_id: int=0, status: int=0):
    return db.query(Transaction).filter(and_(Transaction.user_id == user_id, Transaction.status == status, Transaction.deleted_at == None)).all()

def get_transactions_by_wallet_id(db: Session, wallet_id: int=0):
    return db.query(Transaction).filter(and_(Transaction.wallet_id == wallet_id, Transaction.deleted_at == None)).all()

def get_transactions_by_wallet_id_and_status(db: Session, wallet_id: int=0, status: int=0):
    return db.query(Transaction).filter(and_(Transaction.wallet_id == wallet_id, Transaction.status == status, Transaction.deleted_at == None)).all()

def get_deposits_transactions(db: Session):
    return db.query(Transaction).filter(Transaction.transaction_type == TRANSACTION_TYPES['DEPOSIT']).all()

def get_deposits_transactions_by_user_id(db: Session, user_id: int = 0):
    return db.query(Transaction).filter(and_(Transaction.transaction_type == TRANSACTION_TYPES['DEPOSIT'], Transaction.user_id == user_id)).all()

def get_collections_transactions(db: Session):
    return db.query(Transaction).filter(Transaction.transaction_type == TRANSACTION_TYPES['COLLECTION']).all()

def get_collections_transactions_by_user_id(db: Session, user_id: int = 0):
    return db.query(Transaction).filter(and_(Transaction.transaction_type == TRANSACTION_TYPES['COLLECTION'], Transaction.user_id == user_id)).all()

def get_transactions_by_log_id(db: Session, log_id: int=0):
    return db.query(Transaction).filter_by(log_id = log_id).first()

def get_all_transactions(db: Session):
    return db.query(Transaction).filter(Transaction.deleted_at == None).all()

def count_transactions(db: Session):
    return db.query(Transaction).count()

def count_transactions_by_reference(db: Session, reference: str = None):
    return db.query(Transaction).filter(Transaction.reference == reference).count()

def count_transactions_by_external_reference(db: Session, external_reference: str = None):
    return db.query(Transaction).filter(Transaction.external_reference == external_reference).count()

def check_if_external_refernce_exist(db: Session, external_reference: str = None):
    count = count_transactions_by_external_reference(db=db, external_reference=external_reference)
    if count > 0:
        return True
    else:
        return False