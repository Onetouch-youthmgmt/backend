from fastapi import HTTPException
from schemas.attendance_schema import AttendanceCreate
from database.database import supabase


def create_or_update_attendance(attendance: AttendanceCreate):
    try:
        sabha_response = supabase.table("sabhas").select("*, sabha_centers(city)").eq("id", attendance.sabha_id).execute()
        if not sabha_response.data:
            raise HTTPException(status_code=404, detail="Sabha not found")
        sabha = sabha_response.data[0]

        attendance_data = attendance.attendance_data
        youth_ids = [att.youth_id for att in attendance_data]

        existing_youths = supabase.table("youths").select("id").in_("id", youth_ids).execute()
        existing_youth_ids = {youth["id"] for youth in existing_youths.data}

        invalid_youth_ids = set(youth_ids) - existing_youth_ids
        if invalid_youth_ids:
            raise HTTPException(status_code=404, detail=f"Youth IDs not found: {', '.join(map(str, invalid_youth_ids))}")

        rows = [
            {
                "sabha_id": attendance.sabha_id,
                "youth_id": att_data.youth_id,
                "is_present": att_data.is_present,
            }
            for att_data in attendance_data
        ]
        supabase.table("attendances").upsert(rows, on_conflict="sabha_id,youth_id").execute()

        sabha_center_city = sabha["sabha_centers"]["city"] if sabha.get("sabha_centers") else ""
        return {"message": f"Attendance for {sabha_center_city} and {sabha['topic']} modified successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_attendance_by_sabha_id(sabha_id: int):
    try:
        sabha = supabase.table("sabhas").select("id").eq("id", sabha_id).execute()
        if not sabha.data:
            raise HTTPException(status_code=404, detail="Sabha not found")

        attendance = supabase.table("attendances").select("youth_id").eq("sabha_id", sabha_id).eq("is_present", True).execute()

        if not attendance.data:
            raise HTTPException(status_code=404, detail="Attendance not found for the given sabha_id")

        present_youths = [att["youth_id"] for att in attendance.data]
        return {"present_youth_ids": present_youths}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
