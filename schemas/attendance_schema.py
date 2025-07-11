from pydantic import BaseModel


class AttendanceBase(BaseModel):
    sabha_id: int
    youth_id: int
    is_present: bool

class AttendanceData(BaseModel):
    youth_id: int
    is_present: bool

class AttendanceCreate(BaseModel):
    sabha_id: int
    attendance_data: list[AttendanceData]


class AttendanceResponse(AttendanceBase):
    id: int
    
    class ConfigDict:
        from_attributes = True

class AttendanceBySabhaListResponse(BaseModel):
    present_youth_ids: list[int]

    class ConfigDict:
        from_attributes = True
