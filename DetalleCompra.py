from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import engine, Base

# Defino la clase DetalleCompra
class DetalleCompra(Base):
    __tablename__ = 'detalle_compra'

    id_detalle_compra = Column(Integer, primary_key=True, autoincrement=True)
    id_compra = Column(Integer, ForeignKey('compra.id_compra'))
    id_libro = Column(Integer, ForeignKey('libros.id_libro'), nullable=True)
    nombre_libro = Column(String(255))
    cantidad = Column(Integer)
    precio = Column(Float)
    
    compra = relationship('Compra', back_populates='detalles')

