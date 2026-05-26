from pydantic import BaseModel
from datetime import datetime, date


class Login(BaseModel):
    email: str
    password: str


class Usuarios(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    sexo: str
    fecha_nacimiento: date
    direccion: str
    telefono: str
    especialidad: str
    cedula_prof: str
    correo: str
    contrasena: str
    fecha_registro: datetime
    estado: bool
    tipo_usuario: str
    user_key: str


class Pacientes(BaseModel):
    id_paciente: int | None = None
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    sexo: str
    fecha_nacimiento: date
    direccion: str
    correo: str
    telefono: str
    estado_salud: str
    id_usuario_paciente: int


class Expediente_Medico(BaseModel):
    pacienteId: int
    antecedentes: str
    tratamientos: str
    notas_medicas: str
    planes_personalizados: list["PlanPersonalizado"]
    consultas: list["Consulta"]
    eventos: list["Evento"]
    monitoreos: list["Monitoreo"]
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    estado: str


class Monitoreo(BaseModel):
    fecha_registro: datetime
    presion_arterial: str
    nivel_glucosa: str
    temperatura: str
    sintomas: str
    comentarios: str


class PlanPersonalizado(BaseModel):
    descripcion: str
    objetivo: str
    tipo_plan: str
    duracion: str
    frecuencia: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str
    observaciones: str
    recomendaciones: str
    contraindicaciones: str
    metodos_anticonceptivos: list["MetodoAnticonceptivo"]


class MetodoAnticonceptivo(BaseModel):
    metodo_id: int


class Consulta(BaseModel):
    fecha: datetime
    hora: str
    motivo: str
    diagnostico: str
    observaciones: str


class Evento(BaseModel):
    tipo_evento: str
    fecha: datetime
    hora: str
    descripcion: str
    estado: int


class Metodos_Anticonceptivos(BaseModel):
    id_metodo: int
    tipo: str
    nombre: str
    descripcion: str
    efectividad: float
    uso_recomendado: str
    frecuencia: str
    contraindicaciones: str
    efectos_secundarios: str
    requiere_receta: bool
    es_reversible: bool
    disponible: bool