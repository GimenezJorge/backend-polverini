from fastapi import APIRouter, HTTPException
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

# Endpoint PUT para modificar un género
@router.put("/generos/{id_genero}", tags=["Generos"], summary="Modificar un género", description="Este endpoint modifica el nombre de un género identificado por su ID.")
def modificar_genero(id_genero: int, genero_in: GeneroModel):
    resultado = Genero.modificar_genero(id_genero, genero_in)

    if not resultado:
        raise HTTPException(status_code=404, detail=f"Género con id {id_genero} no encontrado")

    return {"message": "Género modificado correctamente"}

# Endpoint DELETE para eliminar un género
@router.delete("/generos/{id_genero}", tags=["Generos"], summary="Eliminar un género", description="Este endpoint elimina un género identificado por su ID.")
def eliminar_genero(id_genero: int):
    resultado = Genero.eliminar_genero(id_genero)

    if not resultado:
        raise HTTPException(status_code=404, detail=f"Género con id {id_genero} no encontrado")

    return {"message": "Género eliminado correctamente"}
