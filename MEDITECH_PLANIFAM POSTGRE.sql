CREATE TABLE Usuarios
(
    Id_Usuario SERIAL PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Apellido_Paterno VARCHAR(50),
    Apellido_Materno VARCHAR(50),
    Sexo CHAR(1) NOT NULL CHECK (Sexo IN ('M','F','P')),
    Fecha_Nacimiento DATE NOT NULL,
    Direccion VARCHAR(150) NOT NULL,
    Telefono VARCHAR(15) NOT NULL,
    Especialidad VARCHAR(100),
    Cedula_Prof VARCHAR(20) UNIQUE,
    Correo VARCHAR(100) NOT NULL UNIQUE,
    Contrasena VARCHAR(250) NOT NULL,
    Fecha_Registro DATE NOT NULL DEFAULT CURRENT_DATE,
    Estado BOOLEAN NOT NULL DEFAULT FALSE,
    Tipo_Usuario CHAR(1) NOT NULL CHECK (Tipo_Usuario IN ('P','M','A')),
    User_Key VARCHAR(100)
);

-- =========================================
-- TABLA: PACIENTES
-- =========================================
CREATE TABLE Pacientes
(
    Id_Paciente SERIAL PRIMARY KEY,
    Nombre VARCHAR(75) NOT NULL,
    Apellido_Paterno VARCHAR(50),
    Apellido_Materno VARCHAR(50),
    Sexo CHAR(1) NOT NULL CHECK (Sexo IN ('M','F','P')),
    Fecha_Nacimiento DATE NOT NULL,
    Direccion VARCHAR(150) NOT NULL,
    Correo VARCHAR(100) NOT NULL UNIQUE,
    Telefono VARCHAR(15) NOT NULL,
    Estado_Salud TEXT NOT NULL,
    Id_Usuario_Paciente INT,

    CONSTRAINT FK_Id_Usuario_Paciente
        FOREIGN KEY (Id_Usuario_Paciente)
        REFERENCES Usuarios(Id_Usuario)
);

-- =========================================
-- TABLA: CONSULTAS
-- =========================================
CREATE TABLE Consultas
(
    Id_Consulta SERIAL PRIMARY KEY,
    Fecha DATE NOT NULL,
    Hora TIME NOT NULL,
    Motivo TEXT NOT NULL,
    Diagnostico TEXT,
    Observaciones TEXT,
    Id_Paciente_Consulta INT,
    Id_Usuario_Consulta INT,

    CONSTRAINT FK_Id_Paciente_Consulta
        FOREIGN KEY (Id_Paciente_Consulta)
        REFERENCES Pacientes(Id_Paciente),

    CONSTRAINT FK_Id_Usuario_Consulta
        FOREIGN KEY (Id_Usuario_Consulta)
        REFERENCES Usuarios(Id_Usuario)
);

-- =========================================
-- TABLA: EVENTOS_CALENDARIO
-- =========================================
CREATE TABLE Eventos_Calendario
(
    Id_Evento_Calendario SERIAL PRIMARY KEY,
    Tipo_Evento VARCHAR(50) NOT NULL,
    Fecha_Evento DATE NOT NULL,
    Hora_Evento TIME NOT NULL,
    Descripcion TEXT,
    Estado BOOLEAN NOT NULL DEFAULT FALSE,
    Id_Paciente_Eventos INT,

    CONSTRAINT FK_Id_Paciente_Eventos
        FOREIGN KEY (Id_Paciente_Eventos)
        REFERENCES Pacientes(Id_Paciente)
);

-- =========================================
-- TABLA: METODOS ANTICONCEPTIVOS
-- =========================================
CREATE TABLE Metodos_Anticonceptivos
(
    Id_Metodo SERIAL PRIMARY KEY,
    Tipo VARCHAR(50) NOT NULL,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    Efectividad DECIMAL(5,2) NOT NULL,
    Uso_Recomendado VARCHAR(150) NOT NULL,
    Frecuencia VARCHAR(50) NOT NULL,
    Contraindicaciones TEXT,
    Efectos_Secundarios TEXT,
    Requiere_Receta BOOLEAN NOT NULL DEFAULT FALSE,
    Es_Reversible BOOLEAN NOT NULL DEFAULT FALSE,
    Disponible BOOLEAN NOT NULL DEFAULT FALSE
);

