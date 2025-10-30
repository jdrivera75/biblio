from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session  # CORREGIDO: usar SQLAlchemy
from database import engine
import crud
from models import Libro, Autor
from esquemas import LibroCreate, LibroUpdate, LibroRead, AutorRead

router = APIRouter(prefix="/libros", tags=["Libros"])

@router.post("/", response_model=LibroRead, status_code=status.HTTP_201_CREATED)
def crear(new_libro: LibroCreate):
    with Session(engine) as session:
        return crud.crear_libro(session, new_libro)

@router.get("/", response_model=list[LibroRead])
def listar():
    with Session(engine) as session:
        return crud.listar_libros(session)

@router.get("/{libro_id}", response_model=LibroRead)
def obtener(libro_id: int):
    with Session(engine) as session:
        libro = crud.obtener_libro(session, libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return libro

@router.patch("/{libro_id}", response_model=LibroRead)
def actualizar(libro_id: int, datos: LibroUpdate):
    with Session(engine) as session:
        libro = crud.actualizar_libro(session, libro_id, datos)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return libro

@router.delete("/{libro_id}")
def eliminar(libro_id: int):
    with Session(engine) as session:
        exito = crud.eliminar_libro(session, libro_id)
        if not exito:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return {"message": "Libro eliminado correctamente"}

@router.get("/{libro_id}/autor", response_model=AutorRead)
def autor_del_libro(libro_id: int):
    with Session(engine) as session:
        autor = crud.obtener_libro(session, libro_id).autor
        if not autor:
            raise HTTPException(status_code=404, detail="Autor no encontrado")
        return autor
