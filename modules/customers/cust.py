from typing import Dict
from database.model import get_single_user_by_id, get_single_user_by_phone_number, get_single_user_by_username, get_single_user_by_email, get_profile_by_user_id, get_single_setting_by_user_id, get_wallet_by_user_id, get_user_active_device, get_batteries_by_user_id_and_status, get_all_user_mobility_device, get_batteries_by_mobility_device_id, get_all_user_active_collections, get_single_battery_by_id, get_single_mobility_device_type_by_id, get_single_battery_type_by_id, get_all_batteries
from modules.utils.net import get_ip_info, process_phone_number
from modules.utils.tools import check_if_time_as_pass
from sqlalchemy.orm import Session

def get_user_collection_arrears(db: Session, user_id: int=0):
    amount = 0
    collections = get_all_user_active_collections(db=db, user_id=user_id)
    if len(collections) > 0:
        for i in range(len(collections)):
            coll = collections[i]
            if check_if_time_as_pass(time_str=coll.due_date) == True:
                battery = get_single_battery_by_id(db=db, id=coll.battery_id)
                if battery is not None:
                    amount = float(amount) + float(battery.collection_due_fees)
    return amount

def get_user_mob_batter_info(db: Session, user_id: int=0):
    mob_devices = get_all_user_mobility_device(db=db, user_id=user_id)
    if len(mob_devices) == 0:
        return []
    else:
        arr = []
        for i in range(len(mob_devices)):
            mob = mob_devices[i]
            mob_dev_type = get_single_mobility_device_type_by_id(db=db, id=mob.device_type_id)
            fee = 0
            if mob_dev_type is not None:
                battery_type_id = mob_dev_type.battery_type_id
                battery_type = get_single_battery_type_by_id(db=db, id=battery_type_id)
                if battery_type is not None:
                    fee = battery_type.fee
            ret = {
                'id': mob.id,
                'user_id': user_id,
                'code': mob.code,
                'name': mob.name,
                'device_type_id': mob.device_type_id,
                'model': mob.model,
                'registration_number': mob.registration_number,
                'vin': mob.vin,
                'latitude': mob.latitude,
                'longitude': mob.longitude,
                'conversion_date': mob.conversion_date,
                'front_image': mob.front_image,
                'left_image': mob.left_image,
                'right_image': mob.right_image,
                'back_image': mob.back_image,
                'battery_collection_status': mob.battery_collection_status,
                'status': mob.status,
                'created_at': mob.created_at,
                'type_name': mob.type_name,
                'type_code': mob.type_code,
                'type_description': mob.type_description,
                'number_of_wheels': mob.number_of_wheels,
                'number_of_batteries': mob.number_of_batteries,
                'fee': fee,
                'created_by': mob.created_by,
                'batteries': get_batteries_by_mobility_device_id(db=db, mobility_device_id=mob.id)
            }
            arr.append(ret)
        return arr
            

def get_customer_info(db: Session, user_id: int = 0):
    user = get_single_user_by_id(db=db, id=user_id)
    if user is None:
        return {
            'status': False,
            'message': 'Customer not found',
            'data': None
        }
    else:
        profile = get_profile_by_user_id(db=db, user_id=user_id)
        setting = get_single_setting_by_user_id(db=db, user_id=user_id)
        wallet = get_wallet_by_user_id(db=db, user_id=user_id)
        user_device = get_user_active_device(db=db, user_id=user_id)
        # batteries = get_batteries_by_user_id_and_status(db=db, user_id=user_id, status=1)
        mobility_devices = get_user_mob_batter_info(db=db, user_id=user_id)
        pin_available = False
        if user.pin is not None:
            pin_available = True
        collection_arrears = get_user_collection_arrears(db=db, user_id=user_id)
        data = {
            'id': user.id,
            'username': user.username,
            'phone_number': user.phone_number,
            'email': user.email,
            'qr_code': user.qr_code,
            'profile': profile,
            'setting': setting,
            'wallet': wallet,
            'user_device': user_device,
            'mobility_devices': mobility_devices,
            'pin_available': pin_available,
            'collection_arrears': collection_arrears,
        }
        return {
            'status': True,
            'message': 'Success',
            'data': data
        }
    
def get_customer_info_by_phone_number(db: Session, phone_number: str=None):
    country_code = "NG"
    processed_phone_number = process_phone_number(phone_number=phone_number, country_code=country_code)
    if processed_phone_number['status'] == False:
        return {
            'status': False,
            'message': processed_phone_number['message'],
            'data': None
        }
    else:
        phone = processed_phone_number['phone_number']
        user = get_single_user_by_phone_number(db=db, phone_number=phone)
        if user is None:
            return {
                'status': False,
                'message': 'Customer not found',
                'data': None
            }
        else:
            return get_customer_info(db=db, user_id=user.id)
        
def get_customer_info_by_email(db: Session, email: str=None):
    user = get_single_user_by_email(db=db, email=email)
    if user is None:
        return {
            'status': False,
            'message': 'Customer not found',
            'data': None
        }
    else:
        return get_customer_info(db=db, user_id=user.id)
        
def get_customer_info_by_username(db: Session, username: str=None):
    user = get_single_user_by_username(db=db, username=username)
    if user is None:
        return {
            'status': False,
            'message': 'Customer not found',
            'data': None
        }
    else:
        return get_customer_info(db=db, user_id=user.id)