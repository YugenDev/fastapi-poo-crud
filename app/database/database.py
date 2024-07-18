from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mypassword@localhost/TiendaJPBB"

# Crear el motor de base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
