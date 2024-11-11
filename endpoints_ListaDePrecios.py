from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models import ListaDePreciosModel  # Asegúrate de que este modelo esté en models.py
from ListaDePrecios import ListaDePrecios  # Asegúrate de que la clase ListaDePrecios esté importada
from database import SessionLocal  # Importa SessionLocal de database.py
from sqlalchemy.orm import Session

router = APIRouter()

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()  # Crear una nueva sesión
    try:
        yield db  # Usar la sesión en la ruta
    finally:
        db.close()  # Cerrar la sesión después de usarla

# Endpoint POST para crear un nuevo precio
@router.post("/listas_precios/nueva/", tags=["Listas de Precios"], summary="Crear una nueva lista de precios", description="Este endpoint crea una nueva lista de precios en la base de datos.")
def crear_precio(precio: ListaDePreciosModel, db: Session = Depends(get_db)):
    nuevo_precio = ListaDePrecios.crear_precio(
        session=db,
        id_editorial=precio.id_editorial,
        id_libro=precio.id_libro,
        precio=precio.precio
    )

    # Agregar el nuevo precio a la sesión y hacer commit
    db.add(nuevo_precio)
    db.commit()  # Guarda los cambios en la base de datos
    db.refresh(nuevo_precio)  # Actualiza el objeto nuevo_precio con los datos de la base de datos

    return {"message": "Precio creado exitosamente", "precio": nuevo_precio}

# Endpoint GET para obtener todos los precios
@router.get("/listas_precios/", response_model=List[ListaDePreciosModel], tags=["Listas de Precios"], summary="Obtener todos los precios", description="Este endpoint devuelve una lista de todos los precios registrados en la base de datos.")
def obtener_precios(db: Session = Depends(get_db)):
    precios = ListaDePrecios.mostrar_todos(db)
    return precios
