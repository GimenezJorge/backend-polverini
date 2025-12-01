from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from database import Base, engine
from models import ClienteModel 

# Defino la clase Cliente
class Cliente(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    email = Column(String(100))
    telefono = Column(String(20))
    direccion = Column(String(255))

    @classmethod
    def agregar_cliente(cls, cliente_in: ClienteModel):
        nuevo_cliente = cls(
            nombre=cliente_in.nombre,
            email=cliente_in.email,
            telefono=cliente_in.telefono,
            direccion=cliente_in.direccion
        )
        session = sessionmaker(bind=engine)()
        session.add(nuevo_cliente)
        session.commit()
        session.refresh(nuevo_cliente)
        session.close()
        return nuevo_cliente

    @classmethod
    def obtener_cliente(cls, cliente_id: int):
        session = sessionmaker(bind=engine)()
        cliente = session.query(cls).filter_by(id_cliente=cliente_id).one_or_none()
        session.close()
        return cliente

    @classmethod
    def obtener_por_nombre(cls, nombre: str):
        session = sessionmaker(bind=engine)()
        try:
            clientes = (
                session.query(cls)
                .filter(cls.nombre.ilike(f"%{nombre}%"))
                .all()
            )
            return clientes
        finally:
            session.close()


    @classmethod
    def mostrar_todos(cls):
        session = sessionmaker(bind=engine)()
        clientes = session.query(cls).all()
        session.close()
        return clientes  

    @classmethod
    def modificar_cliente(cls, cliente_id: int, cliente_in: ClienteModel):
        session = sessionmaker(bind=engine)()
        cliente_existente = session.query(cls).filter(cls.id_cliente == cliente_id).one_or_none()
        if not cliente_existente:
            session.close()
            raise Exception(f"Cliente con id {cliente_id} no encontrado")
        
        cliente_existente.nombre = cliente_in.nombre
        cliente_existente.email = cliente_in.email
        cliente_existente.telefono = cliente_in.telefono        
        cliente_existente.direccion = cliente_in.direccion
                        
        session.commit()
        session.refresh(cliente_existente)
        session.close()
        
        return cliente_existente

    @classmethod
    def eliminar_cliente(cls, cliente_id: int):
        #ACA VOY A TENER QUE IMPORTAR LA CLASE VENTA_CLIENTE CUANDO TENGO VENTA_CLIENTE.PY
        session = sessionmaker(bind=engine)()        
        #DESDE ACA VOY A TENER QUE BORRAR EL ID_CLIENTE DE LA TABLA VENTA_CLIENTE
        cliente = session.query(cls).filter_by(id_cliente=cliente_id).first()
        if cliente:
            session.delete(cliente)
            session.commit()
            session.close()
            return True
        session.close()
        return False