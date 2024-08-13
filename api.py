from datetime import datetime, date
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from main import Alumno, Curso, engine
from sqlalchemy.orm import sessionmaker, joinedload

app = FastAPI()

# CORS (permite la interacción con los navegadores)
origins = [
    "http://localhost",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo (formato) Pydantic para las entradas y salidas de Alumno
class AlumnoModel(BaseModel):
    idalumno: int = None
    apyn: str
    idcurso: int
    curso: str = None  # Campo para el nombre del curso
    fecnac: date

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d')
        }

# Modelo (formato) Pydantic para las entradas y salidas de Curso
class CursoModel(BaseModel):
    idcurso: int = None
    curso: str

    class Config:
        from_attributes = True



# Endpoint GET para obtener todos los alumnos en formato JSON
@app.get("/alumnos/", response_model=List[AlumnoModel])
def obtener_alumnos():
    Session = sessionmaker(bind=engine)
    session = Session()

    alumnos = session.query(Alumno).options(joinedload(Alumno.curso)).all()
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

# Endpoint POST para manejar el envío del formulario y crear un nuevo alumno
@app.post("/alumnos/nuevo/")
def agregar_alumno(alumno: AlumnoModel):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Obtener el curso correspondiente al idcurso proporcionado
    curso = session.query(Curso).filter(Curso.idcurso == alumno.idcurso).one_or_none()

    if not curso:
        session.close()
        raise HTTPException(status_code=404, detail=f"Curso con id {alumno.idcurso} no encontrado")

    nuevo_alumno = Alumno(
        apyn=alumno.apyn,
        idcurso=alumno.idcurso,
        fecnac=alumno.fecnac
    )

    session.add(nuevo_alumno)
    session.commit()
    session.refresh(nuevo_alumno)

    # Obtener el nombre del curso mientras la sesión está abierta
    nombre_curso = curso.curso

    session.close()

    # Crear el modelo AlumnoModel con el curso cargado
    alumno_con_curso = AlumnoModel(
        idalumno=nuevo_alumno.idalumno,
        apyn=nuevo_alumno.apyn,
        idcurso=nuevo_alumno.idcurso,
        curso=nombre_curso,  # Aquí se obtiene el nombre del curso
        fecnac=nuevo_alumno.fecnac
    )

    return {"message": "Alumno creado exitosamente", "alumno": alumno_con_curso}




# Endpoint DELETE para eliminar un alumno
@app.delete("/alumnos/{alumno_id}")
def eliminar_alumno(alumno_id: int):
    if not Alumno.eliminar_alumno(alumno_id):
        raise HTTPException(status_code=404, detail=f"Alumno con id {alumno_id} no encontrado")
    return {"message": f"Alumno con id {alumno_id} eliminado correctamente"}

# Endpoint PUT para modificar un alumno
@app.put("/alumnos/{alumno_id}", response_model=AlumnoModel)
def modificar_alumno(alumno_id: int, alumno_in: AlumnoModel):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Obtener el alumno existente
    alumno_existente = session.query(Alumno).filter(Alumno.idalumno == alumno_id).one_or_none()

    if not alumno_existente:
        session.close()
        raise HTTPException(status_code=404, detail=f"Alumno con id {alumno_id} no encontrado")

    # Actualizar los campos del alumno
    alumno_existente.apyn = alumno_in.apyn
    alumno_existente.idcurso = alumno_in.idcurso
    alumno_existente.fecnac = alumno_in.fecnac

    session.commit()
    session.refresh(alumno_existente)

    # Obtener el curso correspondiente al idcurso del alumno actualizado
    curso = session.query(Curso).filter(Curso.idcurso == alumno_existente.idcurso).one_or_none()
    nombre_curso = curso.curso if curso else None

    session.close()

    # Crear el modelo AlumnoModel con el curso cargado
    alumno_con_curso = AlumnoModel(
        idalumno=alumno_existente.idalumno,
        apyn=alumno_existente.apyn,
        idcurso=alumno_existente.idcurso,
        curso=nombre_curso,  # Aquí se obtiene el nombre del curso
        fecnac=alumno_existente.fecnac
    )

    return alumno_con_curso

# Endpoint POST para agregar un curso
@app.post("/cursos/nuevo/")
def agregar_curso(curso: CursoModel):
    nuevo_curso = Curso.agregar_curso(curso.curso)
    return {"message": "Curso agregado exitosamente", "curso": CursoModel.model_validate(nuevo_curso)}

# Endpoint GET para recuperar todos los cursos
@app.get("/cursos/", response_model=List[CursoModel])
def recuperar_cursos():
    cursos = Curso.recuperar_cursos()
    return cursos