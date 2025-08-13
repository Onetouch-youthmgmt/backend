import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request
from jose import jwt
from jwt import PyJWKClient
import requests



load_dotenv()
# ZITADEL_JWKS_URL = os.getenv("ZITADEL_JWKS_URL")
# ZITADEL_AUDIENCE = os.getenv("ZITADEL_AUDIENCE")
# ZITADEL_ISSUER = os.getenv("ZITADEL_ISSUER")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
ALGORITHMS = ["RS256"]

# Caceh for JWKS
jwks_client = PyJWKClient(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")


def verify_jwt_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = auth_header.split(" ")[1]
    
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=ALGORITHMS,
            audience=AUTH0_API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTClaimsError:
        raise HTTPException(status_code=401, detail="Invalid claims")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")