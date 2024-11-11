from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String
from database import engine, Base

# Defino la clase Genero
class Genero(Base):
    __tablename__ = 'generos'

    id_genero = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    
    # Relación con la tabla de libros
    libros = relationship("Libro", back_populates="genero")

    @classmethod
    def agregar_genero(cls, nombre: str):
        nuevo_genero = cls(nombre=nombre)
        session = sessionmaker(bind=engine)()
        session.add(nuevo_genero)
        session.commit()
        session.refresh(nuevo_genero)
        session.close()
        return nuevo_genero

    @classmethod
    def obtener_todos(cls):
        session = sessionmaker(bind=engine)()
        generos = session.query(cls).all()
        session.close()
        return generos
