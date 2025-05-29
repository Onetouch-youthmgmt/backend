

from schemas.sabha_center_schema import SabhaCenterCreate, SabhaCenterResponse
from models.sabha_center import SabhaCenter
from fastapi import HTTPException
from sqlalchemy.orm import Session


def get_all_sabha_centers(db:Session):
    try:
        sabha_centers = db.query(SabhaCenter).all()
        return sabha_centers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sabha centers: {str(e)}")

def get_sabha_center_by_id(sabha_center_id: int, db:Session):
    try:
        sabha_center = db.query(SabhaCenter).filter(SabhaCenter.id == sabha_center_id).first()
        if not sabha_center:
            raise HTTPException(status_code=404, detail="Sabha center not found")
        return sabha_center
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sabha center by id: {str(e)}")
        
def create_new_sabha_center(sabha_center: SabhaCenterCreate, db:Session):
    try:
        new_sabha_center = SabhaCenter(
            city = sabha_center.city,
            address = sabha_center.address,
            responsible_person = sabha_center.responsible_person,
            contact_number = sabha_center.contact_number,
            name = sabha_center.name
        )   
        db.add(new_sabha_center)
        db.commit()
        db.refresh(new_sabha_center)
        return {"message": f"Sabha center in {sabha_center.city} created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating sabha center: {str(e)}")

def update_sabha_center_by_id(sabha_center_id: int, sabha_center: SabhaCenterCreate, db:Session):
    try:
        sabha_center_to_update = db.query(SabhaCenter).filter(SabhaCenter.id == sabha_center_id).first()
        if not sabha_center_to_update:
            raise HTTPException(status_code=404, detail="Sabha center not found for update")
        sabha_center_to_update.city = sabha_center.city
        sabha_center_to_update.address = sabha_center.address
        sabha_center_to_update.responsible_person = sabha_center.responsible_person
        sabha_center_to_update.contact_number = sabha_center.contact_number
        sabha_center_to_update.name = sabha_center.name
        db.commit()
        db.refresh(sabha_center_to_update)
        return {"message": f"Sabha center in {sabha_center.city} updated successfully"} 
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating sabha center: {str(e)}")

def delete_sabha_center_by_id(sabha_center_id: int, db:Session):
    try:
        sabha_center_to_delete = db.query(SabhaCenter).filter(SabhaCenter.id == sabha_center_id).first()
        if not sabha_center_to_delete:
            raise HTTPException(status_code=404, detail="Sabha center not found for deletion")
        db.delete(sabha_center_to_delete)
        db.commit()
        return {"message": f"Sabha center in {sabha_center_to_delete.city} deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting sabha center: {str(e)}")
