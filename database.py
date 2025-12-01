from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Aquí defines tu cadena de conexión
server = r'JLG\SQLEXPRESS'
database = 'bdg3'

connection_string = (
    f'mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server'
    '&TrustServerCertificate=yes'
)

"""
#CONEXION DE LA ESCUELA:
server = 'sqlserver\\sqlserver'
database = 'bdg3'
username = 'bdg3'
password = 'bdg3'
driver = 'ODBC Driver 18 for SQL Server'

# Construcción de la cadena de conexión usando las variables
connection_string = (
    f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
    '&TrustServerCertificate=yes'
)
"""
"""
# Pruebo la conexión
try:
    engine = create_engine(connection_string)
    print("Conexión exitosa!")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
"""

# Crear el motor de SQLAlchemy
engine = create_engine(connection_string)

# Declarar la clase base
Base = declarative_base()

# Crear una instancia de sessionmaker para reutilizar en las operaciones de sesión
SessionLocal = sessionmaker(bind=engine)
