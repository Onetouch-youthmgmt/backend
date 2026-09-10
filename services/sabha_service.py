from schemas.sabha_schema import SabhaCreate
from fastapi import HTTPException
from database.database import supabase


def get_all_sabhas(sabha_center_id: int):
    try:
        response = supabase.table("sabhas").select("*").eq("sabha_center_id", sabha_center_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sabhas: {str(e)}")

def get_sabha_by_id(sabha_id: int):
    try:
        response = supabase.table("sabhas").select("*").eq("id", sabha_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Sabha not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sabha by id: {str(e)}")

def create_new_sabha(sabha: SabhaCreate):
    try:
        sabha_center = supabase.table("sabha_centers").select("id").eq("id", sabha.sabha_center_id).execute()
        if not sabha_center.data:
            raise HTTPException(status_code=404, detail="Sabha center not found")
        response = supabase.table("sabhas").insert({
            "topic": sabha.topic,
            "speaker_name": sabha.speaker_name,
            "date": sabha.date.isoformat(),
            "food": sabha.food,
            "sabha_center_id": sabha.sabha_center_id,
        }).execute()
        new_sabha = response.data[0]
        return {"sabha_id": new_sabha["id"], "message": f"Sabha with topic {sabha.topic} and for date {sabha.date} created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating sabha: {str(e)}")

def update_sabha_by_id(sabha_id: int, sabha: SabhaCreate):
    try:
        existing = supabase.table("sabhas").select("id").eq("id", sabha_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Sabha not found for update")
        sabha_center = supabase.table("sabha_centers").select("id").eq("id", sabha.sabha_center_id).execute()
        if not sabha_center.data:
            raise HTTPException(status_code=404, detail="Sabha center not found")
        supabase.table("sabhas").update({
            "topic": sabha.topic,
            "speaker_name": sabha.speaker_name,
            "date": sabha.date.isoformat(),
            "sabha_center_id": sabha.sabha_center_id,
            "food": sabha.food,
        }).eq("id", sabha_id).execute()
        return {"message": f"Sabha with topic {sabha.topic} and for date {sabha.date} updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating sabha: {str(e)}")

def delete_sabha_by_id(sabha_id: int):
    try:
        existing = supabase.table("sabhas").select("topic, date").eq("id", sabha_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Sabha not found for deletion")
        supabase.table("attendances").delete().eq("sabha_id", sabha_id).execute()
        supabase.table("sabhas").delete().eq("id", sabha_id).execute()
        return {"message": f"Sabha with topic {existing.data[0]['topic']} and for date {existing.data[0]['date']} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting sabha: {str(e)}")
