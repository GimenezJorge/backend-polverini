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
@router.get("/lista_precios/por_editorial/", response_model=List[LibroConPrecioModel], tags=["Lista de Precios"], summary="Obtener todos los libros, filtrando por el ID de la editorial" ,description="Obtener todos los libros y precios de una editorial específica.")
def obtener_libros_y_precios_por_editorial(id_editorial: int):
    libros = ListaDePrecios.obtener_libros_por_editorial(id_editorial)
    
    # Formateamos la respuesta con los datos de los libros, precios y nombre de la editorial
    respuesta = []
    
    for libro, precio, editorial in libros:
        libro_con_precio = LibroConPrecioModel(
            id_libro=libro.id_libro,
            titulo=libro.titulo,
            autor=libro.autor,
            isbn=libro.isbn,
            stock=libro.stock,
            id_genero=libro.id_genero,
            precio=precio,
            editorial=editorial,  # Incluye el nombre de la editorial
        )
        respuesta.append(libro_con_precio)    
    
    return respuesta
    
    
# Endpoint GET para obtener libros y precios por id_libro
@router.get("/lista_precios/por_libro/", response_model=List[LibroConPrecioModel], tags=["Lista de Precios"], summary="Obtener todos los libros, filtrando por el ID del libro",description="Obtener todos los libros con un id específico, incluyendo su editorial y precio.")
def obtener_libros_por_id_libro(id_libro: int):
    libros = ListaDePrecios.obtener_libros_por_id(id_libro)
    
    # Formateamos la respuesta con los datos de los libros, precios y nombre de la editorial
    respuesta = []
    
    for libro, precio, editorial in libros:
        libro_con_precio = LibroConPrecioModel(
            id_libro=libro.id_libro,
            titulo=libro.titulo,
            autor=libro.autor,
            isbn=libro.isbn,
            stock=libro.stock,
            id_genero=libro.id_genero,
            precio=precio,
            editorial=editorial,  # Incluye el nombre de la editorial
        )
        respuesta.append(libro_con_precio)
    
    return respuesta

# Endpoint GET para obtener libros y precios iguales a un precio específico
@router.get("/lista_precios/por_precio/", response_model=List[LibroConPrecioModel], tags=["Lista de Precios"], summary="Obtener todos los libros, indicando el precio",description="Obtener todos los libros cuyo precio sea igual al valor especificado.")
def obtener_libros_y_precio_por_precio(precio: float):
    libros = ListaDePrecios.obtener_libros_por_precio(precio)
    
    respuesta = []
    
    for libro, precio, editorial in libros:
        libro_con_precio = LibroConPrecioModel(
            id_libro=libro.id_libro,
            titulo=libro.titulo,
            autor=libro.autor,
            isbn=libro.isbn,
            stock=libro.stock,
            id_genero=libro.id_genero,
            precio=precio,
            editorial=editorial, 
        )
        respuesta.append(libro_con_precio)
    
    return respuesta

# Endpoint GET para obtener libros y precios mayores a un precio específico
@router.get("/lista_precios/por_precio_minimo/", response_model=List[LibroConPrecioModel], tags=["Lista de Precios"], summary="Obtener todos los libros, indicando el precio minimo",description="Obtener todos los libros cuyo precio sea mayor o igual al valor especificado.")
def obtener_libros_y_precio_por_precio_minimo(precio: float):
    libros = ListaDePrecios.obtener_libros_por_precio_minimo(precio)
    
    respuesta = []
    
    for libro, precio, editorial in libros:
        libro_con_precio = LibroConPrecioModel(
            id_libro=libro.id_libro,
            titulo=libro.titulo,
            autor=libro.autor,
            isbn=libro.isbn,
            stock=libro.stock,
            id_genero=libro.id_genero,
            precio=precio,
            editorial=editorial, 
        )
        respuesta.append(libro_con_precio)
    
    return respuesta

# Endpoint GET para obtener libros y precios menores a un precio específico
@router.get("/lista_precios/por_precio_maximo/", response_model=List[LibroConPrecioModel], tags=["Lista de Precios"], summary="Obtener todos los libros, indicando el precio maximo",description="Obtener todos los libros cuyo precio sea menor o igual al valor especificado.")
def obtener_libros_y_precio_por_precio_maximo(precio: float):
    libros = ListaDePrecios.obtener_libros_por_precio_maximo(precio)
    
    respuesta = []
    
    for libro, precio, editorial in libros:
        libro_con_precio = LibroConPrecioModel(
            id_libro=libro.id_libro,
            titulo=libro.titulo,
            autor=libro.autor,
            isbn=libro.isbn,
            stock=libro.stock,
            id_genero=libro.id_genero,
            precio=precio,
            editorial=editorial, 
        )
        respuesta.append(libro_con_precio)
    
    return respuesta

