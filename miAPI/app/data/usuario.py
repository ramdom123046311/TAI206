from sqlalchemy import Column, Integer, String
from app.data.db import Base


class Usuario(Base):
    __tablename__ = "tb_usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    edad = Column(Integer)
    