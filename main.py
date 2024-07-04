'''
instalado:
FastAPI (completo, incluido jinja2 y uvicorn)
sql server management estudio 20
sql server (evaluation version)
python 3.12.4 (64-bit)
pyodbc
SQLAlchemy
Microsoft ODBC Driver 18 for SQL Server (x64) version 18.3.3.1
Microsoft Visual C++ Redistributable (version 14.40.33810.0)
'''

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import pyodbc


server = r'DESKTOP-HL0DSTT'
database = 'dbbackend'

connection_string = (
    f'mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server'
    '&TrustServerCertificate=yes'
)

'''
# Pruebo la conexión
try:
    engine = create_engine(connection_string)
    print("Conexión exitosa!")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
'''

# Creo el motor de SQLAlchemy y declaro la clase base
engine = create_engine(connection_string)
Base = declarative_base()


# Defino la clase Publicacion (en base a la tabla de la base de datos)
class Publicacion(Base):
    __tablename__ = 'publicaciones'

    id_publicacion = Column(Integer, primary_key=True)
    especie = Column(String(50))
    nombre = Column(String(50))
    descripcion = Column(String(300))
    ubicacion = Column(String(100))
    estado = Column(String(50))
    telefono = Column(String(20))

    @classmethod
    def mostrar_todas(cls):
        session = sessionmaker(bind=engine)()
        publicaciones = session.query(cls).all()
        session.close()
        return publicaciones

    @classmethod
    def agregar_publicacion(cls, especie, nombre, descripcion, ubicacion, estado, telefono):
        nueva_publicacion = cls(
            especie=especie,
            nombre=nombre,
            descripcion=descripcion,
            ubicacion=ubicacion,
            estado=estado,
            telefono=telefono
        )
        session = sessionmaker(bind=engine)()
        session.add(nueva_publicacion)
        session.commit()
        session.refresh(nueva_publicacion)
        session.close()
        return nueva_publicacion
    
    @classmethod
    def eliminar_publicacion(cls, publicacion_id):
        session = sessionmaker(bind=engine)()
        publicacion = session.query(cls).filter_by(id_publicacion=publicacion_id).first()
        if publicacion:
            session.delete(publicacion)
            session.commit()
            session.close()
            return True
        session.close()
        return False
        
    @classmethod
    def modificar_publicacion(cls, publicacion_id, especie, nombre, descripcion, ubicacion, estado, telefono):
        session = sessionmaker(bind=engine)()
        publicacion = session.query(cls).filter_by(id_publicacion=publicacion_id).first()
        if publicacion:
            publicacion.especie = especie
            publicacion.nombre = nombre
            publicacion.descripcion = descripcion
            publicacion.ubicacion = ubicacion
            publicacion.estado = estado
            publicacion.telefono = telefono
            session.commit()
            session.close()
            return True
        session.close()
        return False