from typing import List, Dict, Any
from database.model import get_single_station_by_id, create_request_log, get_stations_batteries_by_station_id, update_station, get_station_slot, update_station_battery, get_batteries_by_slot_id, update_battery, get_batteries_by_station_id, get_batteries_by_slot_id, create_collections, get_single_mobility_device_by_id, get_single_battery_type_by_id, get_single_battery_by_id, get_active_user_battery_collection, update_collection, update_mobility_device, update_request_log, get_single_station_by_code
from sqlalchemy.orm import Session
from database.db import get_added_laravel_datetime, get_laravel_datetime
from modules.utils.tools import json_loader, process_schema_dictionary
import json

def get_single_station_info(db: Session, station_id: int=0):
    station = get_single_station_by_id(db=db, id=station_id)
    if station is None:
        return {}
    else:
        slots_info = get_stations_batteries_by_station_id(db=db, station_id=station.id)
        slots = []
        if len(slots_info) > 0:
            for i in range(len(slots_info)):
                slot = slots_info[i]
                battery_code = None
                battery_id = 0
                battery = get_batteries_by_slot_id(db=db, slot_id=slot.id)
                if battery is not None:
                    battery_id = battery.id
                    battery_code = battery.code
                res = {
                    'id': slot.id,
                    'station_id': station.id,
                    'battery_id': battery_id,
                    'battery_code': battery_code,
                    'slot_number': slot.slot_number,
                    'status': slot.status,
                    'created_at': slot.created_at,
                    'updated_at': slot.updated_at,
                }
                slots.append(res)
        return {
            'id': station.id,
            'code': station.code,
            'name': station.name,
            'description': station.description,
            'address': station.address,
            'city': station.city,
            'state': station.state,
            'image': station.image,
            'autonomy_charge': station.autonomy_charge,
            'autonomy_charge_time': station.autonomy_charge_time,
            'latitude': station.latitude,
            'longitude': station.longitude,
            'status': station.status,
            'created_at': station.created_at,
            'slots': slots
        }

def get_single_station_info_by_code(db: Session, code: str=None):
    station = get_single_station_by_code(db=db, code=code)
    if station is None:
        return {}
    else:
        slots_info = get_stations_batteries_by_station_id(db=db, station_id=station.id)
        slots = []
        if len(slots_info) > 0:
            for i in range(len(slots_info)):
                slot = slots_info[i]
                battery_code = None
                battery_id = 0
                battery = get_batteries_by_slot_id(db=db, slot_id=slot.id)
                if battery is not None:
                    battery_id = battery.id
                    battery_code = battery.code
                res = {
                    'id': slot.id,
                    'station_id': station.id,
                    'battery_id': battery_id,
                    'battery_code': battery_code,
                    'slot_number': slot.slot_number,
                    'status': slot.status,
                    'created_at': slot.created_at,
                    'updated_at': slot.updated_at,
                }
                slots.append(res)
        return {
            'id': station.id,
            'code': station.code,
            'name': station.name,
            'description': station.description,
            'address': station.address,
            'city': station.city,
            'state': station.state,
            'image': station.image,
            'autonomy_charge': station.autonomy_charge,
            'autonomy_charge_time': station.autonomy_charge_time,
            'latitude': station.latitude,
            'longitude': station.longitude,
            'status': station.status,
            'created_at': station.created_at,
            'slots': slots
        }

def open_station_slot_for_charging(db: Session, station_id: int=0, mobility_device_id: int=0, slot_number: int=0):
    station = get_single_station_by_id(db=db, id=station_id)
    if station is None:
        return {
            'status': False,
            'message': 'Station not found'
        }
    else:
        station_slot = get_station_slot(db=db, station_id=station_id, slot_number=slot_number)
        if station_slot is None:
            return {
                'status': False,
                'message': 'Slot not found',
            }
        else:
            update_station_battery(db=db, id=station_slot.id, values={'station_allow_charge': 1, 'battery_eject': 1, 'battery_ejected_by': mobility_device_id})
            # battery = get_batteries_by_slot_id(db=db, slot_id=station_slot.id)
            # if battery is None:
            #     pass
            return {
                'status': True,
                'message': 'Success'
            }
        
