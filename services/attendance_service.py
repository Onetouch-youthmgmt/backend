from fastapi import HTTPException
from models.attendance import Attendance
from models.youth import Youth
from models.sabha import Sabha
from schemas.attendance_schema import AttendanceCreate
from sqlalchemy.orm import Session



def create_or_update_attendance(attendance: AttendanceCreate, db: Session):

    sabha = db.query(Sabha).filter(Sabha.id == attendance.sabha_id).first()
    if not sabha:
        raise HTTPException(status_code=404, detail="Sabha not found")
    
    try:
        attendance_data = attendance.attendance_data

        # create a list of youth_ids
        youth_ids = [att.youth_id for att in attendance_data] 

        # validating wether youth ids are present in the youth table
        existing_youths = db.query(Youth).filter(Youth.id.in_(youth_ids)).all()
        existing_youths_ids = {youth.id for youth in existing_youths}

        # youth ids that are not present in the youth table for the given sent ids
        invalid_youth_ids = set(youth_ids) - existing_youths_ids
        if invalid_youth_ids:
            raise HTTPException(status_code=404, detail=f"Youth IDs not found: {', '.join(map(str, invalid_youth_ids))}")


        # fetch existing attendance for the youth ids
        existing_attendance = db.query(Attendance).filter(
            Attendance.youth_id.in_(youth_ids),
            Attendance.sabha_id == sabha.id
        ).all()

        existing_attendance_map = {att.youth_id: att for att in existing_attendance}
        result = []

        for att_data in attendance_data:
            if att_data.youth_id in existing_attendance_map:
                # update the attendance
                existing_record = existing_attendance_map[att_data.youth_id]
                existing_record.is_present = att_data.is_present
                result.append(existing_record)
            else:
                # create a new attendance
                new_attendance = Attendance(
                    sabha_id = sabha.id,
                    youth_id = att_data.youth_id,
                    is_present = att_data.is_present
                )
                db.add(new_attendance)
                result.append(new_attendance)

        db.commit()

        return {"message": f"Attendance for {sabha.sabha_center.city} and {sabha.topic} created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

        




