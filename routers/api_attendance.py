from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from services import attendance_service
from schemas.attendance_schema import AttendanceCreate
from database.database import get_db
from auth.auth_decorators import authorize
from enums.user import UserRole



router = APIRouter(
    prefix="/attendance",
    tags=["attendance"],
)


@router.get("/")
# @authorize([UserRole.ADMIN, UserRole.KARYAKARTA])
async def get_attendance(request: Request, db: Session = Depends(get_db)):
    return {"message": "Attendance created successfully"}
    
@router.post("/")
# @authorize([UserRole.ADMIN, UserRole.KARYAKARTA])
async def create_attendance(request: Request, attendance: AttendanceCreate, db: Session = Depends(get_db)):

    return attendance_service.create_or_update_attendance(attendance, db)