from pydantic import BaseModel

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

class ClienteModel(BaseModel):
    id_cliente: int = None
    nombre: str = None
    email: str = None
    telefono: str = None
    direccion: str = None

    class Config:
        from_attributes = True


class Genero(BaseModel):
    id_genero: int
    nombre: str

    class Config:
        from_attributes = True


class LibroCreate(BaseModel):
    titulo: str
    autor: str
    isbn: str
    precio: float
    stock: int
    id_genero: int

class LibroModel(BaseModel):
    id_libro: int
    titulo: str
    autor: str
    isbn: str
    precio: float
    stock: int
    id_genero: int

    class Config:
        from_attributes = True

class ListaDePreciosModel(BaseModel):
    id_lista_precio: int = None
    id_editorial: int
    id_libro: int
    precio: float

    class Config:
        from_attributes = True
