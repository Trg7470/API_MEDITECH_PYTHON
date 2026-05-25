from pydantic import BaseModel
from datetime import datetime, date

class Login(BaseModel):
    email: str
    password: str

class Usuarios(BaseModel):
    Id_Usuario: int
    Nombre: str
    Apellido_Paterno: str
    Apellido_Materno: str
    Sexo: str
    Fecha_Nacimiento: datetime
    Direccion: str
    Telefono: str
    Especialidad: str
    Cedula_Prof: str
    Correo: str
    Contrasena: str
    Fecha_Registro: datetime
    Estado: bool
    Tipo_Usuario: str
    User_Key: str
    Ultimo_Acceso: datetime

class Pacientes(BaseModel):
    Id_Paciente: int
    Nombre: str
    Apellido_Paterno: str
    Apellido_Materno: str
    Sexo: str
    Fecha_Nacimiento: datetime
    Direccion: str
    Correo: str
    Telefono: str
    Estado_Salud: str
    Id_Usuario_Paciente: int

class Expediente_Medico(BaseModel):
    _id: str | None
    pacienteId: int
    antecedentes: str
    tratamientos: str
    notasMedicas: str
    planesPersonalizados: list["PlanPersonalizado"]
    consultas: list["Consulta"]
    eventos: list["Evento"]
    monitoreos: list["Monitoreo"]
    fechaCreacion: datetime
    fechaActualizacion: datetime
    estado: str


class Monitoreo(BaseModel):
    _id: str
    fechaRegistro: datetime
    presionArterial: str
    nivelGlucosa: str
    temperatura: str
    sintomas: str
    comentarios: str


class PlanPersonalizado(BaseModel):
    _id: str
    descripcion: str
    objetivo: str
    tipoPlan: str
    duracion: str
    frecuencia: str
    fechaInicio: datetime
    fechaFin: datetime
    estado: str
    observaciones: str
    recomendaciones: str
    contraindicaciones: str
    metodosAnticonceptivos: list["MetodoAnticonceptivo"]


class MetodoAnticonceptivo(BaseModel):
    _id: str | None
    metodoId: int


class Consulta(BaseModel):
    id_Consulta: str
    fecha: datetime
    hora: str
    motivo: str
    diagnostico: str
    observaciones: str


class Evento(BaseModel):
    _id: str
    tipoEvento: str
    fecha: datetime
    hora: str
    descripcion: str
    estado: int

class Metodos_Anticonceptivos(BaseModel):
    IdMetodo: int
    Tipo: str
    Nombre: str
    Descripcion: str
    Efectividad: float
    Uso_Recomendado: str
    Frecuencia: str
    Contraindicaciones: str
    Efectos_Secundarios: str
    Requiere_Receta: bool
    Es_Reversible: bool
    Disponible: bool