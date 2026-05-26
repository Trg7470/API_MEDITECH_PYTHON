from fastapi import FastAPI, HTTPException, Depends
from bson import ObjectId
import bcrypt
from datetime import datetime

from database import get_connection
from mongodb import client, db, expediente_medico
from schemas import Login, Expediente_Medico, Usuarios, Pacientes, Monitoreo, PlanPersonalizado
from auth import crear_token, verificar_token

app = FastAPI(
    title="API RESTful MEDITECH_PLANIFAM",
    description="API con FastAPI, PostgreSQL, MongoDB y JWT",
    version="1.0"
)

@app.get("/")
def inicio():
    return {"mensaje": "API híbrida de MEDITECH PLANIFAM funcionando correctamente"}


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

# Usuarios
# Obtener Usuarios
@app.get("/u/get")
def obtener_usuarios(access: str = Depends(verificar_token)):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
            SELECT Id_Usuario, Nombre, Apellido_Paterno, Apellido_Materno, Sexo, Fecha_Nacimiento, Direccion, Telefono, Especialidad, Cedula_Prof, Correo, Fecha_Registro,
            Estado, Tipo_Usuario, User_Key FROM Usuarios ORDER BY Id_Usuario ASC  
        """)

    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"usuarios": usuarios}

@app.post("/u/create")
def crear_usuario(usuario: Usuarios, access: str = Depends(verificar_token)):
    conn = get_connection()
    cursor = conn.cursor()

    contrasena_hash = bcrypt.hashpw(
        usuario.contrasena.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    cursor.execute("""
        INSERT INTO Usuarios (Nombre, Apellido_Paterno, Apellido_Materno, Sexo, Fecha_Nacimiento,
        Direccion, Telefono, Especialidad, Cedula_Prof, Correo, Contrasena, Fecha_Registro,
        Estado, Tipo_Usuario, User_Key)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING Id_Usuario
    """, (
        usuario.nombre,
        usuario.apellido_paterno,
        usuario.apellido_materno,
        usuario.sexo,
        usuario.fecha_nacimiento,
        usuario.direccion,
        usuario.telefono,
        usuario.especialidad,
        usuario.cedula_prof,
        usuario.correo,
        contrasena_hash,
        usuario.fecha_registro,
        usuario.estado,
        usuario.tipo_usuario,
        usuario.user_key
    ))

    nuevo_usuario_id = cursor.fetchone()["id_usuario"]

    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Usuario creado exitosamente", "id_usuario": nuevo_usuario_id}

@app.put("/u/update/{id_usuario}")
def actualizar_usuario(id_usuario: int, usuario: Usuarios, access: str = Depends(verificar_token)):
    conn = get_connection()
    cursor = conn.cursor()

    contrasena_hash = bcrypt.hashpw(
        usuario.contrasena.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    cursor.execute("""
        UPDATE Usuarios SET Nombre = %s, Apellido_Paterno = %s, Apellido_Materno = %s, Sexo = %s,
        Fecha_Nacimiento = %s, Direccion = %s, Telefono = %s, Especialidad = %s, Cedula_Prof = %s,
        Correo = %s, Contrasena = %s, Fecha_Registro = %s, Estado = %s, Tipo_Usuario = %s,
        User_Key = %s WHERE Id_Usuario = %s
    """, (
        usuario.nombre,
        usuario.apellido_paterno,
        usuario.apellido_materno,
        usuario.sexo,
        usuario.fecha_nacimiento,
        usuario.direccion,
        usuario.telefono,
        usuario.especialidad,
        usuario.cedula_prof,
        usuario.correo,
        contrasena_hash,
        usuario.fecha_registro,
        usuario.estado,
        usuario.tipo_usuario,
        usuario.user_key,
        id_usuario
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Usuario actualizado exitosamente"}

@app.delete("/u/delete/{id_usuario}")
def eliminar_usuario(id_usuario: int, access: str = Depends(verificar_token)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM Usuarios WHERE Id_Usuario = %s
    """, (id_usuario,))

    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Usuario eliminado exitosamente"}

# Monitoreos
@app.get("/u/m/get/{paciente_id}")
def obtener_monitoreos(
    paciente_id: int,
    access: str = Depends(verificar_token)
):
    expediente = expediente_medico.find_one(
        {"pacienteId": paciente_id}
    )
    if not expediente:
        return {"monitoreos": []}
    monitoreos = expediente.get("monitoreos", [])
    for monitoreo in monitoreos:
        if "_id" in monitoreo:
            monitoreo["_id"] = str(monitoreo["_id"])
    return {"monitoreos": monitoreos}

