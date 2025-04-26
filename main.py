from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import auth_router
from app.database.database import database, engine, Base
from app.models import user  

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3000",  # React o cualquier frontend local
    "http://127.0.0.1:3000",  # Otra posible configuración local
    "https://mi-dominio.com",  # Dominio de producción


    "http://localhost:8081",  # React nativate
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir estos orígenes
    allow_credentials=True,  # Permitir el envío de cookies o credenciales
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

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