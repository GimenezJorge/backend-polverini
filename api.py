from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from main import Publicacion, engine
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware

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

# Configuración de Jinja2
templates = Jinja2Templates(directory="templates")

# Modelo (formato) Pydantic para las entradas y salidas
class PublicacionModel(BaseModel):
    id_publicacion: int = None
    especie: str
    nombre: str
    descripcion: str
    ubicacion: str
    estado: str
    telefono: str

    class Config:
        from_attributes = True

# Endpoint GET para obtener todas las publicaciones y renderizar la plantilla
@app.get("/publicaciones/html/", response_class=HTMLResponse)
def leer_publicaciones_html(request: Request):
    Session = sessionmaker(bind=engine)
    session = Session()
    publicaciones = session.query(Publicacion).all()
    session.close()
    return templates.TemplateResponse("index.html", {"request": request, "publicaciones": publicaciones})


# Endpoint GET para mostrar el formulario de creación de publicaciones
@app.get("/publicaciones/nueva/html/", response_class=HTMLResponse)
def mostrar_formulario_creacion(request: Request):
    return templates.TemplateResponse("create_publicacion.html", {"request": request})

# Endpoint POST para manejar el envío del formulario y crear una nueva publicación
@app.post("/publicaciones/nueva/html/")
def agregar_publicacion_html(
    request: Request,
    especie: str = Form(...),
    nombre: str = Form(...),
    descripcion: str = Form(...),
    ubicacion: str = Form(...),
    estado: str = Form(...),
    telefono: str = Form(...),
):
    Session = sessionmaker(bind=engine)
    session = Session()

    nueva_publicacion = Publicacion(
        especie=especie,
        nombre=nombre,
        descripcion=descripcion,
        ubicacion=ubicacion,
        estado=estado,
        telefono=telefono
    )

    session.add(nueva_publicacion)
    session.commit()
    session.refresh(nueva_publicacion)
    session.close()

    return templates.TemplateResponse("create_publicacion.html", {"request": request, "mensaje": "Publicación creada exitosamente"})








# Endpoint DELETE para eliminar una publicación
@app.delete("/publicaciones/{publicacion_id}")
def eliminar_publicacion(publicacion_id: int):
    if not Publicacion.eliminar_publicacion(publicacion_id):
        raise HTTPException(status_code=404, detail=f"Publicación con id {publicacion_id} no encontrada")
    return {"message": f"Publicación con id {publicacion_id} eliminada correctamente"}

# Endpoint PUT para modificar una publicación
@app.put("/publicaciones/{publicacion_id}", response_model=PublicacionModel)
def modificar_publicacion(publicacion_id: int, publicacion_in: PublicacionModel):
    updated = Publicacion.modificar_publicacion(
        publicacion_id,
        especie=publicacion_in.especie,
        nombre=publicacion_in.nombre,
        descripcion=publicacion_in.descripcion,
        ubicacion=publicacion_in.ubicacion,
        estado=publicacion_in.estado,
        telefono=publicacion_in.telefono
    )

    if not updated:
        raise HTTPException(status_code=404, detail=f"Publicación con id {publicacion_id} no encontradajuju")

    return publicacion_in

'''
json para la modificacion PUT en thunderclient:
{
    "especie": "Gato",
    "nombre": "michi",
    "descripcion": "gato molesto",
    "ubicacion": "Casa",
    "estado": "Encontrado",
    "telefono": "4557-1234"
}
'''