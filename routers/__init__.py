from .api_youth import router as api_youth_router
from .api_auth import router as api_auth_router
from .api_admin import router as api_admin_router
from .api_sabha_center import router as api_sabha_center_router     
from .api_sabha import router as api_sabha_router
from .api_attendance import router as api_attendance_router
__all__ = ["api_youth_router", "api_auth_router", "api_admin_router", "api_sabha_center_router", "api_sabha_router", "api_attendance_router"]