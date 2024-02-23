import os
from typing import Any
from datetime import datetime
from sqlalchemy.orm import Session
from database.model import create_request_log
from settings.config import load_env_config

config = load_env_config()

def store_post_request_data(db: Session, data: Any):
    if isinstance(data, bytes):
        data = data.decode()
    create_request_log(db=db, server_type="test", name="post", value=str(data))
    return {
        'status': True,
        'data': str(data),
    }

def store_get_request_data(db: Session, data: Any):
    if isinstance(data, bytes):
        data = data.decode()
    create_request_log(db=db, name="get", value=str(data))
    return {
        'status': True,
        'data': str(data),
    }

    