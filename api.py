from fastapi import FastAPI
from routers import api_youth_router, api_sabha_center_router, api_sabha_router, api_attendance_router , api_health_router

def register_routers(app: FastAPI):
    app.include_router(api_youth_router, prefix="/api", tags=["youths"])
    app.include_router(api_sabha_center_router, prefix="/api", tags=["sabha_centers"])
    app.include_router(api_sabha_router, prefix="/api", tags=["sabhas"])
    app.include_router(api_attendance_router, prefix="/api", tags=["attendance"])
    app.include_router(api_health_router, prefix="/api", tags=["health"])