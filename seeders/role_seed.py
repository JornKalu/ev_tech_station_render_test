# from database.db import session
from sqlalchemy.orm import Session
from database.model import create_role, get_single_role_by_id

# db = session




def run_role_seeder(db: Session):
    role = create_role(db=db, name="Superadmin", description="Superadmin role", status=1, created_by=1)
    return get_single_role_by_id(db=db, id=role.id)
