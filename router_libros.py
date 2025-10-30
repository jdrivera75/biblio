from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from models import Libro, Autor
from esquemas import LibroCreate, LibroRead, LibroUpdate  # o esquemas import según cómo lo nombraste

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.post("/", response_model=LibroRead, status_code=status.HTTP_201_CREATED)
def crear_libro(data: LibroCreate, db: Session = Depends(get_session)):
    # Verificar que exista el autor indicado (si se envía autor_id)
    if data.autor_id is not None:
        autor = db.query(Autor).get(data.autor_id)
        if not autor:
            raise HTTPException(status_code=404, detail="Autor no encontrado")

    libro = Libro(
        titulo=data.titulo,
        genero=data.genero,
        anio_publicacion=data.anio_publicacion,
        autor_id=data.autor_id
    )
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro


@router.get("/", response_model=List[LibroRead])
def listar_libros(genero: Optional[str] = None, anio: Optional[int] = None, db: Session = Depends(get_session)):
    query = db.query(Libro)
    if genero is not None:
        query = query.filter(Libro.genero == genero)
    if anio is not None:
        query = query.filter(Libro.anio_publicacion == anio)

    libros = query.all()
    if not libros:
        raise HTTPException(status_code=404, detail="No se encontraron libros con esos filtros")
    return libros


@router.get("/{libro_id}", response_model=LibroRead)
def obtener_libro(libro_id: int, db: Session = Depends(get_session)):
    libro = db.query(Libro).get(libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@router.put("/{libro_id}", response_model=LibroRead)
def actualizar_libro(libro_id: int, data: LibroUpdate, db: Session = Depends(get_session)):
    libro = db.query(Libro).get(libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    # Si se cambia el autor, validar que exista
    if data.autor_id is not None and data.autor_id != libro.autor_id:
        autor = db.query(Autor).get(data.autor_id)
        if not autor:
            raise HTTPException(status_code=404, detail="Autor nuevo no encontrado")

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(libro, campo, valor)

    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro


@router.delete("/{libro_id}")
def eliminar_libro(libro_id: int, db: Session = Depends(get_session)):
    libro = db.query(Libro).get(libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    db.delete(libro)
    db.commit()
    return {"mensaje": "Libro eliminado correctamente"}


@router.get("/autor/{autor_id}", response_model=List[LibroRead])
def libros_por_autor(autor_id: int, db: Session = Depends(get_session)):
    autor = db.query(Autor).get(autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    libros = db.query(Libro).filter(Libro.autor_id == autor_id).all()
    if not libros:
        raise HTTPException(status_code=404, detail="Este autor no tiene libros registrados")
    return libros
