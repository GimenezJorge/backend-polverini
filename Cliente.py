from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from database import Base, engine

# Defino la clase Cliente
class Cliente(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    email = Column(String(100))
    telefono = Column(String(20))
    direccion = Column(String(255))

    @classmethod
    def registrar_cliente(cls, nombre: str, email: str = None, telefono: str = None, direccion: str = None):
        nuevo_cliente = cls(
            nombre=nombre,
            email=email,
            telefono=telefono,
            direccion=direccion
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
    def mostrar_todos(cls):
        session = sessionmaker(bind=engine)()
        clientes = session.query(cls).all()
        session.close()
        return clientes

    @classmethod
    def modificar_cliente(cls, cliente_id: int, nombre: str = None, email: str = None, telefono: str = None, direccion: str = None):
        session = sessionmaker(bind=engine)()
        cliente_existente = session.query(cls).filter(cls.id_cliente == cliente_id).one_or_none()
        if not cliente_existente:
            session.close()
            raise Exception(f"Cliente con id {cliente_id} no encontrado")
        
        if nombre is not None:
            cliente_existente.nombre = nombre
        if email is not None:
            cliente_existente.email = email
        if telefono is not None:
            cliente_existente.telefono = telefono
        if direccion is not None:
            cliente_existente.direccion = direccion
        
        session.commit()
        session.refresh(cliente_existente)
        session.close()
        
        return cliente_existente

    @classmethod
    def eliminar_cliente(cls, cliente_id: int):
        session = sessionmaker(bind=engine)()
        cliente = session.query(cls).filter_by(id_cliente=cliente_id).first()
        if cliente:
            session.delete(cliente)
            session.commit()
            session.close()
            return True
        session.close()
        return False