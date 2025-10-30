from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ------------------------------
# CONFIGURACIÓN DE LA BASE DE DATOS
# ------------------------------

# Crear el motor de base de datos SQLite
engine = create_engine(
    "sqlite:///biblioteca.db",  # El archivo SQLite se llamará biblioteca.db
    echo=True,                  # Muestra en consola las consultas SQL ejecutadas
    connect_args={"check_same_thread": False}  # Necesario para SQLite con threads
)

# Base declarativa para definir los modelos
Base = declarative_base()

# Crear la sesión de base de datos
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)
