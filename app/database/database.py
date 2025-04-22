from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from databases import Database
from app.config import settings

# Configuración de la base de datos
DATABASE_URL = settings.DATABASE_URL

# Configuración de SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configuración de databases (para consultas asíncronas)
database = Database(DATABASE_URL)