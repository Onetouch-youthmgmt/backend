
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from auth.auth import get_hashed_password
from enums.user import UserRole
from models.karyakarta import Karyakarta

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def create_admin_user(db: Session):
    if not ADMIN_USERNAME or not ADMIN_PASSWORD:
        raise ValueError("ADMIN_USERNAME and ADMIN_PASSWORD must be set")
    
    existing_admin = db.query(Karyakarta).filter(Karyakarta.email == ADMIN_USERNAME).first()

    if not existing_admin:
        hashed_password = get_hashed_password(ADMIN_PASSWORD)
        admin = Karyakarta(email=ADMIN_USERNAME, hashed_password=hashed_password, role=UserRole.ADMIN.value)
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"Admin user {ADMIN_USERNAME} created successfully")
    else:
        print(f"Admin user {ADMIN_USERNAME} already exists")




