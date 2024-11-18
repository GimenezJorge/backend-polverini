from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from database import Base, engine
from models import CompraModel
from DetalleCompra import DetalleCompra

class Compra(Base):
    __tablename__ = 'compra'    

    id_compra = Column(Integer, primary_key=True, autoincrement=True)
    id_editorial = Column(Integer, ForeignKey('editoriales.id_editorial'))  # Relación con Editorial
    nombre_editorial = Column(String)
    fecha = Column(Date)
    total = Column(Float)

    # Relación con DetalleCompra
    detalles = relationship("DetalleCompra", back_populates="compra")
    













    # @classmethod
    # def agregar_compra(cls, compra_in: CompraModel):


    #     # Crear el registro de la compra
    #     nueva_compra = cls(
    #         id_editorial=compra_in.id_editorial,
    #         nombre_editorial=compra_in.nombre_editorial,
    #         fecha=compra_in.fecha,
    #         total=compra_in.total
    #     )
    #     session = sessionmaker(bind=engine)()
    #     session.add(nueva_compra)
    #     session.commit()
    #     session.refresh(nueva_compra)  
    #     session.close()  
    #     return nueva_compra


















        # # Agregar los detalles de la compra
        # for detalle in compra_in.detalles:
        #     # Buscar el libro por id_libro
        #     libro = session.query(Libro).filter(Libro.id_libro == detalle.id_libro).first()
        #     if libro:
        #         # Crear el detalle de la compra
        #         detalle_compra = DetalleCompra(
        #             id_compra=nueva_compra.idcompra,
        #             id_libro=libro.id_libro,
        #             nombre_libro=libro.titulo,  # Usar el título del libro
        #             cantidad=detalle.cantidad,
        #             precio=detalle.precio
        #         )
        #         session.add(detalle_compra)

        # session.commit()  # Confirmar los cambios




