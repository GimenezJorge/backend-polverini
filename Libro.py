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

    @classmethod
    def modificar_libro(cls, id_libro: int, libro_in: LibroModel):
        session = sessionmaker(bind=engine)()
        libro = session.query(cls).filter(cls.id_libro == id_libro).one_or_none()

        if not libro:
            session.close()
            return False

        # Verifico que el género exista
        from Genero import Genero
        genero = session.query(Genero).filter(Genero.id_genero == libro_in.id_genero).one_or_none()
        if not genero:
            session.close()
            return "genero_invalido"

        libro.titulo = libro_in.titulo
        libro.autor = libro_in.autor
        libro.isbn = libro_in.isbn
        libro.stock = libro_in.stock
        libro.id_genero = libro_in.id_genero

        session.commit()
        session.close()
        return True


    @classmethod
    def eliminar_libro(cls, id_libro: int):
        session = sessionmaker(bind=engine)()
        libro = session.query(cls).filter(cls.id_libro == id_libro).one_or_none()

        if not libro:
            session.close()
            return False

        session.delete(libro)
        session.commit()
        session.close()
        return True

    @classmethod
    def obtener_por_genero(cls, id_genero: int):
        session = sessionmaker(bind=engine)()
        libros = session.query(cls).filter(cls.id_genero == id_genero).all()
        session.close()
        return libros

    @classmethod
    def obtener_por_nombre(cls, nombre: str):
        session = sessionmaker(bind=engine)()
        try:
            libros = (
                session.query(cls)
                .filter(cls.titulo.isnot(None))             # <-- evita NULL
                .filter(cls.titulo.ilike(f"%{nombre}%"))    # <-- busca coincidencia
                .all()
            )
            return libros
        finally:
            session.close()
