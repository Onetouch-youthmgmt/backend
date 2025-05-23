from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
import dotenv

dotenv.load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY_FOR_TOKEN = os.getenv("SECRET_KEY_FOR_TOKEN")
ALGORITHM_FOR_TOKEN = os.getenv("ALGORITHM_FOR_TOKEN")


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires_delta})
    return jwt.encode(to_encode, SECRET_KEY_FOR_TOKEN, algorithm=ALGORITHM_FOR_TOKEN)   