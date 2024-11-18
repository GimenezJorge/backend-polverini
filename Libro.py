from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from database import engine, Base
from models import LibroModel
from Genero import Genero
from fastapi import HTTPException

class Libro(Base):
    __tablename__ = 'libros'

    id_libro = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255))
    autor = Column(String(100))
    isbn = Column(String(20), unique=True)
    stock = Column(Integer)
    id_genero = Column(Integer, ForeignKey('generos.id_genero'))

    # Relación con la tabla Genero
    genero = relationship("Genero", back_populates="libros")
    lista_de_precios = relationship("ListaDePrecios", back_populates="libro")
    
    @classmethod
    def agregar_libro(cls, libro_in: LibroModel):
        session = sessionmaker(bind=engine)()
        genero_existente = session.query(Genero).filter(Genero.id_genero == libro_in.id_genero).one_or_none()
        if not genero_existente:
            session.close()            
            raise HTTPException(status_code=400, detail=f"El género con id {libro_in.id_genero} no existe.")
        
        nuevo_libro = cls(
            titulo=libro_in.titulo,
            autor=libro_in.autor,
            isbn=libro_in.isbn,
            stock=libro_in.stock,
            id_genero=libro_in.id_genero
        )
         
        
        
        session.add(nuevo_libro)
        session.commit()
        session.refresh(nuevo_libro)
        session.close()
        return nuevo_libro

    @classmethod
    def mostrar_todos(cls):
        session = sessionmaker(bind=engine)()
        libros = session.query(cls).all()
        session.close()
        return libros
