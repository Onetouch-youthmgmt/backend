import os
from fastapi import Depends, HTTPException, Request
from clerk_backend_api import Clerk
from clerk_backend_api.security import authenticate_request
from clerk_backend_api.security.types import AuthenticateRequestOptions
from dotenv import load_dotenv

load_dotenv()


CLERK_API_KEY = os.getenv('CLERK_API_KEY')
print("CLERK_API_KEY:", CLERK_API_KEY)
CLERK_AUTHORIZED_PARTY = os.getenv("CLERK_AUTHORIZED_PARTY", "http://localhost:5173/")

def verify_jwt_token(request: Request):
    """
    Dependency to verify Clerk token from Authorization header or __session cookie.
    Returns request_state if signed in, else raises HTTPException 401.
    """
    sdk = Clerk(bearer_auth=CLERK_API_KEY)
    options = AuthenticateRequestOptions(
        authorized_parties=["http://localhost:5173/"],
        clock_skew_in_ms=60000  
    )
    request_state = sdk.authenticate_request(request, options)
    if not request_state.is_signed_in:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return request_state