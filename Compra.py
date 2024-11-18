from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

# Clase Compra
class Compra(Base):
    __tablename__ = 'compra'

    id_compra = Column(Integer, primary_key=True, autoincrement=True)
    id_editorial = Column(Integer, ForeignKey('editoriales.id_editorial'))
    nombre_editorial = Column(String(255))
    fecha = Column(Date)
    total = Column(Float)

    # Relación con DetalleCompra
    detalles = relationship("DetalleCompra", back_populates="compra")


# Clase DetalleCompra
class DetalleCompra(Base):
    __tablename__ = 'detalle_compra'

    id_detalle_compra = Column(Integer, primary_key=True, autoincrement=True)
    id_compra = Column(Integer, ForeignKey('compra.id_compra'))
    id_libro = Column(Integer, ForeignKey('libros.id_libro'))
    nombre_libro = Column(String(255))
    cantidad = Column(Integer)
    precio = Column(Float)

    # Relación con Compra
    compra = relationship("Compra", back_populates="detalles")