def open_station_slot_for_charging_by_code(db: Session, station_code: str=None, mobility_device_id: int=0, slot_number: int=0):
    station = get_single_station_by_code(db=db, code=station_code)
    if station is None:
        return {
            'status': False,
            'message': 'Station not found'
        }
    else:
        station_slot = get_station_slot(db=db, station_id=station.id, slot_number=slot_number)
        if station_slot is None:
            return {
                'status': False,
                'message': 'Slot not found',
            }
        else:
            update_station_battery(db=db, id=station_slot.id, values={'station_allow_charge': 1, 'battery_eject': 1, 'battery_ejected_by': mobility_device_id})
            # battery = get_batteries_by_slot_id(db=db, slot_id=station_slot.id)
            # if battery is None:
            #     pass
            return {
                'status': True,
                'message': 'Success'
            }

def manage_station_slots(db: Session, station_id: int=0, mobility_device_id: int=0, slots: List=[]):
    station = get_single_station_by_id(db=db, id=station_id)
    if station is None:
        return {
            'status': False,
            'message': 'Station not found'
        }
    else:
        user_id = 0
        mobility_device = get_single_mobility_device_by_id(db=db, id=mobility_device_id)
        if mobility_device is not None:
            user_id = mobility_device.user_id
        if len(slots) > 0:
            for i in range(len(slots)):
                slot = slots[i]
                station_slot = get_station_slot(db=db, station_id=station_id, slot_number=slot['slot_number'])
                if station_slot is not None:
                    if 'is_ejected' in slot:
                        if slot['is_ejected'] == 1:
                            collection_date = None
                            if slot['battery_id'] > 0:
                                collection_date = calculate_battery_collection_date(db=db, battery_id=slot['battery_id'])
                            update_battery(db=db, id=slot['battery_id'], values={'slot_id': 0, 'mobility_device_id': mobility_device_id, 'status': 0, 'temp_status': None, 'temp_host': mobility_device.code})
                            update_station_battery(db=db, id=station_slot.id, values={'status': 0})
                            create_collections(db=db, user_id=user_id, mobility_device_id=mobility_device_id, station_id=station_id, battery_id=slot['battery_id'], date_of_collection=get_laravel_datetime(), due_date=collection_date, status=0)
                            if mobility_device_id > 0:
                                update_mobility_device(db=db, id=mobility_device_id, values={'temp_transaction_id': 0, 'battery_collection_status': 0})
                    if 'is_returned' in slot:
                        if slot['is_returned'] == 1:
                            update_battery(db=db, id=slot['battery_id'], values={'slot_id': station_slot.id, 'mobility_device_id': 0, 'status': 0, 'temp_status': 3, 'temp_host': station.code})
                            update_station_battery(db=db, id=station_slot.id, values={'status': 1, 'station_allow_charge': 1})
                            coll = get_active_user_battery_collection(db=db, user_id=user_id, battery_id=slot['battery_id'])
                            if coll is not None:
                                update_collection(db=db, id=coll.id, values={'status': 1})
        return {
            'status': True,
            'message': 'Success'
        }

def manage_station_slots_by_code(db: Session, station_code: str=None, mobility_device_id: int=0, slots: List=[]):
    station = get_single_station_by_code(db=db, code=station_code)
    if station is None:
        return {
            'status': False,
            'message': 'Station not found'
        }
    else:
        user_id = 0
        mobility_device = get_single_mobility_device_by_id(db=db, id=mobility_device_id)
        if mobility_device is not None:
            user_id = mobility_device.user_id
        if len(slots) > 0:
            for i in range(len(slots)):
                slot = slots[i]
                station_slot = get_station_slot(db=db, station_id=station.id, slot_number=slot['slot_number'])
                if station_slot is not None:
                    if 'is_ejected' in slot:
                        if slot['is_ejected'] == 1:
                            collection_date = None
                            if slot['battery_id'] > 0:
                                collection_date = calculate_battery_collection_date(db=db, battery_id=slot['battery_id'])
                            update_battery(db=db, id=slot['battery_id'], values={'slot_id': 0, 'mobility_device_id': mobility_device_id, 'status': 0, 'temp_status': None, 'temp_host': mobility_device.code})
                            update_station_battery(db=db, id=station_slot.id, values={'status': 0})
                            create_collections(db=db, user_id=user_id, mobility_device_id=mobility_device_id, station_id=station.id, battery_id=slot['battery_id'], date_of_collection=get_laravel_datetime(), due_date=collection_date, status=0)
                            if mobility_device_id > 0:
                                update_mobility_device(db=db, id=mobility_device_id, values={'temp_transaction_id': 0, 'battery_collection_status': 0})
                    if 'is_returned' in slot:
                        if slot['is_returned'] == 1:
                            update_battery(db=db, id=slot['battery_id'], values={'slot_id': station_slot.id, 'mobility_device_id': 0, 'status': 0, 'temp_status': 3, 'temp_host': station.code})
                            update_station_battery(db=db, id=station_slot.id, values={'status': 1, 'station_allow_charge': 1})
                            coll = get_active_user_battery_collection(db=db, user_id=user_id, battery_id=slot['battery_id'])
                            if coll is not None:
                                update_collection(db=db, id=coll.id, values={'status': 1})
        return {
            'status': True,
            'message': 'Success'
        }

