from fastapi import FastAPI, HTTPException
from bson import ObjectId
import bcrypt

from database import get_connection
from mongodb import MongoClient
from schemas import Login
from auth import crear_token, verificar_token

app = FastAPI(
    title="API RESTful Hibrida de MEDITECH PLANIFAM",
    description="API con FastAPI, PostgreSQL, MongoDB y JWT",
    version="1.0"
)

@app.get("/")
def inicio():
    return {"mensaje": "API híbrida de nómina funcionando correctamente"}


# LOGIN CON JWT
@app.post("/login")
def login(usuario: Login):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_usuario, correo, contrasena, tipo_usuario
        FROM Usuarios
        WHERE correo = %s
    """, (usuario.email,))

    usuario_bd = cursor.fetchone()

    cursor.close()
    conn.close()

    if not usuario_bd:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    contrasena_hash = usuario_bd["contrasena"]

    password_valido = bcrypt.checkpw(
        usuario.password.encode("utf-8"),
        contrasena_hash.encode("utf-8")
    )

    if not password_valido:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    token = crear_token({
        "id_usuario": usuario_bd["id_usuario"],
        "tipo_usuario": usuario_bd["tipo_usuario"],
        "sub": usuario_bd["correo"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

