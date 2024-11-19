from fastapi import APIRouter, HTTPException
from models import VentaModel
from Venta import Venta

router = APIRouter()

@router.post("/ventas/nueva/", tags=["Ventas"], summary="Registrar una nueva venta", description="Este endpoint registra una nueva venta y sus detalles. Para agregar libros, indicar 'id_libro', 'cantidad' y 'precio'.")
def agregar_venta(venta: VentaModel):
    Venta.agregar_venta(venta)
    return {"message": "Venta registrada exitosamente"}

@router.get("/ventas/", tags=["Ventas"], summary="Obtener todas las ventas", description="Este endpoint devuelve todas las ventas con sus detalles.")
def obtener_ventas():
    try:
        ventas = Venta.obtener_ventas()
        return ventas
    except HTTPException as e:
        raise e

@router.get("/ventas/cliente/{id_cliente}", tags=["Ventas"], summary="Obtener ventas por cliente", description="Este endpoint devuelve todas las ventas de un cliente específico con sus detalles y el total de ventas.")
async def obtener_ventas_por_cliente(id_cliente: int):
    try:
        # Obtener las ventas filtradas por id_cliente
        ventas = Venta.obtener_ventas_por_cliente(id_cliente)
        return ventas
    except HTTPException as e:
        raise e