def calculate_battery_collection_date(db: Session, battery_id: int = 0):
    collection_date = None
    battery = get_single_battery_by_id(db=db, id=battery_id)
    if battery is None:
        collection_due_days = battery.collection_due_days
        if collection_due_days > 0:
            collection_date = get_added_laravel_datetime(days=collection_due_days)
    return collection_date

def process_station_request(db: Session, data: Any):
    create_request_log(db=db, server_type="station", name="post", value=str(data))
    if isinstance(data, bytes) == False:
        return {
            'status': False,
            'message': 'Invalid request'
        }
    else:
        data = data.decode()
        jdata = json_loader(jstr=data)
        if jdata is None:
            return {
                'status': False,
                'message': 'Invalid data',
            }
        else:
            if type(jdata) is not dict:
                return {
                    'status': False,
                    'message': 'Invalid body',
                }
            jlist = list(jdata.keys())
            clist = ['StationID', 'BatteryData', 'TimeStamp']
            check =  all(item in jlist for item in clist)
            if check is False:
                return {
                    'status': False,
                    'message': 'Validation error',
                }
            else:
                battery_data = jdata['BatteryData']
                if len(battery_data) == 0:
                    return {
                        'status': False,
                        'message': 'Empty Battery Data',
                    }
                else:
                    station_id = jdata['StationID']
                    time_stamp = jdata['TimeStamp']


def sync_station_info(db: Session, initial_instruction: str=None, original_values: str=None, station_id: int=0, latitude: str=None, longitude: str=None, slots: List=[], status: int=None):
    req = create_request_log(db=db, initial_instruction=initial_instruction, server_type="station", name="post", value=original_values)
    station = get_single_station_by_id(db=db, id=station_id)
    if station is None:
        fin_data = {
            'status': False,
            'message': 'Not found',
            'data': None
        }
        update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
    else:
        new_status = None
        up_vals = {}
        if latitude is not None:
            up_vals['latitude'] = latitude
        if longitude is not None:
            up_vals['longitude'] = longitude
        if status is not None:
            if station.status != status:
                up_vals['status'] = status
                new_status = status
            else:
                new_status = station.status
        else:
            new_status = station.status
        if len(up_vals) > 0:
            update_station(db=db, id=station.id, values=up_vals)
        data = {
            'id': station.id,
            'status': new_status,
        }
        slot_data = []
        if slots is not None:
            if len(slots) > 0:
                for i in range(len(slots)):
                    slot = slots[i]
                    temp_dict = {
                        'slot_number': slot['slot_number'],
                        'allow_charge': None,
                        'battery_docked': None,
                        'battery_eject': None,
                        'battery_stop_charge': None,
                        'status': None,
                    }
                    station_slot = get_station_slot(db=db, station_id=station.id, slot_number=slot['slot_number'])
                    if station_slot is None:
                        vals = {}
                        if station_slot.station_allow_charge is not None:
                            temp_dict['allow_charge'] = station_slot.station_allow_charge
                            vals['station_allow_charge'] = None
                        # if 'allow_charge' in slot:
                        #     if slot['allow_charge'] is not None:
                        #         vals['allow_charge'] = slot['allow_charge']
                        #         temp_dict['allow_charge'] = slot['allow_charge']
                        #     else:
                        #         temp_dict['allow_charge'] = station.station_allow_charge
                        # else:
                        #     temp_dict['allow_charge'] = station.station_allow_charge
                        if station_slot.battery_docked is not None:
                            temp_dict['battery_docked'] = station.battery_docked
                            vals['battery_docked'] = None
                        if station_slot.battery_eject is not None:
                            temp_dict['battery_eject'] = station.battery_eject
                            vals['battery_eject'] = None
                        if station_slot.battery_stop_charge is not None:
                            temp_dict['battery_stop_charge'] = station.battery_stop_charge
                            vals['battery_stop_charge'] = None
                        if station_slot.status is not None:
                            temp_dict['status'] = station.status
                        update_station_battery(db=db, id=station_slot.id, values=vals)
                    slot_data.append(temp_dict)
            
        data['slots'] = slot_data
        fin_data = {
            'status': True,
            'message': 'Success',
            'data': data
        }
        update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
        return fin_data

