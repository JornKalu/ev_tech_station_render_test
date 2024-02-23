# from database.db import session
from sqlalchemy.orm import Session
from modules.authentication.auth import auth, create_user_with_other_rows, get_profile_by_user_id, get_single_setting_by_user_id, get_wallet_by_user_id

# db = session



def run_user_seeder(db: Session):
    password = "secret"
    hashed_password = auth.get_password_hash(password=password)

    user = create_user_with_other_rows(db=db, phone_number="+2348178666383", email="test@u.com", password=hashed_password, username="test_user", device_name="test_device", imei="12383474848", mac_address="1635347647", fbt="test_token")
    profile = get_profile_by_user_id(db=db, user_id=user.id)
    setting = get_single_setting_by_user_id(db=db, user_id=user.id)
    wallet = get_wallet_by_user_id(db=db, user_id=user.id)
    data = {
        'id': user.id,
        'username': user.username,
        'phone_number': user.phone_number,
        'email': user.email,
        'profile': profile,
        'setting': setting,
        'wallet': wallet,
    }
    return data