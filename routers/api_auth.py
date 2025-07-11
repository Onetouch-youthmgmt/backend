from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.auth import create_access_token, verify_password
from auth.auth_decorators import authorize
from enums.user import UserRole
from database.database import get_db

router = APIRouter(
    prefix="/token",
    tags=["token"],
)



# @router.post("/")
# # @authorize([UserRole.ADMIN, UserRole.KARYAKARTA])
# def login(form_data:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(Karyakarta).filter(Karyakarta.email == form_data.username).first()

#     # unhash password and check that it matches
#     is_password_correct = verify_password(form_data.password, user.hashed_password)
#     if not user or not is_password_correct:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
    
#     token = create_access_token(data = {"sub": user.email, "role": user.role})
    
#     return {"access_token": token, "token_type": "Bearer"}