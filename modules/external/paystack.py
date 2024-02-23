import requests
import dateparser
import time
from datetime import datetime, timedelta
from settings.config import load_env_config

config = load_env_config()

def send_to_paystack(endpoint=None, data={}, request_type=1):
    url = config['paystack_url'] + str(endpoint)
    headers = {
        'Authorization': 'Bearer ' + str(config['paystack_secret_key']),
        'Content-Type': 'application/json',
    }
    if request_type == 1:
        response = requests.get(url=url, params=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    elif request_type == 2:
        response = requests.post(url=url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    else:
        return None
    

def verify_paystack_transaction(transaction_id: str=None):
    endpoint = "transaction/verify/" + str(transaction_id)
    data = {}
    return send_to_paystack(endpoint=endpoint, data=data, request_type=1)