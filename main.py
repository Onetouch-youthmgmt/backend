from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import register_routers
from scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()

app = FastAPI(
    title="OneTouch App",
    description="Youth management App",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [
    "http://localhost:5173",
    "https://backend-s8fi.onrender.com",
    "https://onetouchpro.app",
    "https://www.onetouchpro.app",
     "https://api.onetouchpro.app"
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
