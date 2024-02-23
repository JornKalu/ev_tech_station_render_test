# from database.db import session
from sqlalchemy.orm import Session
from modules.authentication.auth import auth, create_admin, get_single_role_by_id

# db = session

def run_admin_seeder(db: Session):
    password = "secret"
    hashed_password = auth.get_password_hash(password=password)

    admin = create_admin(db=db, role_id=1, email="superadmin@u.com", phone_number="+2348178666383", username="superadmin", password=hashed_password, status=1, created_by=1)
    data = {
        'id': admin.id,
        'username': admin.username,
        'phone_number': admin.phone_number,
        'email': admin.email,
        'first_name': admin.first_name,
        'other_name': admin.other_name,
        'last_name': admin.last_name,
        'address': admin.address,
        'gender': admin.gender,
        'avatar': admin.avatar,
        'role': get_single_role_by_id(db=db, id=admin.role_id)
    }
    return data
