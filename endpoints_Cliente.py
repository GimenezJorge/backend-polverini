from fastapi import APIRouter, HTTPException
from typing import List
from Cliente import Cliente  
from models import ClienteModel 

router = APIRouter()

# Endpoint POST para registrar un nuevo cliente
@router.post("/clientes/nuevo/", tags=["Clientes"], summary="Registrar un nuevo cliente", description="Este endpoint crea un nuevo cliente en la base de datos.")
def agregar_cliente(cliente: ClienteModel):
    Cliente.agregar_cliente(cliente)
    return {"message": "Cliente registrado exitosamente"}

# Endpoint GET para obtener todos los clientes
@router.get("/clientes/", response_model=List[ClienteModel], tags=["Clientes"], summary="Obtener todos los clientes", description="Este endpoint devuelve una lista de todos los clientes registrados en la base de datos.")
def obtener_clientes():
    clientes = Cliente.mostrar_todos()
    return clientes

# Endpoint GET para buscar clientes por nombre
@router.get("/clientes/buscar/", response_model=List[ClienteModel], tags=["Clientes"], summary="Buscar clientes por nombre", description="Devuelve todos los clientes cuyo nombre coincida parcial o totalmente.")
def buscar_clientes(nombre: str):
    clientes = Cliente.obtener_por_nombre(nombre)
    if not clientes:
        raise HTTPException(status_code=404, detail="No se encontraron clientes con ese nombre")
    return clientes

# Endpoint GET para obtener un cliente por ID
@router.get("/clientes/{cliente_id}", response_model=ClienteModel, tags=["Clientes"], summary="Obtener un cliente por ID", description="Este endpoint devuelve los datos de un cliente específico.")
def obtener_cliente(cliente_id: int):
    cliente = Cliente.obtener_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente con id {cliente_id} no encontrado")
    return cliente

# Endpoint PUT para modificar un cliente
@router.put("/clientes/{cliente_id}", tags=["Clientes"], summary="Modificar un cliente", description="Este endpoint modifica los datos de un cliente específico identificado por su ID.")
def modificar_cliente(cliente_id: int, cliente_in: ClienteModel):
    try:
        Cliente.modificar_cliente(cliente_id, cliente_in)
        return {"message": "Cliente modificado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint DELETE para eliminar un cliente
@router.delete("/clientes/{cliente_id}", tags=["Clientes"], summary="Eliminar un cliente", description="Este endpoint elimina un cliente específico identificado por su ID.")
def eliminar_cliente(cliente_id: int):
    if not Cliente.eliminar_cliente(cliente_id):
        raise HTTPException(status_code=404, detail=f"Cliente con id {cliente_id} no encontrado")
    return {"message": f"Cliente con id {cliente_id} eliminado correctamente"}
