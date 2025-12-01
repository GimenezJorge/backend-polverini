from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from database import Base, engine
from models import CompraModel
from DetalleCompra import DetalleCompra
from Editorial import Editorial
from Libro import Libro
from ListaDePrecios import ListaDePrecios  # Importar ListaDePrecios
from fastapi import HTTPException
from datetime import date
from sqlalchemy import extract

class Compra(Base):
    __tablename__ = 'compra'    

    id_compra = Column(Integer, primary_key=True, autoincrement=True)
    id_editorial = Column(Integer, ForeignKey('editoriales.id_editorial'))  # Relación con Editorial
    nombre_editorial = Column(String)
    fecha = Column(Date)
    total = Column(Float)

    # Relación con DetalleCompra
    detalles = relationship("DetalleCompra", back_populates="compra")
    
    @classmethod
    def agregar_compra(cls, compra_in: CompraModel):
        session = sessionmaker(bind=engine)()

        # Buscar el nombre de la editorial basado en el id_editorial
        editorial = session.query(Editorial).filter(Editorial.id_editorial == compra_in.id_editorial).one_or_none()
        if editorial is None:
            session.close()
            raise HTTPException(status_code=404, detail=f"Editorial con id {compra_in.id_editorial} no encontrada")

        # Crear la compra con el nombre de la editorial obtenido
        nueva_compra = cls(
            id_editorial=compra_in.id_editorial,
            nombre_editorial=editorial.nombre, 
            fecha=compra_in.fecha,
            total=0  # Inicializamos el total en 0
        )
        session.add(nueva_compra)
        session.commit()
        session.refresh(nueva_compra)

        # Inicializar total
        total = 0

        # Guardar los detalles de la compra y calcular el total
        for detalle in compra_in.detalles:
            # Verificar si el libro existe en la base de datos
            libro = session.query(Libro).filter(Libro.id_libro == detalle.id_libro).one_or_none()
            if libro is None:
                session.close()
                raise HTTPException(status_code=404, detail=f"Libro con id {detalle.id_libro} no encontrado")

            # Obtener el precio del libro desde la tabla 'lista_de_precios'
            
            precio_libro = session.query(ListaDePrecios).filter(ListaDePrecios.id_libro == detalle.id_libro, ListaDePrecios.id_editorial == compra_in.id_editorial).one_or_none()

            
            if precio_libro is None:
                session.close()
                raise HTTPException(status_code=404, detail=f"Esa editorial no tiene el libro con id {detalle.id_libro}")

            # Aumentar stock porque se está comprando al proveedor
            libro.stock += detalle.cantidad
            session.commit()

            detalle_compra = DetalleCompra(
                id_compra=nueva_compra.id_compra,
                id_libro=libro.id_libro,
                nombre_libro=libro.titulo,
                cantidad=detalle.cantidad,
                precio=precio_libro.precio  # Obtener el precio desde 'lista_de_precios'
            )
            session.add(detalle_compra)
            total += detalle.cantidad * precio_libro.precio  # Acumulamos el precio total

        # Asigno el total calculado a la compra
        nueva_compra.total = total
        session.commit()  
        session.close()

        return nueva_compra

    @classmethod
    def obtener_compras(cls):
        session = sessionmaker(bind=engine)()
        try:
            # Obtener todas las compras con los detalles
            compras = session.query(cls).options(joinedload(cls.detalles)).all()
            
            # Contar la cantidad de compras
            cantidad_compras = len(compras)
            
            return {"cantidad_compras": cantidad_compras, "compras": compras}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            session.close()

    @classmethod
    def obtener_compras_por_editorial(cls, id_editorial: int):
        session = sessionmaker(bind=engine)()
        try:
            # Filtrar las compras por id_editorial
            compras = session.query(cls).filter(cls.id_editorial == id_editorial).options(joinedload(cls.detalles)).all()
            
            # Obtener el total de compras
            total_compras = len(compras)
            
            # Retornar el total primero y luego las compras
            return {"total_compras": total_compras, "compras": compras}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            session.close()

    @classmethod
    def obtener_compras_por_fecha(cls, fecha: date = None, desde: date = None, hasta: date = None, año: int = None, mes: int = None):
        session = sessionmaker(bind=engine)()
        try:
            query = session.query(cls).options(joinedload(cls.detalles))

            if fecha:
                query = query.filter(cls.fecha == fecha)

            if desde:
                query = query.filter(cls.fecha >= desde)
            if hasta:
                query = query.filter(cls.fecha <= hasta)

            if año:
                query = query.filter(extract("year", cls.fecha) == año)

            if año and mes:
                query = query.filter(extract("month", cls.fecha) == mes)

            compras = query.all()
            total_filtradas = len(compras)

            return {"total_filtradas": total_filtradas, "compras": compras}

        finally:
            session.close()
