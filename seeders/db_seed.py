from sqlalchemy.orm import Session
from seeders.admin_seed import run_admin_seeder
from seeders.role_seed import run_role_seeder
from seeders.user_seed import run_user_seeder

def seed(db: Session):
    print(run_admin_seeder(db=db))
    print(run_role_seeder(db=db))
    print(run_user_seeder(db=db))