from fastapi import APIRouter, Request, Depends
from auth.auth import verify_jwt_token
from services import attendance_service
from schemas.attendance_schema import AttendanceBySabhaListResponse, AttendanceCreate

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"],
     dependencies=[Depends(verify_jwt_token)],
)


@router.get("/")
async def get_attendance(request: Request):
    return {"message": "Get request Attendance successfully"}

@router.get("/{sabha_id}")
async def get_attendance_by_sabha(request: Request, sabha_id: int)->AttendanceBySabhaListResponse:
    """
    Get attendance by sabha_id
    Args
    request: FastAPI Request object
    sabha_id: ID of the sabha to get attendance for
    Returns:
    :return: List of youth id for the specified sabha_id
    """
    return attendance_service.get_attendance_by_sabha_id(sabha_id)

@router.post("/")
async def create_attendance(request: Request, attendance: AttendanceCreate):

    return attendance_service.create_or_update_attendance(attendance)
