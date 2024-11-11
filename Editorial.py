from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String
from database  import engine, Base 
from models import EditorialModel  

# Defino la clase Editorial
class Editorial(Base):
    __tablename__ = 'editoriales'

    id_editorial = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    razon_social = Column(String)
    cuit = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    mail = Column(String)

    listas_de_precios = relationship("ListaDePrecios", back_populates="editorial")

    @classmethod
    def agregar_editorial(cls, nombre: str, razon_social: str, cuit: str, direccion: str, telefono: str, mail: str):
        nueva_editorial = cls(
            nombre=nombre,
            razon_social=razon_social,
            cuit=cuit,
            direccion=direccion,
            telefono=telefono,
            mail=mail
        )
        session = sessionmaker(bind=engine)()
        session.add(nueva_editorial)
        session.commit()
        session.refresh(nueva_editorial)
        session.close()
        return nueva_editorial

    @classmethod
    def mostrar_todos(cls):
        session = sessionmaker(bind=engine)()
        editoriales = session.query(cls).all()
        session.close()
        return editoriales

    @classmethod
    def eliminar_editorial(cls, editorial_id: int):
        session = sessionmaker(bind=engine)()
        editorial = session.query(cls).filter_by(id_editorial=editorial_id).first()
        if editorial:
            session.delete(editorial)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @classmethod
    def modificar_editorial(cls, editorial_id: int, editorial_in: EditorialModel):
        session = sessionmaker(bind=engine)()
        editorial_existente = session.query(cls).filter(cls.id_editorial == editorial_id).one_or_none()
        if not editorial_existente:
            session.close()
            raise Exception(f"Editorial con id {editorial_id} no encontrado")
                
        editorial_existente.nombre = editorial_in.nombre
        editorial_existente.razon_social = editorial_in.razon_social
        editorial_existente.cuit = editorial_in.cuit
        editorial_existente.direccion = editorial_in.direccion
        editorial_existente.telefono = editorial_in.telefono
        editorial_existente.mail = editorial_in.mail
        

        session.commit()
        session.refresh(editorial_existente)
        session.close()
        
        return EditorialModel(
            id_editorial=editorial_existente.id_editorial,
            nombre=editorial_existente.nombre,
            direccion=editorial_existente.direccion,
            telefono=editorial_existente.telefono
        )
