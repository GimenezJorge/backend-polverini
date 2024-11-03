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
#CONEXION DE MI CASA:
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, joinedload
from model import AlumnoModel, CursoModel, ProveedorModel 
from fastapi import HTTPException

server = r'DESKTOP-9IIVD9P\SQLEXPRESS'
database = 'bdg3'

connection_string = (
    f'mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server'
    '&TrustServerCertificate=yes'
)
"""
#CONEXION DE LA ESCUELA:
server = 'sqlserver\\sqlserver'
database = 'bdg3'
username = 'bdg3'
password = 'bdg3'
driver = 'ODBC Driver 18 for SQL Server'

# Construcción de la cadena de conexión usando las variables
connection_string = (
    f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
    '&TrustServerCertificate=yes'
)
"""

"""
# Pruebo la conexión
try:
    engine = create_engine(connection_string)
    print("Conexión exitosa!")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
"""

# Creo el motor de SQLAlchemy y declaro la clase base
engine = create_engine(connection_string)
Base = declarative_base()


# Defino la clase Alumno (en base a la tabla de la base de datos)
class Alumno(Base):
    __tablename__ = 'alumnos'

    idalumno = Column(Integer, primary_key=True, autoincrement=True)
    apyn = Column(String)
    idcurso = Column(Integer, ForeignKey('cursos.idcurso'))
    fecnac = Column(Date)

    # Relación con la tabla 'cursos'
    curso = relationship('Curso', back_populates='alumnos')

    @classmethod
    def mostrar_todos(cls):
        session = sessionmaker(bind=engine)()
        alumnos = session.query(cls).options(joinedload(cls.curso)).all()
        session.close()

        # Mapea los datos para incluir el nombre del curso
        alumnos_con_curso = [
            {
                "idalumno": alumno.idalumno,
                "apyn": alumno.apyn,
                "idcurso": alumno.idcurso,
                "curso": alumno.curso.curso,  # Aquí se obtiene el nombre del curso
                "fecnac": alumno.fecnac
            }
            for alumno in alumnos
        ]

        return alumnos_con_curso

    @classmethod
    def agregar_alumno(cls, apyn: str, idcurso: int, fecnac: Date):
        Session = sessionmaker(bind=engine)
        session = Session()

        # Obtener el curso correspondiente al idcurso proporcionado
        curso = session.query(Curso).filter(Curso.idcurso == idcurso).one_or_none()
        if not curso:
            session.close()
            raise Exception(f"Curso con id {idcurso} no encontrado")  # Manejo de errores más sencillo

        # Crear un nuevo alumno
        nuevo_alumno = cls(apyn=apyn, idcurso=idcurso, fecnac=fecnac)
        session.add(nuevo_alumno)
        session.commit()
        session.refresh(nuevo_alumno)

        # Obtener el nombre del curso
        nombre_curso = curso.curso
        session.close()

        # Crear el diccionario con la información del nuevo alumno
        alumno_con_curso = {
            "idalumno": nuevo_alumno.idalumno,
            "apyn": nuevo_alumno.apyn,
            "idcurso": nuevo_alumno.idcurso,
            "curso": nombre_curso,
            "fecnac": nuevo_alumno.fecnac
        }

        return alumno_con_curso

    @classmethod
    def eliminar_alumno(cls, alumno_id):
        session = sessionmaker(bind=engine)()
        alumno = session.query(cls).filter_by(idalumno=alumno_id).first()
        if alumno:
            session.delete(alumno)
            session.commit()
            session.close()
            return True
        session.close()
        return False
        
    @classmethod
    def modificar_alumno(cls, alumno_id: int, alumno_in: AlumnoModel):
        session = sessionmaker(bind=engine)()
        alumno_existente = session.query(cls).filter(cls.idalumno == alumno_id).one_or_none()
        if not alumno_existente:
            session.close()
            raise Exception(f"Alumno con id {alumno_id} no encontrado")
        alumno_existente.apyn = alumno_in.apyn
        alumno_existente.idcurso = alumno_in.idcurso
        alumno_existente.fecnac = alumno_in.fecnac
        
        session.commit()
        session.refresh(alumno_existente)
        
        curso = session.query(Curso).filter(Curso.idcurso == alumno_existente.idcurso).one_or_none()
        nombre_curso = curso.curso if curso else None
        session.close()
        alumno_con_curso = AlumnoModel(
            idalumno=alumno_existente.idalumno,
            apyn=alumno_existente.apyn,
            idcurso=alumno_existente.idcurso,
            curso=nombre_curso,
            fecnac=alumno_existente.fecnac
        )
        return alumno_con_curso


# Defino la clase Curso (en base a la tabla de la base de datos)
class Curso(Base):
    __tablename__ = 'cursos'

    idcurso = Column(Integer, primary_key=True, autoincrement=True)
    curso = Column(String)

    # Relación inversa
    alumnos = relationship('Alumno', back_populates='curso')

    @classmethod
    def agregar_curso(cls, curso):
        nuevo_curso = cls(
            curso=curso
        )
        session = sessionmaker(bind=engine)()
        session.add(nuevo_curso)
        session.commit()
        session.refresh(nuevo_curso)
        session.close()
        return nuevo_curso
    
    @classmethod
    def recuperar_cursos(cls):
        session = sessionmaker(bind=engine)()
        cursos = session.query(cls).all()
        session.close()
        return cursos

# Defino la clase Proveedor (en base a la nueva tabla que deseas agregar)
class Proveedor(Base):
    __tablename__ = 'proveedores'

    idproveedor = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    direccion = Column(String)
    telefono = Column(String)

    @classmethod
    def agregar_proveedor(cls, nombre: str, direccion: str, telefono: str):
        nuevo_proveedor = cls(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono
        )
        session = sessionmaker(bind=engine)()
        session.add(nuevo_proveedor)
        session.commit()
        session.refresh(nuevo_proveedor)
        session.close()
        return nuevo_proveedor

    @classmethod
    def mostrar_todos(cls):
        session = sessionmaker(bind=engine)()
        proveedores = session.query(cls).all()
        session.close()
        return proveedores

    @classmethod
    def eliminar_proveedor(cls, proveedor_id: int):
        session = sessionmaker(bind=engine)()
        proveedor = session.query(cls).filter_by(idproveedor=proveedor_id).first()
        if proveedor:
            session.delete(proveedor)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @classmethod
    def modificar_proveedor(cls, proveedor_id: int, proveedor_in: ProveedorModel):
        session = sessionmaker(bind=engine)()
        proveedor_existente = session.query(cls).filter(cls.idproveedor == proveedor_id).one_or_none()
        if not proveedor_existente:
            session.close()
            raise Exception(f"Proveedor con id {proveedor_id} no encontrado")
        
        # Actualiza los campos del proveedor existente
        proveedor_existente.nombre = proveedor_in.nombre
        proveedor_existente.direccion = proveedor_in.direccion
        proveedor_existente.telefono = proveedor_in.telefono

        session.commit()
        session.refresh(proveedor_existente)
        session.close()
        
        return ProveedorModel(
            idproveedor=proveedor_existente.idproveedor,
            nombre=proveedor_existente.nombre,
            direccion=proveedor_existente.direccion,
            telefono=proveedor_existente.telefono
        )

