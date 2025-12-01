from fastapi import APIRouter, HTTPException
from typing import List
from Editorial import Editorial
from models import EditorialModel 

router = APIRouter()

# Endpoint POST para agregar una editorial
@router.post("/editoriales/nueva/", tags=["Editoriales"], summary="Crear una nueva editorial", description="Este endpoint crea una nueva editorial en la base de datos.")
def agregar_editorial(editorial: EditorialModel):
    Editorial.agregar_editorial(editorial)
    return {"message": "Editorial creada exitosamente"}

# Endpoint GET para obtener todas las editoriales
@router.get("/editoriales/", response_model=List[EditorialModel], tags=["Editoriales"], summary="Obtener todas las editoriales", description="Este endpoint devuelve una lista de todas las editoriales registradas en la base de datos.")
def obtener_editoriales():
    editoriales = Editorial.mostrar_todos()
    return editoriales

# Endpoint GET para buscar editoriales por nombre
@router.get("/editoriales/buscar/", response_model=List[EditorialModel], tags=["Editoriales"], summary="Buscar editoriales por nombre", description="Devuelve todas las editoriales cuyo nombre coincida parcial o totalmente.")
def buscar_editoriales(nombre: str):
    editoriales = Editorial.obtener_por_nombre(nombre)
    if not editoriales:
        raise HTTPException(status_code=404, detail="No se encontraron editoriales con ese nombre")
    return editoriales

# Endpoint PUT para modificar una editorial
@router.put("/editoriales/{editorial_id}", tags=["Editoriales"], summary="Modificar una editorial", description="Este endpoint modifica los datos de una editorial específica identificada por su ID.")
def modificar_editorial(editorial_id: int, editorial_in: EditorialModel):
    try:
        Editorial.modificar_editorial(editorial_id, editorial_in)
        return {"message": "Editorial modificada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint DELETE para eliminar una editorial
@router.delete("/editoriales/{editorial_id}", tags=["Editoriales"], summary="Eliminar una editorial", description="Este endpoint elimina una editorial específica identificada por su ID.")
def eliminar_editorial(editorial_id: int):
    if not Editorial.eliminar_editorial(editorial_id):
        raise HTTPException(status_code=404, detail=f"Editorial con id {editorial_id} no encontrada")
    return {"message": f"Editorial con id {editorial_id} eliminada correctamente"}
