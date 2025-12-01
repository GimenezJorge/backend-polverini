from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String
from database import engine, Base
from models import GeneroModel

class Genero(Base):
    __tablename__ = 'generos'

    id_genero = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100)  )
    
    # Relación con la tabla de libros
    libros = relationship("Libro", back_populates="genero")

    @classmethod
    def agregar_genero(cls, genero_in: GeneroModel):
        nuevo_genero = cls(nombre=genero_in.nombre)
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

    @classmethod
    def modificar_genero(cls, id_genero: int, genero_in: GeneroModel):
        session = sessionmaker(bind=engine)()
        genero = session.query(cls).filter(cls.id_genero == id_genero).one_or_none()

        if not genero:
            session.close()
            return False

        genero.nombre = genero_in.nombre
        session.commit()
        session.close()
        return True


    @classmethod
    def eliminar_genero(cls, id_genero: int):
        session = sessionmaker(bind=engine)()
        genero = session.query(cls).filter(cls.id_genero == id_genero).one_or_none()

        if not genero:
            session.close()
            return False

        session.delete(genero)
        session.commit()
        session.close()
        return True
