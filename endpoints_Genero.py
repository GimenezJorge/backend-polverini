from fastapi import APIRouter, HTTPException
from typing import List
from models import Genero as GeneroModel  # Importa el modelo Pydantic
from Genero import Genero  # Importa la clase ORM

router = APIRouter()

# Endpoint para agregar un género
@router.post("/generos/nuevo/", tags=["Generos"], summary="Crear un nuevo género", description="Este endpoint permite crear un nuevo género en la base de datos.")
def agregar_genero(genero: GeneroModel):  # Cambiar a GeneroModel
    nuevo_genero = Genero.agregar_genero(nombre=genero.nombre)
    return {"message": "Género creado exitosamente", "genero": nuevo_genero}

# Endpoint para obtener todos los géneros
@router.get("/generos/", response_model=List[GeneroModel], tags=["Generos"], summary="Obtener todos los géneros", description="Este endpoint devuelve una lista de todos los géneros registrados en la base de datos.")
def obtener_generos():
    generos = Genero.obtener_todos()
    return generos
