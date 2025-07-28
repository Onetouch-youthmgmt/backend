import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request
from jose import jwt
import requests



load_dotenv()
ZITADEL_JWKS_URL = os.getenv("ZITADEL_JWKS_URL")
ZITADEL_AUDIENCE = os.getenv("ZITADEL_AUDIENCE")
ZITADEL_ISSUER = os.getenv("ZITADEL_ISSUER")


def get_jwks():
    response = requests.get(ZITADEL_JWKS_URL)
    response.raise_for_status()
    return response.json()


def verify_jwt_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = auth_header.split(" ")[1]
    jwks = get_jwks()
    
    try:
        payload = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            audience=ZITADEL_AUDIENCE,
            issuer=ZITADEL_ISSUER,
            options={"verify_at_hash": False}  # Add this line to disable at_hash verification
        )
        return payload
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e