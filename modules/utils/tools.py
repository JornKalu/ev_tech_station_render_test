import json
import string 
import random
from datetime import datetime
from typing import List, Dict
from settings.config import load_env_config
import dateparser
import time

config = load_env_config()

def rand_string_generator(size=10):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def rand_upper_string_generator(size=10):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))
    
def rand_lower_string_generator(size=10):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def generate_transaction_reference(tran_type: str = None, rand_type: int = 1, rand_size: int = 10):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    ts = int(ts)
    if rand_type == 1:
        return str(tran_type).upper() + "_" + rand_string_generator(size=rand_size) + "_" + str(ts)
    elif rand_type == 2:
        return str(tran_type).upper() + "_" + rand_upper_string_generator(size=rand_size) + "_" + str(ts)
    elif rand_type == 3:
        return str(tran_type).upper() + "_" + rand_lower_string_generator(size=rand_size) + "_" + str(ts)

def process_schema_dictionary(info: Dict={}):
    if bool(info) == False:
        return {}
    else:
        retval = {}
        for i in info:
            if info[i] != None:
                retval[i] = info[i]
        return retval
    

def is_json(jstr=None):
    if jstr != None:
        try:
            json_obj = json.loads(jstr)
            return True
        except ValueError as e: 
            return False
        return True
    else:
        return False

def json_loader(jstr=None):
    if is_json(jstr=jstr) == False:
        return None
    else:
        return json.loads(jstr)
    
def check_if_time_as_pass(time_str: str=None):
    if time_str is None:
        return False
    else:
        date_parsed = dateparser.parse(str(time_str), date_formats=['%d-%m-%Y %H:%M:%S'])
        time_tz = time.mktime(date_parsed.timetuple())
        time_tz = int(time_tz)
        current_tz = int(time.time())
        if current_tz >= time_tz:
            return True
        else:
            return False