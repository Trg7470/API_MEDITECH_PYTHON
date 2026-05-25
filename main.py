from fastapi import FastAPI, HTTPException, Depends
from bson import ObjectId

from database import get_connection
from mongodb import pagos_nomina
from schemas import Login, Empleado, Pagotiomina
from auth import crear_token, verificar_token

app = FastAPI(
title = "API RESTful Hibrida de Nómina",
description = "API con FastAPI, PostgreSQL, MongoDB y JWT",
version="1.0")

@app.get("/")
def inicio():
    return {"mensaje": "API híbrida de nómina funcionando correctamente"}

#LOGIN CON JWT
@app.post("/login")
def login(usuario: Login):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" SELECT *FROM usuarios
    where nombre_usuario = %s AND contrasena = %s """,
    (usuario.nombre_usuario,usuario.contrasena)
    )

    usuario_bd = cursor.fetchone()
    cursor.close()
    conn.close()

    if not usuario_bd:
        raise HTTPException(status_code=401, detail= "Credenciales incorrectas")

    token = crear_token({
        "sub": usuario.nombre_usuario,
        "rol": usuario_bd["rol"]
    })

    return{
        "access_token":token,
        "token_type":"bearer"
    }
    