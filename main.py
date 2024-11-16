'''
instalado:
FastAPI (completo, incluido jinja2 y uvicorn)
sql server management estudio 20
sql server (evaluation version)
python 3.12.4 (64-bit)
pyodbc
SQLAlchemy
Microsoft ODBC Driver 18 for SQL Server (x64) version 18.3.3.1
Microsoft Visual C++ Redistributable (version 14.40.33810.0)
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints_Editorial import router as router_editorial
from endpoints_Cliente import router as router_cliente 
from endpoints_Genero import router as genero_router
from endpoints_Libro import router as router_libro
from endpoints_ListaDePrecios import router as lista_precios_router

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost",
    "http://127.0.0.1:8000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye los endpoints de api.py
app.include_router(router_editorial)
app.include_router(router_cliente)
app.include_router(genero_router)
app.include_router(router_libro)
app.include_router(lista_precios_router)