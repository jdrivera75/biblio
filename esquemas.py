from pydantic import BaseModel
from typing import Optional, List

# ---------- LIBRO ----------
class LibroBase(BaseModel):
    titulo: str
    genero: Optional[str] = None
    anio_publicacion: Optional[int] = None

class LibroCreate(LibroBase):
    pass

class LibroUpdate(BaseModel):
    titulo: Optional[str] = None
    genero: Optional[str] = None
    anio_publicacion: Optional[int] = None
    autor_id: Optional[int] = None
    isbn: Optional[str] = None
    copias_disponibles: Optional[int] = None

class LibroRead(LibroBase):
    id: int
    autor_id: Optional[int] = None

    class Config:
        # Para Pydantic v2: reemplaza orm_mode por from_attributes
        from_attributes = True


# ---------- AUTOR ----------
class AutorBase(BaseModel):
    nombre: str
    nacionalidad: Optional[str] = None
    edad: Optional[int] = None

class AutorCreate(AutorBase):
    pass

class AutorUpdate(BaseModel):
    nombre: Optional[str] = None
    nacionalidad: Optional[str] = None
    edad: Optional[int] = None

class AutorRead(AutorBase):
    id: int
    libros: List[LibroRead] = []

    class Config:
        from_attributes = True
