from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request
from database.database import get_db
from auth.auth import ALGORITHM_FOR_TOKEN, SECRET_KEY_FOR_TOKEN
from jose import jwt, JWTError
from models.karyakarta import Karyakarta
from functools import wraps
from fastapi.security import HTTPBearer


security = HTTPBearer()

def authorize(roles: list[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):

            if not request:
                raise HTTPException(status_code=401, detail="request object not found")

            #extract token from request
            credentials = await security(request)
            token = credentials.credentials
            
            try:
                payload = jwt.decode(token, SECRET_KEY_FOR_TOKEN, algorithms=[ALGORITHM_FOR_TOKEN])
                username = payload.get("sub")
                role = payload.get("role")

                if not username or not role:
                    raise HTTPException(status_code=401, detail="Invalid token")
                if role not in [role.value for role in roles]:
                    raise HTTPException(status_code=403, detail="Not authorized")
                
                return await func(request, *args, **kwargs)
            except JWTError:
                raise HTTPException(status_code=401, detail="Invalid token")
        return wrapper
    return decorator




