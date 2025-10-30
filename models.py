from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    nacionalidad = Column(String, nullable=True)
    edad = Column(Integer, nullable=True)

    # Relación uno -> muchos (Autor tiene muchos libros)
    libros = relationship("Libro", back_populates="autor", cascade="save-update")


class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    genero = Column(String, nullable=True)
    anio_publicacion = Column(Integer, nullable=True)

    # Campos opcionales adicionales (ISBN y número de copias)
    isbn = Column(String, unique=True, nullable=True, index=True)
    copias_disponibles = Column(Integer, nullable=True, default=0)

    # FK hacia Autor
    autor_id = Column(Integer, ForeignKey("autores.id"), nullable=True)

    # Relación muchos -> uno
    autor = relationship("Autor", back_populates="libros")
