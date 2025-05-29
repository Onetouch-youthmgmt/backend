from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from sqlalchemy import text

router = APIRouter(
    prefix="/health",
    tags=["health"],
)

@router.get("/")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Execute a simple query to check database connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}