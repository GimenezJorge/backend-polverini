from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import  sessionmaker, relationship
from Editorial import Editorial
from Libro import Libro 
from database import engine, Base
from models import ListaDePreciosModel
from fastapi import HTTPException

class ListaDePrecios(Base):
    __tablename__ = 'lista_de_precios'
    id_lista_precio = Column(Integer, primary_key=True, autoincrement=True)
    id_editorial = Column(Integer, ForeignKey('editoriales.id_editorial'))    
    id_libro = Column(Integer, ForeignKey('libros.id_libro'))    
    precio = Column(Float)
    editorial = relationship("Editorial", back_populates="lista_de_precios")
    libro = relationship("Libro", back_populates="lista_de_precios")

    @classmethod
    def agregar_libro_a_lista_precios(cls, lista_precios_in: ListaDePreciosModel):
        session = sessionmaker(bind=engine)()
        editorial_existente = session.query(Editorial).filter(Editorial.id_editorial == lista_precios_in.id_editorial).one_or_none()
        if not editorial_existente:
            session.close()            
            raise HTTPException(status_code=400, detail=f"La editorial con id {lista_precios_in.id_editorial} no existe.")

        libro_existente = session.query(Libro).filter(Libro.id_libro == lista_precios_in.id_libro).one_or_none()
        if not libro_existente:
            session.close()            
            raise HTTPException(status_code=400, detail=f"El libro con id {lista_precios_in.id_libro} no existe.")

        nueva_lista_precio = cls(
            id_editorial=lista_precios_in.id_editorial,
            id_libro=lista_precios_in.id_libro,
            precio=lista_precios_in.precio
        )
        
        session.add(nueva_lista_precio)
        session.commit()
        session.refresh(nueva_lista_precio)
        session.close()
        return nueva_lista_precio

    @classmethod
    def mostrar_todos(cls):
        session = sessionmaker(bind=engine)()
        lista_de_precios = session.query(cls).all() 
        return lista_de_precios

    @classmethod
    def obtener_libros_por_editorial(cls, id_editorial: int):
        session = sessionmaker(bind=engine)()
        
        # Verifica que la editorial exista
        editorial_existente = session.query(Editorial).filter(Editorial.id_editorial == id_editorial).one_or_none()
        if not editorial_existente:
            session.close()
            raise HTTPException(status_code=400, detail=f"La editorial con id {id_editorial} no existe.")                
                
        # Obtiene los libros de esa editorial, junto con su precio y el nombre de la editorial
        libros = (
            session.query(Libro, ListaDePrecios.precio, Editorial.nombre)
            .join(ListaDePrecios, ListaDePrecios.id_libro == Libro.id_libro)
            .join(Editorial, Editorial.id_editorial == ListaDePrecios.id_editorial)
            .filter(Editorial.id_editorial == id_editorial)
            .all()
        )
        session.close()
        return libros

    @classmethod
    def obtener_libros_por_id(cls, id_libro: int):
        session = sessionmaker(bind=engine)()        
        libro_existente = session.query(Libro).filter(Libro.id_libro == id_libro).one_or_none()
        if not libro_existente:
            session.close()
            raise HTTPException(status_code=400, detail=f"El libro con id {id_libro} no existe.")  
              
        # Obtiene los libros con ese id, independientemente de la editorial
        libros = (
            session.query(Libro, ListaDePrecios.precio, Editorial.nombre)
            .join(ListaDePrecios, ListaDePrecios.id_libro == Libro.id_libro)
            .join(Editorial, Editorial.id_editorial == ListaDePrecios.id_editorial)
            .filter(Libro.id_libro == id_libro)
            .all()
        )
        session.close()
        return libros

    @classmethod
    def obtener_libros_por_precio(cls, precio: float):
        session = sessionmaker(bind=engine)()
        
        # Obtiene los libros con precios iguales al precio especificado
        libros = (
            session.query(Libro, ListaDePrecios.precio, Editorial.nombre)
            .join(ListaDePrecios, ListaDePrecios.id_libro == Libro.id_libro)
            .join(Editorial, Editorial.id_editorial == ListaDePrecios.id_editorial)
            .filter(ListaDePrecios.precio == precio)
            .all()
        )
        session.close()
        return libros


    @classmethod
    def obtener_libros_por_precio_minimo(cls, precio_minimo: float):
        session = sessionmaker(bind=engine)()
        
        # Obtiene los libros con precios mayores al precio especificado
        libros = (
            session.query(Libro, ListaDePrecios.precio, Editorial.nombre)
            .join(ListaDePrecios, ListaDePrecios.id_libro == Libro.id_libro)
            .join(Editorial, Editorial.id_editorial == ListaDePrecios.id_editorial)
            .filter(ListaDePrecios.precio >= precio_minimo)
            .all()
        )
        session.close()
        return libros

    @classmethod
    def obtener_libros_por_precio_maximo(cls, precio_maximo: float):
        session = sessionmaker(bind=engine)()
        
        # Obtiene los libros con precios menores al precio especificado
        libros = (
            session.query(Libro, ListaDePrecios.precio, Editorial.nombre)
            .join(ListaDePrecios, ListaDePrecios.id_libro == Libro.id_libro)
            .join(Editorial, Editorial.id_editorial == ListaDePrecios.id_editorial)
            .filter(ListaDePrecios.precio <= precio_maximo)
            .all()
        )
        session.close()
        return libros