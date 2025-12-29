import os
import json
from fastapi import Depends, HTTPException, Request
from clerk_backend_api import Clerk
from clerk_backend_api.security.types import AuthenticateRequestOptions
from dotenv import load_dotenv
import logging

from enums.user import UserRole


load_dotenv()

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_JWT_KEY = os.getenv("CLERK_JWT_KEY")
CLERK_AUTHORIZED_PARTY = os.getenv("CLERK_AUTHORIZED_PARTY", "")

auth_parties = [party.strip() for party in CLERK_AUTHORIZED_PARTY.split(",") if party.strip()] if CLERK_AUTHORIZED_PARTY else []


if not CLERK_SECRET_KEY:
        raise HTTPException(status_code=500, detail="CLERK_API_KEY not configured")
clerk_sdk = Clerk(bearer_auth=CLERK_SECRET_KEY)

def verify_jwt_token(request: Request):
    """
    Verify request with Clerk SDK; if signed-out, include debug info and
    """

    # Allow OPTIONS preflight requests to pass through without authentication
    if request.method == "OPTIONS":
        return {"user_id": None, "role": None}  # ← Fixed the syntax error here
    try:
        options = AuthenticateRequestOptions(
        # authorized_parties=auth_parties,
        jwt_key=CLERK_JWT_KEY,
    )
        request_state = clerk_sdk.authenticate_request(request, options)
        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Unauthorized")
        user_id = request_state.payload.get("sub")

        # Extract role from public metadata
        public_metadata = request_state.payload.get("public_metadata", {})
        role = public_metadata.get("role", UserRole.KARYAKARTA.value)
        return {"user_id": user_id, "role": role}
    except Exception as e:
        logging.debug("Clerk auth exception: %s", str(e))
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