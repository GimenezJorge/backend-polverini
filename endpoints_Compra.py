from fastapi import APIRouter
from models import CompraModel
from Compra import Compra

router = APIRouter()

@router.post("/compras/nueva/", tags=["Compras"], summary="Registrar una nueva compra", description="Este endpoint crea una nueva compra en la base de datos.")
def agregar_compra(compra: CompraModel):
    Compra.agregar_compra(compra)
    return {"message": "Compra registrada exitosamente"}


