from fastapi import FastAPI
from app.auth.routes import auth_router
from app.database.database import database, engine, Base
from app.models import user  

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Conectar a la base de datos
    await database.connect()
    # Crear las tablas definidas en los modelos
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown():
    # Desconectar de la base de datos
    await database.disconnect()

app.include_router(auth_router, prefix="/auth")