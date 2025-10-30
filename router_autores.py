from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from database import engine
import crud
from models import Autor
from esquemas import AutorCreate, AutorUpdate, AutorRead

router = APIRouter(prefix="/autores", tags=["Autores"])

@router.post("/", response_model=AutorRead, status_code=status.HTTP_201_CREATED)
def crear_autor(data: AutorCreate):
    with Session(engine) as session:
        return crud.crear_autor(session, data)

@router.get("/", response_model=list[AutorRead])
def listar_autores(nacionalidad: str = None):
    with Session(engine) as session:
        return crud.listar_autores(session, nacionalidad)

@router.get("/{autor_id}", response_model=AutorRead)
def obtener_autor(autor_id: int):
    with Session(engine) as session:
        return crud.obtener_autor(session, autor_id)

@router.patch("/{autor_id}", response_model=AutorRead)
def actualizar_autor(autor_id: int, data: AutorUpdate):
    with Session(engine) as session:
        return crud.actualizar_autor(session, autor_id, data)

@router.delete("/{autor_id}")
def eliminar_autor(autor_id: int):
    with Session(engine) as session:
        return crud.eliminar_autor(session, autor_id)
