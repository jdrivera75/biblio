from pydantic import BaseModel
from typing import Optional, List

# ---------- LIBRO ----------
class LibroBase(BaseModel):
    titulo: str
    genero: Optional[str] = None
    anio_publicacion: Optional[int] = None

class LibroCreate(LibroBase):
    pass

class LibroRead(LibroBase):
    id: int
    autor_id: Optional[int] = None

    class Config:
        orm_mode = True


# ---------- AUTOR ----------
class AutorBase(BaseModel):
    nombre: str
    nacionalidad: Optional[str] = None
    edad: Optional[int] = None

class AutorCreate(AutorBase):
    pass

class AutorRead(AutorBase):
    id: int
    libros: List[LibroRead] = []

    class Config:
        orm_mode = True