-- =========================================
-- TABLA: BITACORA
-- =========================================
CREATE TABLE Bitacora
(
    Id_Bitacora SERIAL PRIMARY KEY,
    Id_Usuario INT NOT NULL,
    Accion VARCHAR(50) NOT NULL,
    Tabla_Afectada VARCHAR(50) NOT NULL,
    Id_Registro INT,
    Descripcion TEXT,
    Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT FK_Bitacora_Usuario
        FOREIGN KEY (Id_Usuario)
        REFERENCES Usuarios(Id_Usuario)
);


-- =========================================
-- USUARIOS
-- =========================================
INSERT INTO Usuarios
(Nombre, Apellido_Paterno, Apellido_Materno, Sexo, Fecha_Nacimiento, Direccion, Telefono, Especialidad, Cedula_Prof, Correo, Contrasena, Estado, Tipo_Usuario, User_Key)
VALUES
('Victoria','Torres','Hernandez','F','2004-04-19','Calle Hidalgo 45','8719876543','Administracion',NULL,'vicky19.th@meditech.com','123456',TRUE,'A','KEY002'),

('Jared','Salazar','Romero','M','2001-06-26','Colonia Centro','8715557788',NULL,NULL,'jared26.sr@gmail.com','123456',TRUE,'P','KEY003');

-- =========================================
-- PACIENTES
-- =========================================
INSERT INTO Pacientes
(Nombre, Apellido_Paterno, Apellido_Materno, Sexo, Fecha_Nacimiento, Direccion, Correo, Telefono, Estado_Salud, Id_Usuario_Paciente)
VALUES
('Sarai','Hurtado','Flores','F','2000-11-27','Colonia Roma','sara.hf@gmail.com','8712223344','Salud estable',1),

('Isaac','Castro','Gomez','M','2002-12-07','Colonia Moderna','isaac.@gmail.com','8713334455','Hipertension controlada',2);

-- =========================================
-- CONSULTAS
-- =========================================
INSERT INTO Consultas
(Fecha, Hora, Motivo, Diagnostico, Observaciones, Id_Paciente_Consulta, Id_Usuario_Consulta)
VALUES
('2026-03-10','10:30:00','Consulta general','Paciente estable','Continuar tratamiento',1,1),

('2026-03-12','11:00:00','Dolor abdominal','Gastritis leve','Dieta blanda',2,1);

-- =========================================
-- EVENTOS_CALENDARIO
-- =========================================
INSERT INTO Eventos_Calendario
(Tipo_Evento, Fecha_Evento, Hora_Evento, Descripcion, Estado, Id_Paciente_Eventos)
VALUES
('Cita Medica','2026-03-20','09:00:00','Consulta de seguimiento',FALSE,1),

('Recordatorio Medicamento','2026-03-18','08:00:00','Tomar medicamento para la presion',TRUE,2),

('Consulta General','2026-03-22','10:30:00','Revision general del paciente',FALSE,1),

('Control Medico','2026-03-25','11:00:00','Control de hipertension',FALSE,2),

('Cita Ginecologica','2026-03-28','12:15:00','Consulta preventiva',TRUE,1);

-- =========================================
-- METODOS ANTICONCEPTIVOS
-- =========================================
INSERT INTO Metodos_Anticonceptivos
(Tipo, Nombre, Descripcion, Efectividad, Uso_Recomendado, Frecuencia, Contraindicaciones, Efectos_Secundarios, Requiere_Receta, Es_Reversible, Disponible)
VALUES
('Hormonal','Pastillas Anticonceptivas','Metodo hormonal que evita la ovulacion',99.00,'Mujeres en edad reproductiva','Diario','Problemas de coagulación','Nauseas, dolor de cabeza',TRUE,TRUE,TRUE),

('Barrera','Condon Masculino','Metodo de barrera que evita el paso de espermatozoides',98.00,'Relaciones sexuales','Cada relacion','Alergia al latex','Irritacion',FALSE,TRUE,TRUE),

('Hormonal','Inyeccion Anticonceptiva','Metodo hormonal aplicado mediante inyeccion',94.00,'Mujeres que buscan metodo mensual','Mensual','Problemas hormonales','Cambios en el ciclo menstrual',TRUE,TRUE,TRUE),

('Dispositivo','DIU','Dispositivo intrauterino colocado en el utero',99.80,'Metodo de larga duracion','5 a 10 años','Infecciones uterinas','Dolor abdominal',TRUE,TRUE,TRUE),

('Natural','Metodo del Ritmo','Control del ciclo menstrual para evitar dias fertiles',76.00,'Parejas con ciclos regulares','Mensual','Ciclos irregulares','Riesgo de embarazo',FALSE,TRUE,TRUE);