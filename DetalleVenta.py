from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import engine, Base

# Defino la clase DetalleVenta
class DetalleVenta(Base):
    __tablename__ = 'detalle_venta'

    id_detalle_venta = Column(Integer, primary_key=True, autoincrement=True)
    id_venta = Column(Integer, ForeignKey('venta.id_venta'))
    id_libro = Column(Integer, ForeignKey('libros.id_libro'), nullable=True)
    nombre_libro = Column(String(255))
    cantidad = Column(Integer)
    precio = Column(Float)

    venta = relationship('Venta', back_populates='detalles')
