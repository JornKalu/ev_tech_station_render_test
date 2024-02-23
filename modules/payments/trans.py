from typing import Dict
from sqlalchemy.orm import Session
from modules.utils.tools import generate_transaction_reference
from database.model import get_wallet_by_user_id, add_user_to_wallet_balance, sub_user_from_wallet_balance, create_collection_transaction, check_if_external_refernce_exist, get_single_user_by_id, get_single_mobility_device_by_id, get_single_station_by_id, update_mobility_device
import json

def process_collection_payment(db: Session, user_id: int=0, station_id: int=0, mobility_device_id: int=0, amount: int=0):
    user = get_single_user_by_id(db=db, id=user_id)
    if user is None:
        return {
            'status': False,
            'message': 'Customer not found',
        }
    else:
        station = get_single_station_by_id(db=db, id=station_id)
        if station is None:
            return {
                'status': False,
                'message': 'Station not found',
            }
        else:
            mobility_device = get_single_mobility_device_by_id(db=db, id=mobility_device_id)
            if mobility_device is None:
                return {
                    'status': False,
                    'message': 'Mobility device not found',
                }
            else:
                wallet = get_wallet_by_user_id(db=db, user_id=user_id)
                if wallet is None:
                    return {
                        'status': False,
                        'message': 'User wallet not found',
                    }
                else:
                    wallet_balance = float(wallet.balance)
                    if wallet_balance < amount:
                        return {
                            'status': False,
                            'message': 'Wallet balance is low'
                        }
                    else:
                        new_balance = wallet_balance - amount
                        new_balance = round(new_balance, 2)
                        reference = generate_transaction_reference(tran_type="Collection", rand_type=2)
                        sub_user_from_wallet_balance(db=db, user_id=user_id, amount=amount)
                        trans = create_collection_transaction(db=db, user_id=user_id, wallet_id=wallet.id, mobility_device_id=mobility_device_id, reference=reference, amount=amount, total_amount=amount, balance=new_balance, battery_quantity=mobility_device.number_of_batteries, battery_taken_status=0, is_battery=1, status=1)
                        update_mobility_device(db=db, id=mobility_device_id, values={'temp_transaction_id': trans.id, 'battery_collection_status': 1})
                        return {
                            'status': True,
                            'message': 'Success'
                        }
