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

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


server = r'DESKTOP-HL0DSTT'
database = 'dbbackend'

connection_string = (
    f'mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server'
    '&TrustServerCertificate=yes'
)


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
        alumnos = session.query(cls).all()
        session.close()
        return alumnos

    @classmethod
    def agregar_alumno(cls, apyn, idcurso, fecnac):
        nuevo_alumno = cls(
            apyn=apyn,
            idcurso=idcurso,
            fecnac=fecnac
        )
        session = sessionmaker(bind=engine)()
        session.add(nuevo_alumno)
        session.commit()
        session.refresh(nuevo_alumno)
        session.close()
        return nuevo_alumno
    
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
    def modificar_alumno(cls, alumno_id, apyn, idcurso, fecnac):
        session = sessionmaker(bind=engine)()
        alumno = session.query(cls).filter_by(idalumno=alumno_id).first()
        if alumno:
            alumno.apyn = apyn
            alumno.idcurso = idcurso
            alumno.fecnac = fecnac
            session.commit()
            session.close()
            return True
        session.close()
        return False

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
    
 