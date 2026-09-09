from fastapi import HTTPException
from schemas.youth_schema import YouthCreate
from database.database import supabase

YOUTH_SELECT_WITH_SABHA_CENTERS = "*, youth_sabha_center_association(sabha_centers(*))"

def _flatten_sabha_centers(youth: dict) -> dict:
    associations = youth.pop("youth_sabha_center_association", []) or []
    youth["sabha_centers"] = [assoc["sabha_centers"] for assoc in associations if assoc.get("sabha_centers")]
    return youth

def get_all_youths(sabha_center_id):
    try:
        association = supabase.table("youth_sabha_center_association").select("youth_id").eq("sabha_center_id", sabha_center_id).execute()
        youth_ids = [row["youth_id"] for row in association.data]
        if not youth_ids:
            return []

        youths_response = supabase.table("youths").select(YOUTH_SELECT_WITH_SABHA_CENTERS).eq("is_active", True).in_("id", youth_ids).execute()
        youths = [_flatten_sabha_centers(youth) for youth in youths_response.data]

        karyakarta_ids = {youth["karyakarta_id"] for youth in youths if youth.get("karyakarta_id")}
        karyakarta_names = {}
        if karyakarta_ids:
            karyakartas = supabase.table("youths").select("id, first_name, last_name").in_("id", list(karyakarta_ids)).execute()
            karyakarta_names = {k["id"]: f"{k['first_name']} {k['last_name']}" for k in karyakartas.data}

        for youth in youths:
            youth["karyakarta_name"] = karyakarta_names.get(youth.get("karyakarta_id"))

        return youths
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting youths: {str(e)}")

def get_youth_by_id(youth_id: int):
    try:
        response = supabase.table("youths").select(YOUTH_SELECT_WITH_SABHA_CENTERS).eq("id", youth_id).eq("is_active", True).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Youth not found")
        youth = _flatten_sabha_centers(response.data[0])

        if youth.get("karyakarta_id"):
            karyakarta = supabase.table("youths").select("first_name, last_name").eq("id", youth["karyakarta_id"]).execute()
            youth["karyakarta_name"] = f"{karyakarta.data[0]['first_name']} {karyakarta.data[0]['last_name']}" if karyakarta.data else None
        else:
            youth["karyakarta_name"] = None
        return youth
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting youth by id: {str(e)}")

def create_new_youth(youth: YouthCreate):
    try:
        sabha_center_ids = youth.sabha_center_ids
        sabha_centers = supabase.table("sabha_centers").select("id").in_("id", sabha_center_ids).execute()
        if not sabha_centers.data:
            raise HTTPException(status_code=404, detail=f"Invalid sabha center ids: {sabha_center_ids}")

        if youth.karyakarta_id is not None:
            karyakarta_youth = supabase.table("youths").select("id").eq("id", youth.karyakarta_id).execute()
            if not karyakarta_youth.data:
                raise HTTPException(status_code=404, detail="Karyakarta not found")

        response = supabase.table("youths").insert({
            "first_name": youth.first_name,
            "last_name": youth.last_name,
            "email": youth.email,
            "phone_number": youth.phone_number,
            "birth_date": youth.birth_date.isoformat(),
            "origin_city_india": youth.origin_city_india,
            "current_city_germany": youth.current_city_germany,
            "is_active": True,
            "is_karyakarta": youth.is_karyakarta,
            "karyakarta_id": youth.karyakarta_id,
            "educational_field": youth.educational_field,
            "address": youth.address,
            "pin_code": youth.pin_code,
        }).execute()
        new_youth = response.data[0]

        association_rows = [{"youth_id": new_youth["id"], "sabha_center_id": sc_id} for sc_id in sabha_center_ids]
        supabase.table("youth_sabha_center_association").insert(association_rows).execute()

        return {"message": f"Youth {youth.first_name} {youth.last_name} created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating new youth: {str(e)}")

def _delete_youth_cascade(youth_id: int):
    """Mirrors the previous SQLAlchemy `cascade="all, delete-orphan"` on managed_youths:
    deleting a karyakarta also deletes the youths they manage, recursively."""
    managed = supabase.table("youths").select("id").eq("karyakarta_id", youth_id).execute()
    for managed_youth in managed.data:
        _delete_youth_cascade(managed_youth["id"])
    supabase.table("youth_sabha_center_association").delete().eq("youth_id", youth_id).execute()
    supabase.table("youths").delete().eq("id", youth_id).execute()

def delete_youth_by_id(youth_id: int):
    try:
        youth = supabase.table("youths").select("first_name, last_name").eq("id", youth_id).execute()
        if not youth.data:
            raise HTTPException(status_code=404, detail="Youth not found")
        _delete_youth_cascade(youth_id)
        return {"message": f"Youth {youth.data[0]['first_name']} {youth.data[0]['last_name']} deleted permanently"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting youth: {str(e)}")

def update_youth_by_id(youth_id: int, youth: YouthCreate):
    try:
        if youth.karyakarta_id is not None:
            karyakarta_youth = supabase.table("youths").select("id").eq("id", youth.karyakarta_id).execute()
            if not karyakarta_youth.data:
                raise HTTPException(status_code=404, detail="Karyakarta not found")

        sabha_center_ids = youth.sabha_center_ids
        sabha_centers = supabase.table("sabha_centers").select("id").in_("id", sabha_center_ids).execute()
        if not sabha_centers.data:
            raise HTTPException(status_code=404, detail=f"Invalid sabha center ids: {sabha_center_ids}")

        youth_to_update = supabase.table("youths").select("id").eq("id", youth_id).execute()
        if not youth_to_update.data:
            raise HTTPException(status_code=404, detail="Youth to update not found")

        supabase.table("youths").update({
            "first_name": youth.first_name,
            "last_name": youth.last_name,
            "email": youth.email,
            "phone_number": youth.phone_number,
            "birth_date": youth.birth_date.isoformat(),
            "origin_city_india": youth.origin_city_india,
            "current_city_germany": youth.current_city_germany,
            "educational_field": youth.educational_field,
            "karyakarta_id": youth.karyakarta_id,
            "is_active": youth.is_active,
            "is_karyakarta": youth.is_karyakarta,
            "address": youth.address if youth.address else None,
            "pin_code": youth.pin_code if youth.pin_code else None,
        }).eq("id", youth_id).execute()

        # replace m2m sabha center links with the new set
        supabase.table("youth_sabha_center_association").delete().eq("youth_id", youth_id).execute()
        association_rows = [{"youth_id": youth_id, "sabha_center_id": sc_id} for sc_id in sabha_center_ids]
        supabase.table("youth_sabha_center_association").insert(association_rows).execute()

        return {"message": f"Youth {youth.first_name} {youth.last_name} updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating youth: {str(e)}")

def get_youths_by_karyakarta_id(karyakarta_id: int):
    try:
        karyakarta = supabase.table("youths").select("id").eq("id", karyakarta_id).execute()
        if not karyakarta.data:
            raise HTTPException(status_code=404, detail="Karyakarta not found")

        managed = supabase.table("youths").select("id, first_name, last_name, created_at").eq("karyakarta_id", karyakarta_id).execute()
        youths = [
            {"id": youth["id"], "name": f"{youth['first_name']} {youth['last_name']}", "created_date": youth["created_at"]}
            for youth in managed.data
        ]
        return youths
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting youths by karyakarta id: {str(e)}")