@app.post("/u/m/create/{paciente_id}")
def crear_monitoreo(
    paciente_id: int,
    monitoreo: Monitoreo,
    access: str = Depends(verificar_token)
):

    monitoreo_id = ObjectId()

    nuevo_monitoreo = {
        "_id": monitoreo_id,
        "fechaRegistro": datetime.now(),
        "presionArterial": monitoreo.presion_arterial,
        "nivelGlucosa": monitoreo.nivel_glucosa,
        "temperatura": monitoreo.temperatura,
        "sintomas": monitoreo.sintomas,
        "comentarios": monitoreo.comentarios
    }

    resultado = expediente_medico.update_one(
        {"pacienteId": paciente_id},
        {"$push": {"monitoreos": nuevo_monitoreo}}
    )

    if resultado.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    return {
        "mensaje": "Monitoreo creado exitosamente",
        "_id": str(monitoreo_id)
    }

@app.put("/u/m/update/{paciente_id}/{monitoreo_id}")
def actualizar_monitoreo(
    paciente_id: int,
    monitoreo_id: str,
    monitoreo: Monitoreo,
    access: str = Depends(verificar_token)
):
    resultado = expediente_medico.update_one(
        {
            "pacienteId": paciente_id,
            "monitoreos._id": ObjectId(monitoreo_id)
        },
        {
            "$set": {
                "monitoreos.$.fechaRegistro": monitoreo.fecha_registro,
                "monitoreos.$.presionArterial": monitoreo.presion_arterial,
                "monitoreos.$.nivelGlucosa": monitoreo.nivel_glucosa,
                "monitoreos.$.temperatura": monitoreo.temperatura,
                "monitoreos.$.sintomas": monitoreo.sintomas,
                "monitoreos.$.comentarios": monitoreo.comentarios
            }
        }
    )
    if resultado.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Monitoreo no encontrado"
        )
    return {
        "mensaje": "Monitoreo actualizado exitosamente"
    }

@app.delete("/u/m/delete/{paciente_id}/{monitoreo_id}")
def eliminar_monitoreo(
    paciente_id: int,
    monitoreo_id: str,
    access: str = Depends(verificar_token)
):
    resultado = expediente_medico.update_one(
        {"pacienteId": paciente_id},
        {"$pull": {"monitoreos": {"_id": ObjectId(monitoreo_id)}}}
    )
    if resultado.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Monitoreo no encontrado"
        )
    return {
        "mensaje": "Monitoreo eliminado exitosamente"
    }


# PACIENTES

# Consulta completa (todos los pacientes)
@app.get("/pacientes", dependencies=[Depends(verificar_token)])
def get_pacientes():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Pacientes
        ORDER BY Id_Paciente
    """)

    pacientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return pacientes

# Consulta Paciente por Id
@app.get("/pacientes/{id}", dependencies=[Depends(verificar_token)])
def get_paciente(id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Pacientes
        WHERE Id_Paciente = %s
    """, (id,))

    paciente = cursor.fetchone()

    cursor.close()
    conn.close()

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    return paciente

# CRUD PACIENTES
# Crear paciente
@app.post("/pacientes", dependencies=[Depends(verificar_token)])
def create_paciente(paciente: Pacientes):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Pacientes (
            Nombre,
            Apellido_Paterno,
            Apellido_Materno,
            Sexo,
            Fecha_Nacimiento,
            Direccion,
            Correo,
            Telefono,
            Estado_Salud,
            Id_Usuario_Paciente
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING Id_Paciente
    """, (
        paciente.nombre,
        paciente.apellido_paterno,
        paciente.apellido_materno,
        paciente.sexo,
        paciente.fecha_nacimiento,
        paciente.direccion,
        paciente.correo,
        paciente.telefono,
        paciente.estado_salud,
        paciente.id_usuario_paciente
    ))

    nuevo_paciente = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "mensaje": "Paciente creado correctamente",
        "id_paciente": nuevo_paciente["id_paciente"]
    }

# Actualizar paciente
@app.put("/pacientes/{id}", dependencies=[Depends(verificar_token)])
def update_paciente(id: int, paciente: Pacientes):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Pacientes
        SET
            Nombre = %s,
            Apellido_Paterno = %s,
            Apellido_Materno = %s,
            Sexo = %s,
            Fecha_Nacimiento = %s,
            Direccion = %s,
            Correo = %s,
            Telefono = %s,
            Estado_Salud = %s,
            Id_Usuario_Paciente = %s
        WHERE Id_Paciente = %s
    """, (
        paciente.nombre,
        paciente.apellido_paterno,
        paciente.apellido_materno,
        paciente.sexo,
        paciente.fecha_nacimiento,
        paciente.direccion,
        paciente.correo,
        paciente.telefono,
        paciente.estado_salud,
        paciente.id_usuario_paciente,
        id
    ))

    conn.commit()

    if cursor.rowcount == 0:

        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    cursor.close()
    conn.close()

    return {
        "mensaje": "Paciente actualizado correctamente"
    }

# Eliminar paciente
@app.delete("/pacientes/{id}", dependencies=[Depends(verificar_token)])
def delete_paciente(id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM Pacientes
        WHERE Id_Paciente = %s
    """, (id,))

    conn.commit()

    if cursor.rowcount == 0:

        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    cursor.close()
    conn.close()

    return {
        "mensaje": "Paciente eliminado correctamente"
    }
