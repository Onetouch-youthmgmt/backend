from fastapi import Depends, HTTPException, Request
from database.database import supabase
from enums.user import UserRole


def verify_jwt_token(request: Request):
    """
    Verify request with Supabase Auth; if signed-out, raise 401.
    """

    # Allow OPTIONS preflight requests to pass through without authentication
    if request.method == "OPTIONS":
        return {"user_id": None, "role": None}

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header[len("Bearer "):].strip()

    try:
        user_response = supabase.auth.get_user(token)
        user = user_response.user if user_response else None
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Extract role from app metadata (admin-only, set via Supabase Admin API/SQL)
        app_metadata = user.app_metadata or {}
        role = app_metadata.get("role", UserRole.KARYAKARTA.value)
        return {"user_id": user.id, "role": role}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

def require_admin(auth: dict = Depends(verify_jwt_token)):
    """
    Dependency to check if user is admin.
    """
    if auth["role"] != UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="Forbidden: Admin access required")
    return auth

def require_karyakarta(auth: dict = Depends(verify_jwt_token)):
    """
    Dependency to check if user is karyakarta or admin.
    """
    if auth["role"] not in [UserRole.ADMIN.value, UserRole.KARYAKARTA.value]:
        raise HTTPException(status_code=403, detail="Forbidden: Karyakarta access required")
    return auth
