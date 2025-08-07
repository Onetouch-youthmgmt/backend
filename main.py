from contextlib import asynccontextmanager
from auth.auth import verify_jwt_token
from database.database import Base, engine, get_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import register_routers
from fastapi import Depends


# Create the database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="OneTouch App",
    description="Youth management App",
    version="1.0.0",
    dependencies=[Depends(verify_jwt_token)]  # <-- Add your auth dependency here
)

origins = [
    "http://localhost:5173",
    "https://one-touch-frontend.vercel.app/",
    "https://www.onetouchpro.app/"
    ]

app.add_middleware(    
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

register_routers(app)

@app.get("/")
async def root():
    return {"message": "Hello World from OneTouch backend"}
