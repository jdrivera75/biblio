from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from database import engine
import crud
from models import Libro, Autor
from esquemas import LibroCreate, LibroUpdate, LibroRead, AutorRead

router = APIRouter(prefix="/libros", tags=["Libros"])

@router.post("/", response_model=LibroRead, status_code=status.HTTP_201_CREATED)
def crear_libro(data: LibroCreate):
    with Session(engine) as session:
        return crud.crear_libro(session, data)

@router.get("/", response_model=list[LibroRead])
def listar_libros():
    with Session(engine) as session:
        return crud.listar_libros(session)

@router.get("/{libro_id}", response_model=LibroRead)
def obtener_libro(libro_id: int):
    with Session(engine) as session:
        return crud.obtener_libro(session, libro_id)

@router.patch("/{libro_id}", response_model=LibroRead)
def actualizar_libro(libro_id: int, data: LibroUpdate):
    with Session(engine) as session:
        return crud.actualizar_libro(session, libro_id, data)

@router.delete("/{libro_id}")
def eliminar_libro(libro_id: int):
    with Session(engine) as session:
        return crud.eliminar_libro(session, libro_id)

@router.get("/{libro_id}/autor", response_model=AutorRead)
def autor_del_libro(libro_id: int):
    with Session(engine) as session:
        libro = crud.obtener_libro(session, libro_id)
        if not libro.autor:
            raise HTTPException(status_code=404, detail="Autor no encontrado")
        return libro.autor
