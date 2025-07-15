from models.sabha_center import SabhaCenter
from schemas.sabha_schema import SabhaCreate, SabhaResponse
from models.sabha import Sabha
from fastapi import HTTPException
from sqlalchemy.orm import Session

def get_all_sabhas(sabha_center_id:int, db:Session):
    try:
        sabhas = db.query(Sabha).filter(Sabha.sabha_center_id == sabha_center_id).all()
        return sabhas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sabhas: {str(e)}")

def get_sabha_by_id(sabha_id:int, db:Session):
    try:
        sabha = db.query(Sabha).filter(Sabha.id == sabha_id).first()
        if not sabha:
            raise HTTPException(status_code=404, detail="Sabha not found")
        return sabha
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sabha by id: {str(e)}")

def create_new_sabha(sabha:SabhaCreate, db:Session):
    try:
        sabha_center = db.query(SabhaCenter).filter(SabhaCenter.id == sabha.sabha_center_id).first()
        if not sabha_center:
            raise HTTPException(status_code=404, detail="Sabha center not found")
        new_sabha = Sabha(
            topic = sabha.topic,
            speaker_name = sabha.speaker_name,
            date = sabha.date,
            food = sabha.food,
            sabha_center_id = sabha.sabha_center_id)  
        db.add(new_sabha)
        db.commit()
        db.refresh(new_sabha)
        return {"sabha_id": new_sabha.id, "message": f"Sabha with topic {sabha.topic} and for date {sabha.date} created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating sabha: {str(e)}")

def update_sabha_by_id(sabha_id:int, sabha:SabhaCreate, db:Session):
    try:
        sabha_to_update = db.query(Sabha).filter(Sabha.id == sabha_id).first()
        if not sabha_to_update:
            raise HTTPException(status_code=404, detail="Sabha not found for update")
        sabha_center = db.query(SabhaCenter).filter(SabhaCenter.id == sabha.sabha_center_id).first()
        if not sabha_center:
            raise HTTPException(status_code=404, detail="Sabha center not found")
        sabha_to_update.topic = sabha.topic
        sabha_to_update.speaker_name = sabha.speaker_name
        sabha_to_update.date = sabha.date
        sabha_to_update.sabha_center_id = sabha.sabha_center_id
        sabha_to_update.food = sabha.food
        db.commit()
        db.refresh(sabha_to_update)
        return {"message": f"Sabha with topic {sabha.topic} and for date {sabha.date} updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating sabha: {str(e)}")

def delete_sabha_by_id(sabha_id:int, db:Session):
    try:
        sabha_to_delete = db.query(Sabha).filter(Sabha.id == sabha_id).first()
        if not sabha_to_delete:
            raise HTTPException(status_code=404, detail="Sabha not found for deletion")
        db.delete(sabha_to_delete)
        db.commit()
        return {"message": f"Sabha with topic {sabha_to_delete.topic} and for date {sabha_to_delete.date} deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting sabha: {str(e)}")