from fastapi import APIRouter
from typing import List
from models import GeneroModel
from Genero import Genero  

router = APIRouter()

# Endpoint para agregar un género
@router.post("/generos/nuevo/", tags=["Generos"], summary="Crear un nuevo género", description="Este endpoint permite crear un nuevo género en la base de datos.")
def agregar_genero(genero: GeneroModel):
    Genero.agregar_genero(genero)
    return {"message": "Género creado exitosamente"}

# Endpoint para obtener todos los géneros
@router.get("/generos/", response_model=List[GeneroModel], tags=["Generos"], summary="Obtener todos los géneros", description="Este endpoint devuelve una lista de todos los géneros registrados en la base de datos.")
def obtener_generos():
    generos = Genero.obtener_todos()
    return generos
