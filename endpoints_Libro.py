from fastapi import APIRouter, HTTPException
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

# Obtener libros por género
@router.get("/libros/genero/{id_genero}", tags=["Libros"], summary="Obtener libros por género", description="Devuelve una lista de libros que pertenecen al género indicado.")
def obtener_libros_por_genero(id_genero: int):
    libros = Libro.obtener_por_genero(id_genero)

    if not libros:
        raise HTTPException(status_code=404, detail=f"No hay libros con el género {id_genero}")

    return libros

# Endpoint GET para buscar libros por nombre
@router.get("/libros/buscar/", response_model=List[LibroModel], tags=["Libros"], summary="Buscar libros por nombre", description="Devuelve todos los libros cuyo nombre coincida parcial o totalmente.")
def buscar_libros(nombre: str):
    libros = Libro.obtener_por_nombre(nombre)
    if not libros:
        raise HTTPException(status_code=404, detail="No se encontraron libros con ese nombre")
    return libros

@router.put("/libros/{id_libro}", tags=["Libros"], summary="Modificar un libro", description="Modifica los datos de un libro identificado por su ID.")
def modificar_libro(id_libro: int, libro_in: LibroModel):
    resultado = Libro.modificar_libro(id_libro, libro_in)

    if resultado is False:
        raise HTTPException(status_code=404, detail=f"Libro con id {id_libro} no encontrado")

    if resultado == "genero_invalido":
        raise HTTPException(status_code=400, detail=f"Género con id {libro_in.id_genero} no existe")

    return {"message": "Libro modificado correctamente"}

@router.delete("/libros/{id_libro}", tags=["Libros"], summary="Eliminar un libro", description="Elimina un libro identificado por su ID.")
def eliminar_libro(id_libro: int):
    resultado = Libro.eliminar_libro(id_libro)

    if not resultado:
        raise HTTPException(status_code=404, detail=f"Libro con id {id_libro} no encontrado")

    return {"message": "Libro eliminado correctamente"}
