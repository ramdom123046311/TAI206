from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os 

# 1 definir la url de conexion 
DATABASE_URL= os.getenv("DATABASE_URL", "postgresql://admin:123456@postgres:5432/DB_miapi")

#2 Creamos el motor de conexion
engine = create_engine(DATABASE_URL)

#3 agregamos el gestor de sesiones
sesionLocal= sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind= engine
    )

#4 base declarativa para modelos.
Base= declarative_base()

#5 funcion de manejo de sesion en request
def get_db():
    db= sesionLocal()
    try:
        yield db
    finally:
        db.close()