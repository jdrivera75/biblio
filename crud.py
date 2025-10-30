from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Autor, Libro
from esquemas import AutorCreate, AutorUpdate, LibroCreate, LibroUpdate


# -------------------
#  CRUD AUTORES
# -------------------
def crear_autor(db: Session, data: AutorCreate) -> Autor:
    """
    Crea un nuevo autor.
    - No hay restricción de unicidad sobre el nombre por defecto,
      pero puedes agregarla si lo deseas.
    """
    autor = Autor(
        nombre=data.nombre,
        nacionalidad=getattr(data, "nacionalidad", None),
        edad=getattr(data, "edad", None)
    )
    db.add(autor)
    db.commit()
    db.refresh(autor)
    return autor


def listar_autores(db: Session, nacionalidad: Optional[str] = None) -> List[Autor]:
    """
    Lista autores, opcionalmente filtrando por nacionalidad.
    """
    query = db.query(Autor)
    if nacionalidad is not None:
        query = query.filter(Autor.nacionalidad == nacionalidad)

    autores = query.all()
    if not autores:
        raise HTTPException(status_code=404, detail="No se encontraron autores con esos filtros")
    return autores


def obtener_autor(db: Session, autor_id: int) -> Autor:
    autor = db.get(Autor, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor


def actualizar_autor(db: Session, autor_id: int, data: AutorUpdate) -> Autor:
    autor = db.get(Autor, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(autor, campo, valor)

    db.add(autor)
    db.commit()
    db.refresh(autor)
    return autor


def eliminar_autor(db: Session, autor_id: int):
    """
    Elimina un autor. Regla aplicada: los libros asociados se desasignan
    (se establece autor_id = None) en lugar de eliminar los libros.
    """
    autor = db.get(Autor, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    # Desasignar libros del autor antes de eliminarlo
    libros = db.query(Libro).filter(Libro.autor_id == autor_id).all()
    for libro in libros:
        libro.autor_id = None
        db.add(libro)

    db.delete(autor)
    db.commit()
    return {"mensaje": "Autor eliminado correctamente"}


# -------------------
#  CRUD LIBROS
# -------------------
def crear_libro(db: Session, data: LibroCreate) -> Libro:
    """
    Crea un libro validando:
      - ISBN único (si se usa campo isbn)
      - copias_disponibles >= 0
      - si se proporciona autor_id, el autor debe existir
    """
    # Validar ISBN único si el esquema trae isbn
    isbn_val = getattr(data, "isbn", None)
    if isbn_val is not None:
        existente = db.query(Libro).filter(Libro.isbn == isbn_val).first()
        if existente:
            raise HTTPException(status_code=409, detail="Ya existe un libro con ese ISBN")

    # Validar copias >= 0 si existe el campo
    copias = getattr(data, "copias_disponibles", None)
    if copias is not None and copias < 0:
        raise HTTPException(status_code=400, detail="copias_disponibles debe ser mayor o igual a 0")

    # Validar autor (si se envía autor_id)
    autor_id = getattr(data, "autor_id", None)
    if autor_id is not None:
        autor = db.get(Autor, autor_id)
        if not autor:
            raise HTTPException(status_code=404, detail="Autor especificado no existe")

    libro = Libro(
        titulo=data.titulo,
        genero=getattr(data, "genero", None),
        anio_publicacion=getattr(data, "anio_publicacion", None),
        autor_id=autor_id,
        isbn=isbn_val,
        copias_disponibles=copias
    )
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro


def listar_libros(
    db: Session,
    genero: Optional[str] = None,
    anio: Optional[int] = None,
    autor_id: Optional[int] = None
) -> List[Libro]:
    """
    Lista libros con filtros opcionales: genero, año y autor.
    """
    query = db.query(Libro)
    if genero is not None:
        query = query.filter(Libro.genero == genero)
    if anio is not None:
        query = query.filter(Libro.anio_publicacion == anio)
    if autor_id is not None:
        query = query.filter(Libro.autor_id == autor_id)

    libros = query.all()
    if not libros:
        raise HTTPException(status_code=404, detail="No se encontraron libros con esos filtros")
    return libros


def obtener_libro(db: Session, libro_id: int) -> Libro:
    libro = db.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


def actualizar_libro(db: Session, libro_id: int, data: LibroUpdate) -> Libro:
    libro = db.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    # Si se cambia el ISBN, asegurar unicidad
    new_isbn = getattr(data, "isbn", None)
    if new_isbn is not None and new_isbn != getattr(libro, "isbn", None):
        existente = db.query(Libro).filter(Libro.isbn == new_isbn).first()
        if existente:
            raise HTTPException(status_code=409, detail="Ya existe un libro con ese ISBN nuevo")

    # Si se cambia autor_id, validar existencia del autor
    new_autor_id = getattr(data, "autor_id", None)
    if new_autor_id is not None and new_autor_id != getattr(libro, "autor_id", None):
        autor = db.get(Autor, new_autor_id)
        if not autor:
            raise HTTPException(status_code=404, detail="Autor nuevo no encontrado")

    # Validar copias si se proporciona
    copias = getattr(data, "copias_disponibles", None)
    if copias is not None and copias < 0:
        raise HTTPException(status_code=400, detail="copias_disponibles debe ser mayor o igual a 0")

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(libro, campo, valor)

    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro


def eliminar_libro(db: Session, libro_id: int):
    libro = db.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    db.delete(libro)
    db.commit()
    return {"mensaje": "Libro eliminado correctamente"}


def libros_por_autor(db: Session, autor_id: int) -> List[Libro]:
    autor = db.get(Autor, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    libros = db.query(Libro).filter(Libro.autor_id == autor_id).all()
    if not libros:
        raise HTTPException(status_code=404, detail="Este autor no tiene libros registrados")
    return libros


# -------------------
#  Acciones auxiliares (asignar / desasignar)
# -------------------
def asignar_autor_a_libro(db: Session, libro_id: int, autor_id: int) -> Libro:
    """
    Asigna un autor a un libro (si ambos existen).
    """
    libro = db.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    autor = db.get(Autor, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    libro.autor_id = autor_id
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro


def desasignar_libro(db: Session, libro_id: int) -> Libro:
    """
    Remueve la relación libro -> autor (autor_id = None).
    """
    libro = db.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    libro.autor_id = None
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro
