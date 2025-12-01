from fastapi import APIRouter, HTTPException
from models import CompraModel
from Compra import Compra
from datetime import date
from fastapi import Query

router = APIRouter()

@router.post("/compras/nueva/", tags=["Compras"], summary="Registrar una nueva compra", description="Este endpoint registra una nueva los detalles en la tabla correspondiente. Para agregar libros, indicar 'id_libro', 'cantidad' y 'precio' dentro de 'Detalles'")
def agregar_compra(compra: CompraModel):
    Compra.agregar_compra(compra)
    return {"message": "Compra registrada exitosamente"}

@router.get("/compras/", tags=["Compras"], summary="Obtener todas las compras", description="Este endpoint devuelve todas las compras con sus detalles.")
def obtener_compras():
    try:
        compras = Compra.obtener_compras()
        return compras
    except HTTPException as e:
        raise e

@router.get("/compras/editorial/{id_editorial}", tags=["Compras"], summary="Obtener compras por editorial", description="Este endpoint devuelve todas las compras de una editorial específica con sus detalles y el total de compras.")
async def obtener_compras_por_editorial(id_editorial: int):
    try:
        # Obtener las compras filtradas por id_editorial
        compras = Compra.obtener_compras_por_editorial(id_editorial)
        return compras
    except HTTPException as e:
        raise e
    
@router.get(
    "/compras/filtrar/",
    tags=["Compras"],
    summary="Filtrar compras por fecha",
    description="Permite filtrar compras por fecha exacta, por rango, por año o por mes."
)
def filtrar_compras(
    fecha: date = Query(None),
    desde: date = Query(None),
    hasta: date = Query(None),
    año: int = Query(None),
    mes: int = Query(None)
):
    return Compra.obtener_compras_por_fecha(fecha, desde, hasta, año, mes)
