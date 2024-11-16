from fastapi import APIRouter
from typing import List
from models import ListaDePreciosModel, LibroConPrecioModel
from ListaDePrecios import ListaDePrecios
from sqlalchemy.orm import sessionmaker
from Libro import Libro
router = APIRouter()


# Endpoint POST para crear un nuevo precio
@router.post("/lista_precios/nuevo/", tags=["Lista de Precios"], summary="Agrega un nuevo libro a la lista de precios", description="Este endpoint agrega un nuevo libro a la lista de precios, usando los id de editoriales y libros existentes.")
def agregar_precio(nuevo_libro: ListaDePreciosModel):

    ListaDePrecios.agregar_libro_a_lista_precios(nuevo_libro)
    return {"message": "Precio agregado exitosamente"}


# Endpoint GET para obtener todos los precios
@router.get("/lista_precios/", response_model=List[ListaDePreciosModel], tags=["Lista de Precios"], summary="Obtener todos los precios", description="Este endpoint devuelve una lista de todos los precios y de todas las editoriales registrados en la base de datos.")
def obtener_lista_de_precios():
    precios = ListaDePrecios.mostrar_todos()
    return precios


# Endpoint GET para obtener libros y precios filtrando por editorial
@router.get("/lista_precios/por_editorial/", response_model=List[LibroConPrecioModel], tags=["Lista de Precios"], description="Obtener todos los libros y precios de una editorial específica.")
def obtener_libros_y_precios_por_editorial(id_editorial: int):
    libros = ListaDePrecios.obtener_libros_por_editorial(id_editorial)
    
    # Formateamos la respuesta con los datos de los libros y precios
    respuesta = []
    for libro, precio in libros:
        libro_con_precio = LibroConPrecioModel(
            id_libro=libro.id_libro,
            titulo=libro.titulo,
            autor=libro.autor,
            isbn=libro.isbn,
            precio=precio,
            stock=libro.stock,
            id_genero=libro.id_genero
        )
        respuesta.append(libro_con_precio)    
    
    return respuesta


