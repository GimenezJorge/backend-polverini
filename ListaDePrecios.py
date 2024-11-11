from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, Session
from Editorial import Editorial
from Libro import Libro 
from database import Base, engine


class ListaDePrecios(Base):
    __tablename__ = 'listas_de_precios'

    id_lista_precio = Column(Integer, primary_key=True, autoincrement=True)
    id_editorial = Column(Integer, ForeignKey('editoriales.id_editorial'), nullable=False)
    id_libro = Column(Integer, ForeignKey('libros.id_libro'), nullable=False)
    precio = Column(Float, nullable=False)
    
    nombre_editorial = Column(String)  # Para el nombre de la editorial
    nombre_libro = Column(String)  # Para el nombre del libro

    editorial = relationship("Editorial", back_populates="listas_de_precios")
    libro = relationship("Libro", back_populates="listas_de_precios")

    @classmethod
    def crear_precio(cls, session: Session, id_editorial: int, id_libro: int, precio: float):
        editorial = session.query(Editorial).filter(Editorial.id_editorial == id_editorial).one_or_none()
        if not editorial:
            raise Exception(f"Editorial con id {id_editorial} no encontrada")

        libro = session.query(Libro).filter(Libro.id_libro == id_libro).one_or_none()
        if not libro:
            raise Exception(f"Libro con id {id_libro} no encontrado")

        nueva_lista_precio = cls(
            id_editorial=id_editorial,
            nombre_editorial=editorial.nombre,
            id_libro=id_libro,
            nombre_libro=libro.titulo,
            precio=precio
        )
        
        return nueva_lista_precio

    @classmethod
    def mostrar_todos(cls, session: Session):
        return session.query(cls).all()  # Devuelve todos los registros de precios
