from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from database import engine, Base

class Libro(Base):
    __tablename__ = 'libros'

    id_libro = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    autor = Column(String(100), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    id_genero = Column(Integer, ForeignKey('generos.id_genero'), nullable=False)

    # Relación con la tabla Genero
    genero = relationship("Genero", back_populates="libros")
    listas_de_precios = relationship("ListaDePrecios", back_populates="libro")
    
    @classmethod
    def agregar_libro(cls, titulo: str, autor: str, isbn: str, precio: float, stock: int, id_genero: int):
        nuevo_libro = cls(titulo=titulo, autor=autor, isbn=isbn, precio=precio, stock=stock, id_genero=id_genero)
        session = sessionmaker(bind=engine)()
        session.add(nuevo_libro)
        session.commit()
        session.refresh(nuevo_libro)
        session.close()
        return nuevo_libro

    @classmethod
    def obtener_libros(cls):
        session = sessionmaker(bind=engine)()
        libros = session.query(cls).all()
        session.close()
        return libros
