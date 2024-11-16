from fastapi import APIRouter
from typing import List
from models import LibroModel
from Libro import Libro


router = APIRouter()

@router.post("/libros/nuevo/", tags=["Libros"], summary="Agregar un nuevo libro", description="Este endpoint permite agregar un nuevo libro a la base de datos.")
def agregar_libro(libro: LibroModel):
    Libro.agregar_libro(libro)
    return {"message": "Libro agregado exitosamente"}

@router.get("/libros/", response_model=List[LibroModel], tags=["Libros"], description="Obtener todos los libros")
def obtener_libros():
    libros = Libro.mostrar_todos()
    return libros

