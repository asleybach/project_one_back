from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import auth_router
from app.database.database import database, engine, Base
from app.models import user  
import subprocess
from app.finance.routes import finance_router

app = FastAPI()

origins = [
    "http://localhost:3000",  
    "http://127.0.0.1:3000",  
    "https://mi-dominio.com",  
    "http://localhost:8081",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.on_event("startup")
async def startup():
    subprocess.run(["alembic", "upgrade", "head"])
    await database.connect()
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown():
   await database.disconnect()

app.include_router(auth_router, prefix="/auth")
app.include_router(finance_router, prefix="/finance")