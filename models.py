from pydantic import BaseModel
from typing import List

class ClienteModel(BaseModel):
    id_cliente: int = None
    nombre: str = None
    email: str = None
    telefono: str = None
    direccion: str = None

    class Config:
        from_attributes = True

class EditorialModel(BaseModel):
    id_editorial: int = None
    nombre: str = None
    razon_social: str = None
    cuit: str = None
    direccion: str = None
    telefono: str = None
    mail: str = None

    class Config:
        from_attributes = True

class GeneroModel(BaseModel):
    id_genero: int = None
    nombre: str = None

    class Config:
        from_attributes = True

class LibroModel(BaseModel):
    id_libro: int = None
    titulo: str = None
    autor: str = None
    isbn: str = None
    stock: int = None
    id_genero: int = None

    class Config:
        from_attributes = True

# class LibroConGenero(BaseModel):
#     id_libro: int = None
#     titulo: str = None
#     autor: str = None
#     isbn: str = None
#     stock: int = None
#     id_genero: int = None

#     class Config:
#         from_attributes = True

class ListaDePreciosModel(BaseModel):
    id_lista_precio: int = None
    id_editorial: int  = None
    id_libro: int = None
    precio: float = None

    class Config:
        from_attributes = True

class LibroConPrecioModel(BaseModel):
    id_libro: int = None
    titulo: str = None
    autor: str = None
    isbn: str = None
    precio: float = None
    stock: int = None
    id_genero: int = None

    class Config:
        from_attributes = True

