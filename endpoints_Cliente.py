from fastapi import APIRouter, HTTPException
from typing import List
from Cliente import Cliente  # Asegúrate de tener la clase Cliente importada
from models import ClienteModel 

router = APIRouter()

# Endpoint POST para registrar un nuevo cliente
@router.post("/clientes/nuevo/", tags=["Clientes"], summary="Registrar un nuevo cliente", description="Este endpoint crea un nuevo cliente en la base de datos.")
def registrar_cliente(cliente: ClienteModel):
    nuevo_cliente = Cliente.registrar_cliente(
        nombre=cliente.nombre,
        email=cliente.email,
        telefono=cliente.telefono,
        direccion=cliente.direccion
    )
    return {"message": "Cliente registrado exitosamente", "cliente": nuevo_cliente}

# Endpoint GET para obtener todos los clientes
@router.get("/clientes/", response_model=List[ClienteModel], tags=["Clientes"], summary="Obtener todos los clientes", description="Este endpoint devuelve una lista de todos los clientes registrados en la base de datos.")
def obtener_clientes():
    clientes = Cliente.mostrar_todos()
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
        cliente_existente = Cliente.modificar_cliente(cliente_id, 
            nombre=cliente_in.nombre,
            email=cliente_in.email,
            telefono=cliente_in.telefono,
            direccion=cliente_in.direccion
        )
        return {"message": "Cliente modificado correctamente", "cliente": cliente_existente}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint DELETE para eliminar un cliente
@router.delete("/clientes/{cliente_id}", tags=["Clientes"], summary="Eliminar un cliente", description="Este endpoint elimina un cliente específico identificado por su ID.")
def eliminar_cliente(cliente_id: int):
    if not Cliente.eliminar_cliente(cliente_id):
        raise HTTPException(status_code=404, detail=f"Cliente con id {cliente_id} no encontrado")
    return {"message": f"Cliente con id {cliente_id} eliminado correctamente"}
