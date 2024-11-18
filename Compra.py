from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from database import engine, Base
from models import CompraModel

class Compra(Base):
    __tablename__ = 'compra'

    id_compra = Column(Integer, primary_key=True, autoincrement=True)
    id_editorial = Column(Integer, ForeignKey('editoriales.id_editorial', ondelete='SET NULL'), nullable=True)
    nombre_editorial = Column(String)
    fecha = Column(Date)
    total = Column(Float)  


    detalle_compra = relationship("DetalleCompra", back_populates="compra")
    editorial = relationship("Editorial", back_populates="compras")


@classmethod
def registrar_compra(cls, id_editorial: int, nombre_editorial: str, fecha: str, total: float, detalles: list):
    session = sessionmaker(bind=engine)()
    
    # Crear la nueva compra
    nueva_compra = cls(
        id_editorial=id_editorial,
        nombre_editorial=nombre_editorial,
        fecha=fecha,
        total=total,
    )
    
    # Agregar la compra a la sesión
    session.add(nueva_compra)
    session.commit()  # Obtener el ID de la compra después de insertar
    
    # Crear los detalles de la compra
    for detalle in detalles:
        nuevo_detalle = DetalleCompra(
            id_compra=nueva_compra.id_compra,  # Asociar la compra
            id_libro=detalle['id_libro'],
            nombre_libro=detalle['nombre_libro'],
            cantidad=detalle['cantidad'],
        )
        session.add(nuevo_detalle)
    
    # Confirmar los detalles
    session.commit()
    session.close()
    
    return nueva_compra
