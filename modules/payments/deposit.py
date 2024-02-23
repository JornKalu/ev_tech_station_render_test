from typing import Dict
from modules.external.flutterwave import verify_transaction
from modules.external.paystack import verify_paystack_transaction
from database.model import get_wallet_by_user_id, add_user_to_wallet_balance, sub_user_from_wallet_balance, create_deposit_transaction, check_if_external_refernce_exist
from sqlalchemy.orm import Session
from modules.utils.tools import generate_transaction_reference
import json

def complete_flutterwave_deposit(db: Session, user_id: int = 0, station_id: int = 0, transaction_id: str = None):
    if check_if_external_refernce_exist(db=db, external_reference=transaction_id) == True:
        return {
            'status': False,
            'message': 'Duplicate Transaction',
        }
    else:
        f_trans = verify_transaction(transaction_id=transaction_id)
        if 'status' not in f_trans:
            return {
                'status': False,
                'message': 'Could not verify transaction',
            }
        else:
            if f_trans['status'] != "success":
                return {
                    'status': False,
                    'message': 'Transaction not found',
                }
            else:
                f_data = f_trans['data']
                f_status = f_data['status']
                if f_status != "successful":
                    return {
                        'status': False,
                        'message': 'Transaction failed',
                    }
                else:
                    amount = float(f_data['charged_amount'])
                    reference = generate_transaction_reference(tran_type="Deposit", rand_type=2)
                    wallet = get_wallet_by_user_id(db=db, user_id=user_id)
                    wallet_id = 0
                    balance = 0
                    if wallet is not None:
                        wallet_id = wallet.id
                        balance = float(wallet.balance) + amount
                        balance = round(balance, 2)
                    add_user_to_wallet_balance(db=db, user_id=user_id, amount=amount)
                    create_deposit_transaction(db=db, user_id=user_id, wallet_id=wallet_id, station_id=station_id, reference=reference, external_reference=transaction_id, external_source="FLUTTERWAVE", amount=amount, total_amount=amount, balance=balance, status=1, misc_data=json.dumps(f_trans))
                    return {
                        'status': True,
                        'message': 'Success'
                    }

def complete_paystack_deposit(db: Session, user_id: int = 0, station_id: int = 0, transaction_id: str = None):
    if check_if_external_refernce_exist(db=db, external_reference=transaction_id) == True:
        return {
            'status': False,
            'message': 'Duplicate Transaction',
        }
    else:
        p_trans = verify_paystack_transaction(transaction_id=transaction_id)
        if 'status' not in p_trans:
            return {
                'status': False,
                'message': 'Could not verify transaction',
            }
        else:
            if p_trans['status'] != True:
                return {
                    'status': False,
                    'message': 'Transaction not found',
                }
            else:
                p_data = p_trans['data']
                if p_data['status'] != "success":
                    return {
                        'status': False,
                        'message': 'Transaction failed',
                    }
                else:
                    amount = float(p_data['amount']) / 100
                    amount = round(amount, 2)
                    reference = generate_transaction_reference(tran_type="Deposit", rand_type=2)
                    wallet = get_wallet_by_user_id(db=db, user_id=user_id)
                    wallet_id = 0
                    balance = 0
                    if wallet is not None:
                        wallet_id = wallet.id
                        balance = float(wallet.balance) + amount
                        balance = round(balance, 2)
                    add_user_to_wallet_balance(db=db, user_id=user_id, amount=amount)
                    create_deposit_transaction(db=db, user_id=user_id, station_id=station_id, wallet_id=wallet_id, reference=reference, external_reference=transaction_id, external_source="PAYSTACK", amount=amount, total_amount=amount, balance=balance, status=1, misc_data=json.dumps(p_trans))
                    return {
                        'status': True,
                        'message': 'Success'
                    }