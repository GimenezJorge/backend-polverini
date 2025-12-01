from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from database import Base, engine
from models import VentaCreateModel
from Cliente import Cliente
from Libro import Libro
from DetalleVenta import DetalleVenta
from fastapi import HTTPException
from datetime import date
from sqlalchemy import extract

class Venta(Base):
    __tablename__ = 'venta'

    id_venta = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=False)
    nombre_cliente = Column(String)
    fecha = Column(Date)
    total = Column(Float)

    # Relación con DetalleVenta
    detalles = relationship("DetalleVenta", back_populates="venta")
    
    @classmethod
    def agregar_venta(cls, venta_in: VentaCreateModel):
        session = sessionmaker(bind=engine)()

        # Buscar el cliente basado en id_cliente
        cliente = session.query(Cliente).filter(Cliente.id_cliente == venta_in.id_cliente).one_or_none()
        if cliente is None:
            session.close()
            raise HTTPException(status_code=404, detail=f"Cliente con id {venta_in.id_cliente} no encontrado")

        # Crear la venta con el nombre del cliente obtenido
        nueva_venta = cls(
            id_cliente=venta_in.id_cliente,
            nombre_cliente=cliente.nombre,
            fecha=venta_in.fecha,
            total=0  # Inicializamos el total en 0
        )
        session.add(nueva_venta)
        session.commit()
        session.refresh(nueva_venta)

        # Inicializar total
        total = 0

        # Guardar los detalles de la venta y calcular el total
        for detalle in venta_in.detalles:
            # Verificar si el libro existe en la base de datos
            libro = session.query(Libro).filter(Libro.id_libro == detalle.id_libro).one_or_none()
            if libro is None:
                session.close()
                raise HTTPException(status_code=404, detail=f"Libro con id {detalle.id_libro} no encontrado")

            # Verificar stock suficiente
            if libro.stock < detalle.cantidad:
                session.close()
                raise HTTPException(status_code=400, detail=f"Stock insuficiente para el libro '{libro.titulo}'")

            # Descontar stock
            libro.stock -= detalle.cantidad
            session.commit()

            detalle_venta = DetalleVenta(
                id_venta=nueva_venta.id_venta,
                id_libro=libro.id_libro,
                nombre_libro=libro.titulo,
                cantidad=detalle.cantidad,
                precio=detalle.precio
            )
            session.add(detalle_venta)
            total += detalle.cantidad * detalle.precio

        # Asigno el total calculado a la venta
        nueva_venta.total = total
        session.commit()  
        session.close()

        return nueva_venta

    @classmethod
    def obtener_ventas(cls):
        session = sessionmaker(bind=engine)()
        try:
            # Obtener todas las ventas con los detalles
            ventas = session.query(cls).options(joinedload(cls.detalles)).all()

            # Contar la cantidad de ventas
            cantidad_ventas = len(ventas)

            return {"cantidad_ventas": cantidad_ventas, "ventas": ventas}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            session.close()

    @classmethod
    def obtener_ventas_por_cliente(cls, id_cliente: int):
        session = sessionmaker(bind=engine)()
        try:
            # Filtrar las ventas por id_cliente
            ventas = session.query(cls).filter(cls.id_cliente == id_cliente).options(joinedload(cls.detalles)).all()

            # Obtener el total de ventas
            total_ventas = len(ventas)

            # Retornar el total primero y luego las ventas
            return {"total_ventas": total_ventas, "ventas": ventas}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            session.close()

    @classmethod
    def obtener_ventas_por_fecha(cls, fecha: date = None, desde: date = None, hasta: date = None, año: int = None, mes: int = None):
        session = sessionmaker(bind=engine)()
        try:
            query = session.query(cls).options(joinedload(cls.detalles))

            # Fecha exacta
            if fecha:
                query = query.filter(cls.fecha == fecha)

            # Rango de fechas
            if desde:
                query = query.filter(cls.fecha >= desde)
            if hasta:
                query = query.filter(cls.fecha <= hasta)

            # Año
            if año:
                query = query.filter(extract("year", cls.fecha) == año)

            # Mes dentro de un año
            if año and mes:
                query = query.filter(extract("month", cls.fecha) == mes)

            ventas = query.all()
            total_filtradas = len(ventas)

            return {
                "total_filtradas": total_filtradas,
                "ventas": ventas
            }

        finally:
            session.close()