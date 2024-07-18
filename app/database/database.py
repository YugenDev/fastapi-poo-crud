from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mypassword@db/TiendaJPBB"

# Crear el motor de base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1
        print("Conexión exitosa a la base de datos!")
except Exception as e:
    print(f"Error al conectar a la base de datos: {str(e)}")
