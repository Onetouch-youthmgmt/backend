from sqlalchemy.orm import Session
from auth.auth import get_hashed_password
from enums.user import UserRole
from database.database import get_db
from schemas.karyakarta_schema import KaryakartaCreateSchema
from models.karyakarta import Karyakarta
from fastapi import APIRouter, HTTPException, Request
from fastapi import Depends
from passlib.context import CryptContext
from auth.auth_decorators import authorize
import re
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

@router.post("/create-user")
# @authorize([UserRole.ADMIN])
async def create_karyakarta( request:Request,user: KaryakartaCreateSchema, db: Session = Depends(get_db)):

    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    existing_user = db.query(Karyakarta).filter(Karyakarta.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    if user.role not in [UserRole.ADMIN.value, UserRole.KARYAKARTA.value]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    
    new_user= Karyakarta(email=user.email, hashed_password = get_hashed_password(user.hashed_password), role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User {new_user.email} created successfully"}


    

