from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class Wallet(Base):

    __tablename__ = "wallets"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    account_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    balance = Column(Float, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_wallet(db: Session, user_id: int=0, account_name: str=None, account_number: str=None, balance: float=0, status: int = 0):
    wall = Wallet(user_id=user_id, account_name=account_name, account_number=account_number, balance=balance, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(wall)
    db.commit()
    db.refresh(wall)
    return wall

def update_wallet(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Wallet).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_wallet(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Wallet).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_wallet_by_id(db: Session, id: int=0):
    return db.query(Wallet).filter_by(id = id).first()

def get_wallets(db: Session):
    return db.query(Wallet).filter(Wallet.deleted_at == None).all()

def get_wallet_by_user_id(db: Session, user_id: int = 0):
    return db.query(Wallet).filter(Wallet.user_id == user_id).first()

def count_wallets(db: Session):
    return db.query(Wallet).count()

def add_user_to_wallet_balance(db: Session, user_id: int = 0, amount: float = 0):
    wallet = get_wallet_by_user_id(db=db, user_id=user_id)
    if wallet is None:
        return False
    else:
        balance = float(wallet.balance)
        new_balance = balance + amount
        new_balance = round(new_balance, 2)
        update_wallet(db=db, id=wallet.id, values={'balance': new_balance})
        return True

def sub_user_from_wallet_balance(db: Session, user_id: int = 0, amount: float = 0):
    wallet = get_wallet_by_user_id(db=db, user_id=user_id)
    if wallet is None:
        return False
    else:
        balance = float(wallet.balance)
        new_balance = balance - amount
        new_balance = round(new_balance, 2)
        update_wallet(db=db, id=wallet.id, values={'balance': new_balance})
        return True