def sync_station_info_by_code(db: Session, initial_instruction: str=None, original_values: str=None, station_code: str=None, latitude: str=None, longitude: str=None, slots: List=[], status: int=None):
    # req = create_request_log(db=db, initial_instruction=initial_instruction, server_type="station", name="post", value=original_values)
    station = get_single_station_by_code(db=db, code=station_code)
    return station
    if station is None:
        fin_data = {
            'status': False,
            'message': 'Not found',
            'data': None
        }
        update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
    else:
        new_status = None
        up_vals = {}
        if latitude is not None:
            up_vals['latitude'] = latitude
        if longitude is not None:
            up_vals['longitude'] = longitude
        if status is not None:
            if station.status != status:
                up_vals['status'] = status
                new_status = status
            else:
                new_status = station.status
        else:
            new_status = station.status
        if len(up_vals) > 0:
            update_station(db=db, id=station.id, values=up_vals)
        data = {
            'id': station.id,
            'status': new_status,
        }
        slot_data = []
        if slots is not None:
            if len(slots) > 0:
                for i in range(len(slots)):
                    slot = slots[i]
                    temp_dict = {
                        'slot_number': slot['slot_number'],
                        'allow_charge': None,
                        'battery_docked': None,
                        'battery_eject': None,
                        'battery_stop_charge': None,
                        'status': None,
                    }
                    station_slot = get_station_slot(db=db, station_id=station.id, slot_number=slot['slot_number'])
                    if station_slot is None:
                        vals = {}
                        if station_slot.station_allow_charge is not None:
                            temp_dict['allow_charge'] = station_slot.station_allow_charge
                            vals['station_allow_charge'] = None
                        # if 'allow_charge' in slot:
                        #     if slot['allow_charge'] is not None:
                        #         vals['allow_charge'] = slot['allow_charge']
                        #         temp_dict['allow_charge'] = slot['allow_charge']
                        #     else:
                        #         temp_dict['allow_charge'] = station.station_allow_charge
                        # else:
                        #     temp_dict['allow_charge'] = station.station_allow_charge
                        if station_slot.battery_docked is not None:
                            temp_dict['battery_docked'] = station.battery_docked
                            vals['battery_docked'] = None
                        if station_slot.battery_eject is not None:
                            temp_dict['battery_eject'] = station.battery_eject
                            vals['battery_eject'] = None
                        if station_slot.battery_stop_charge is not None:
                            temp_dict['battery_stop_charge'] = station.battery_stop_charge
                            vals['battery_stop_charge'] = None
                        if station_slot.status is not None:
                            temp_dict['status'] = station.status
                        update_station_battery(db=db, id=station_slot.id, values=vals)
                    slot_data.append(temp_dict)
            
        data['slots'] = slot_data
        fin_data = {
            'status': True,
            'message': 'Success',
            'data': data
        }
        update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
        return fin_data

def manage_slot_status(db: Session, station_id: int=0, slot_number: int=0, status: int=None):
    station_slot = get_station_slot(db=db, station_id=station_id, slot_number=slot_number)
    if station_slot is None:
        return {
            'status': False,
            'message': 'Slot not found',
        }
    else:
        if status is not None:
            update_station_battery(db=db, id=station_slot.id, values={'status': status})
        return {
            'status': True,
            'message': 'Success',
        }
    
def manage_slot_status_by_ce(db: Session, station_id: int=0, slot_number: int=0, status: int=None):
    station_slot = get_station_slot(db=db, station_id=station_id, slot_number=slot_number)
    if station_slot is None:
        return {
            'status': False,
            'message': 'Slot not found',
        }
    else:
        if status is not None:
            update_station_battery(db=db, id=station_slot.id, values={'status': status})
        return {
            'status': True,
            'message': 'Success',
        }