import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from dotenv import load_dotenv
from fastapi import Depends
from typing import Annotated

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

# For render DB
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=5,pool_timeout=60, pool_recycle=1800)
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbSession = Annotated[Session, Depends(get_db)]