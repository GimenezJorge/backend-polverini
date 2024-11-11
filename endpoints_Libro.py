from fastapi import APIRouter
from models import LibroCreate  # Asegúrate de importar el modelo correcto
from Libro import Libro
from models import LibroCreate  # Asegúrate de que ambas clases están importadas

router = APIRouter()

@router.post("/libros/nuevo/", tags=["Libros"], summary="Agregar un nuevo libro", description="Este endpoint permite agregar un nuevo libro a la base de datos.")
async def agregar_libro(libro: LibroCreate):
    try:
        # Llamar al método agregar_libro de la clase Libro y pasar los parámetros correctos
        nuevo_libro = Libro.agregar_libro(
            titulo=libro.titulo,
            autor=libro.autor,
            isbn=libro.isbn,
            precio=libro.precio,
            stock=libro.stock,
            id_genero=libro.id_genero
        )
        return {"message": "Libro agregado exitosamente", "id_libro": nuevo_libro.id_libro}
    except Exception as e:
        return {"error": str(e)}

@router.get("/libros/", tags=["Libros"], description="Obtener todos los libros")
async def mostrar_libros():
    try:
        libros = Libro.obtener_libros()
        return libros
    except Exception as e:
        return {"error": str(e)}
