from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Nombre de la base de datos para el proyecto de biblioteca
DATABASE_URL = "sqlite:///bibliotecagestion.db"

# engine y sesión
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # requerido para SQLite en entornos multi-thread
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos SQLAlchemy (usado en models.py)
Base = declarative_base()


def create_tables():
    """Crea las tablas en la base de datos (llamar al iniciar la app)."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Generador para dependencias de FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# alias para usar en imports (similar al original)
SessionDep = SessionLocal