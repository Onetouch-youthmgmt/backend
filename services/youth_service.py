from models.sabha_center import SabhaCenter
from models.youth import Youth
from fastapi import  HTTPException
from sqlalchemy.orm import Session
from schemas.youth_schema import YouthCreate
from services.utility import sqlalchemy_to_pydantic_dict

def get_all_youths(sabha_center_id, db:Session):
    try:
        youths = db.query(Youth).filter(Youth.is_active == True, Youth.sabha_centers.any(SabhaCenter.id == sabha_center_id)).all()

        youth_with_karyakarta_info = []
        for youth in youths:
            youth_dict = sqlalchemy_to_pydantic_dict(youth)
            
            # Add karyakarta information
            if youth.karyakarta_id:
                followup_karyakarta = db.query(Youth).filter(Youth.id == youth.karyakarta_id).first()
                youth_dict['karyakarta_name'] = f"{followup_karyakarta.first_name} {followup_karyakarta.last_name}" if followup_karyakarta else None
            else:
                youth_dict['karyakarta_name'] = None
                
            youth_with_karyakarta_info.append(youth_dict)
            
        return youth_with_karyakarta_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting youths: {str(e)}")
    
def get_youth_by_id(youth_id: int, db:Session):
    try:
        youth = db.query(Youth).filter(Youth.id == youth_id).filter(Youth.is_active == True).first()
        if not youth:
            raise HTTPException(status_code=404, detail="Youth not found")
        youth_dict = sqlalchemy_to_pydantic_dict(youth)
        # Add karyakarta information
        if youth.karyakarta_id: 
            followup_karyakarta = db.query(Youth).filter(Youth.id == youth.karyakarta_id).first()
            youth_dict['karyakarta_name'] = f"{followup_karyakarta.first_name} {followup_karyakarta.last_name}" if followup_karyakarta else None
        else:
            youth_dict['karyakarta_name'] = None
        return youth_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting youth by id: {str(e)}")

def create_new_youth(youth: YouthCreate, db:Session):
   

   try:
        ## check sabha center ids are valid
        sabha_center_ids = youth.sabha_center_ids
        sabha_centers = db.query(SabhaCenter).filter(SabhaCenter.id.in_(sabha_center_ids)).all()
        if not sabha_centers:
            raise HTTPException(status_code=404, detail=f"Invalid sabha center ids: {sabha_center_ids}")
   
        ## check if provided karyakarta_id is valid
        if youth.karyakarta_id is not None:
            karyakarta_youth = db.query(Youth).filter(Youth.id == youth.karyakarta_id).first()
            if not karyakarta_youth:
                raise HTTPException(status_code=404, detail="Karyakarta not found")
        new_youth = Youth(
            first_name = youth.first_name,
            last_name = youth.last_name,
            email = youth.email,
            phone_number = youth.phone_number,
            birth_date = youth.birth_date,
            origin_city_india = youth.origin_city_india,
            current_city_germany = youth.current_city_germany,  
            is_active = True,
            is_karyakarta = youth.is_karyakarta,
            karyakarta_id = youth.karyakarta_id,
            educational_field = youth.educational_field,
            address = youth.address,
            pin_code = youth.pin_code,
        )

        ## add mtom relationship
        new_youth.sabha_centers=sabha_centers

        db.add(new_youth)
        db.commit()
        db.refresh(new_youth)
        return {"message": f"Youth {youth.first_name} {youth.last_name} created successfully"}
   
   except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating new youth: {str(e)}")
   
def delete_youth_by_id(youth_id: int, db:Session):
    try:
        youth = db.query(Youth).filter(Youth.id == youth_id).first()
        if not youth:
            raise HTTPException(status_code=404, detail="Youth not found")
        db.delete(youth)
        db.commit()
        return {"message": f"Youth {youth.first_name} {youth.last_name  } deleted permanently"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting youth: {str(e)}")
 
def update_youth_by_id(youth_id: int, youth: YouthCreate, db:Session):

    try:
        if youth.karyakarta_id is not None:
            karyakarta_youth = db.query(Youth).filter(Youth.id == youth.karyakarta_id).first()
        if not karyakarta_youth:
            raise HTTPException(status_code=404, detail="Karyakarta not found")
        sabha_center_ids = youth.sabha_center_ids
        sabha_centers = db.query(SabhaCenter).filter(SabhaCenter.id.in_(sabha_center_ids)).all()
        if not sabha_centers:
            raise HTTPException(status_code=404, detail=f"Invalid sabha center ids: {sabha_center_ids}")
        youth_to_update = db.query(Youth).filter(Youth.id == youth_id).first()
        if not youth_to_update:
            raise HTTPException(status_code=404, detail="Youth to update not found")
        youth_to_update.first_name = youth.first_name
        youth_to_update.last_name = youth.last_name
        youth_to_update.email = youth.email
        youth_to_update.phone_number = youth.phone_number
        youth_to_update.birth_date = youth.birth_date
        youth_to_update.origin_city_india = youth.origin_city_india
        youth_to_update.current_city_germany = youth.current_city_germany
        youth_to_update.educational_field = youth.educational_field
        youth_to_update.karyakarta_id = youth.karyakarta_id
        youth_to_update.is_active = youth.is_active
        youth_to_update.is_karyakarta = youth.is_karyakarta
        youth_to_update.address = youth.address | None
        youth_to_update.pin_code = youth.pin_code

        ## add mtom relationship
        ## it will remove old sabha centers and add new ones
        youth_to_update.sabha_centers=sabha_centers

        db.commit()
        db.refresh(youth_to_update)
        return {"message": f"Youth {youth_to_update.first_name} {youth_to_update.last_name} updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating youth: {str(e)}")
    
def get_youths_by_karyakarta_id(karyakarta_id: int, db: Session):

    try:
        karyakarta = db.query(Youth).filter(Youth.id == karyakarta_id).first()
        if not karyakarta:
            raise HTTPException(status_code=404, detail="Karyakarta not found")
        youths = [{"id": youth.id, "name": f"{youth.first_name} {youth.last_name}", "created_date": youth.created_at } for youth in karyakarta.managed_youths]
        return youths
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting youths by karyakarta id: {str(e)}")
