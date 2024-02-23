from typing import Dict
import requests
import phonenumbers
import certifi
from io import BytesIO
from settings.config import load_env_config

config = load_env_config()

def get_ip_info(ip_address: str=None):
    url = "http://www.geoplugin.net/json.gp?ip=" + str(ip_address)
    req = requests.get(url=url)
    return req.json()

def process_phone_number(phone_number: str=None, country_code: str=None) -> Dict:
    try:
        x = phonenumbers.parse(phone_number, country_code)
        x = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        x = str(x).replace(" ", "")
        return {
            'status': True,
            'phone_number': x,
            'message': 'success'
        }
    except (phonenumbers.phonenumberutil.NumberParseException, Exception) as e:
        return {
            'status': False,
            'phone_number': None,
            'message': str(e)
        }


def check_phone_number_validity(phone_number: str=None, country_code: str=None):
    try:
        x = phonenumbers.parse(phone_number, country_code)
        return phonenumbers.is_possible_number(x)
    except (phonenumbers.phonenumberutil.NumberParseException, Exception) as e:
        return False
