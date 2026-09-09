from fastapi import APIRouter
from database.database import supabase

router = APIRouter(
    prefix="/health",
    tags=["health"],
)

@router.get("/")
async def health_check():
    try:
        supabase.table("sabha_centers").select("id").limit(1).execute()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
