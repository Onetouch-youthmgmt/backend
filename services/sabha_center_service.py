from schemas.sabha_center_schema import SabhaCenterCreate
from fastapi import HTTPException
from database.database import supabase


def get_all_sabha_centers():
    try:
        response = supabase.table("sabha_centers").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sabha centers: {str(e)}")

def get_sabha_center_by_id(sabha_center_id: int):
    try:
        response = supabase.table("sabha_centers").select("*").eq("id", sabha_center_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Sabha center not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sabha center by id: {str(e)}")

def create_new_sabha_center(sabha_center: SabhaCenterCreate):
    try:
        supabase.table("sabha_centers").insert({
            "city": sabha_center.city,
            "address": sabha_center.address,
            "responsible_person": sabha_center.responsible_person,
            "contact_number": sabha_center.contact_number,
            "name": sabha_center.name,
        }).execute()
        return {"message": f"Sabha center in {sabha_center.city} created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating sabha center: {str(e)}")

def update_sabha_center_by_id(sabha_center_id: int, sabha_center: SabhaCenterCreate):
    try:
        existing = supabase.table("sabha_centers").select("id").eq("id", sabha_center_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Sabha center not found for update")
        supabase.table("sabha_centers").update({
            "city": sabha_center.city,
            "address": sabha_center.address,
            "responsible_person": sabha_center.responsible_person,
            "contact_number": sabha_center.contact_number,
            "name": sabha_center.name,
        }).eq("id", sabha_center_id).execute()
        return {"message": f"Sabha center in {sabha_center.city} updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating sabha center: {str(e)}")

def delete_sabha_center_by_id(sabha_center_id: int):
    try:
        existing = supabase.table("sabha_centers").select("city").eq("id", sabha_center_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Sabha center not found for deletion")
        supabase.table("sabha_centers").delete().eq("id", sabha_center_id).execute()
        return {"message": f"Sabha center in {existing.data[0]['city']} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting sabha center: {str(e)}")
