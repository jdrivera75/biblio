from fastapi import FastAPI
from database import create_tables
from router_autores import router as router_autores
from router_libros import router as router_libros

app = FastAPI(title="Sistema de Biblioteca")

# Crea las tablas al iniciar la aplicación
create_tables()

# Registrar routers
app.include_router(router_autores)
app.include_router(router_libros)


@app.get("/")
def root():
    return {"mensaje": "API del sistema de biblioteca funcionando correctamente "}