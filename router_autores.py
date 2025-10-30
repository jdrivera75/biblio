from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_session
from crud import (
    crear_autor,
    listar_autores,
    obtener_autor,
    actualizar_autor,
    eliminar_autor,
    libros_por_autor
)
from esquemas import AutorCreate, AutorUpdate, AutorRead, LibroRead

router = APIRouter(prefix="/autores", tags=["Autores"])


@router.post("/", response_model=AutorRead, status_code=status.HTTP_201_CREATED)
def api_crear_autor(data: AutorCreate, db: Session = Depends(get_session)):
    return crear_autor(db, data)


@router.get("/", response_model=List[AutorRead])
def api_listar_autores(nacionalidad: Optional[str] = None, db: Session = Depends(get_session)):
    return listar_autores(db, nacionalidad)


@router.get("/{autor_id}", response_model=AutorRead)
def api_obtener_autor(autor_id: int, db: Session = Depends(get_session)):
    return obtener_autor(db, autor_id)


@router.put("/{autor_id}", response_model=AutorRead)
def api_actualizar_autor(autor_id: int, data: AutorUpdate, db: Session = Depends(get_session)):
    return actualizar_autor(db, autor_id, data)


@router.delete("/{autor_id}", status_code=status.HTTP_200_OK)
def api_eliminar_autor(autor_id: int, db: Session = Depends(get_session)):
    return eliminar_autor(db, autor_id)


@router.get("/{autor_id}/libros", response_model=List[LibroRead])
def api_libros_por_autor(autor_id: int, db: Session = Depends(get_session)):
    return libros_por_autor(db, autor_id)
