-- Pukalendar Database Schema - Final SQL DDL for SQLite
-- Generado el 6 de Noviembre de 2025

-----------------------------------------------------------
-- 1. Estudiantes
-----------------------------------------------------------
-- CREATE TABLE Estudiantes (
--     estudiante_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     nombre VARCHAR(100) NOT NULL,
--     email VARCHAR(150) NOT NULL UNIQUE,
--     password_hash VARCHAR(255) NOT NULL
-- );

-----------------------------------------------------------
-- 2. Cursos_Maestros (Información genérica del curso)
-----------------------------------------------------------
CREATE TABLE Cursos_Maestros (
    curso_maestro_id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    creditos INTEGER NOT NULL
);

-----------------------------------------------------------
-- 3. Inscripciones (Instancia del Curso / Historial)
-----------------------------------------------------------
CREATE TABLE Inscripciones (
    inscripcion_id INTEGER PRIMARY KEY AUTOINCREMENT,
--    estudiante_id INTEGER NOT NULL,
    curso_maestro_id INTEGER NOT NULL,
    periodo VARCHAR(10) NOT NULL,
    nrc VARCHAR(15) NOT NULL,
    sigla VARCHAR(20),
    profesor VARCHAR(150),
    campus VARCHAR(100),
    seccion INTEGER,
    alias VARCHAR(50) NOT NULL,
    color CHAR(7) NOT NULL,
    nota_final DECIMAL(4,2),

--    FOREIGN KEY (estudiante_id) REFERENCES Estudiantes(estudiante_id),
    FOREIGN KEY (curso_maestro_id) REFERENCES Cursos_Maestros(curso_maestro_id)
--    UNIQUE (estudiante_id, nrc, periodo)
);

-----------------------------------------------------------
-- 4. Modulos_Horarios (Horarios Oficiales y Personalizados)
-----------------------------------------------------------
CREATE TABLE Modulos_Horarios (
    modulo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    inscripcion_id INTEGER NOT NULL,
    tipo_modulo TEXT NOT NULL CHECK(tipo_modulo IN ('Oficial', 'Personalizado')),
    dia_semana TEXT NOT NULL CHECK(dia_semana IN ('Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom')),
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    sala VARCHAR(50),

    FOREIGN KEY (inscripcion_id) REFERENCES Inscripciones(inscripcion_id)
);

-----------------------------------------------------------
-- 5. Calificaciones_Estructura (Árbol Recursivo de Notas)
-----------------------------------------------------------
CREATE TABLE Calificaciones_Estructura (
    estructura_id INTEGER PRIMARY KEY AUTOINCREMENT,
    inscripcion_id INTEGER NOT NULL,
    padre_id INTEGER,
    nombre VARCHAR(100) NOT NULL,
    tipo_estructura TEXT NOT NULL CHECK(tipo_estructura IN ('Hoja', 'Ponderado', 'Media_Simple', 'Complejo', 'Granulado')),
    ponderacion DECIMAL(5,2),
    es_eliminable BOOLEAN NOT NULL DEFAULT 0,
    es_extremista BOOLEAN NOT NULL DEFAULT 0,
    expresion_calculo TEXT,

    FOREIGN KEY (inscripcion_id) REFERENCES Inscripciones(inscripcion_id),
    FOREIGN KEY (padre_id) REFERENCES Calificaciones_Estructura(estructura_id)
);

-----------------------------------------------------------
-- 6. Metodo_Calculo_Nota (Transformación Puntaje a Nota)
-----------------------------------------------------------
CREATE TABLE Metodo_Calculo_Nota (
    metodo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    estructura_id INTEGER NOT NULL UNIQUE,
    tipo_metodo TEXT NOT NULL CHECK(tipo_metodo IN ('Exigencia_Lineal', 'Puntaje_Directo', 'Formula_Granulada')),
    exigencia_porcentaje DECIMAL(5,2),
    puntaje_maximo_esperado DECIMAL(10,2),
    puntaje_total_posible DECIMAL(10,2),

    FOREIGN KEY (estructura_id) REFERENCES Calificaciones_Estructura(estructura_id)
);

-----------------------------------------------------------
-- 7. Actividades (Tareas, Evaluaciones, Eventos)
-----------------------------------------------------------
CREATE TABLE Actividades (
    actividad_id INTEGER PRIMARY KEY AUTOINCREMENT,
    inscripcion_id INTEGER NOT NULL,
    estructura_id_asociada INTEGER,
    tipo TEXT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    tiene_calificacion BOOLEAN NOT NULL,
    es_horario_fijo BOOLEAN NOT NULL,
    fecha_arbitraria DATETIME,
    duracion_minutos INTEGER,

    FOREIGN KEY (inscripcion_id) REFERENCES Inscripciones(inscripcion_id),
    FOREIGN KEY (estructura_id_asociada) REFERENCES Calificaciones_Estructura(estructura_id)
);

-----------------------------------------------------------
-- 8. Actividades_Modulos (Instancias de Horario/Clase)
-----------------------------------------------------------
CREATE TABLE Actividades_Modulos (
    actividad_modulo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    actividad_id INTEGER NOT NULL,
    modulo_id INTEGER,
    fecha_instancia DATE NOT NULL,
    estado TEXT CHECK(estado IN ('Pendiente', 'Cancelado', 'Asistido')),

    FOREIGN KEY (actividad_id) REFERENCES Actividades(actividad_id),
    FOREIGN KEY (modulo_id) REFERENCES Modulos_Horarios(modulo_id),
    UNIQUE (actividad_id, fecha_instancia)
);

-----------------------------------------------------------
-- 9. Calificaciones_Valores (Notas Reales y Sobrescritura)
-----------------------------------------------------------
CREATE TABLE Calificaciones_Valores (
    valor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    estructura_id INTEGER,
    actividad_id INTEGER NOT NULL,
    puntaje_obtenido DECIMAL(10,2),
    nota_calculada DECIMAL(4,2),
    nota_manual_usuario DECIMAL(4,2),
    usar_nota_manual BOOLEAN NOT NULL DEFAULT 0,
    puntos_extra DECIMAL(4,2) NOT NULL DEFAULT 0.0,
    puntaje_maximo DECIMAL(10,2),

    FOREIGN KEY (estructura_id) REFERENCES Calificaciones_Estructura(estructura_id),
    FOREIGN KEY (actividad_id) REFERENCES Actividades(actividad_id)
);

-----------------------------------------------------------
-- 10. Sesiones_Estudio (Registro de Tiempo)
-----------------------------------------------------------
CREATE TABLE Sesiones_Estudio (
    sesion_id INTEGER PRIMARY KEY AUTOINCREMENT,
    inscripcion_id INTEGER NOT NULL,
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NOT NULL,
    objetivo VARCHAR(255),
    es_manual BOOLEAN NOT NULL DEFAULT 0,

    FOREIGN KEY (inscripcion_id) REFERENCES Inscripciones(inscripcion_id)
);

-----------------------------------------------------------
-- 11. Tareas_Pendientes (To-Do List, con subtareas y estados)
-----------------------------------------------------------
CREATE TABLE Tareas_Pendientes (
    tarea_id INTEGER PRIMARY KEY AUTOINCREMENT,
    padre_tarea_id INTEGER,
    inscripcion_id INTEGER,
    actividad_id INTEGER,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_limite DATETIME,
    porcentaje_completado INTEGER NOT NULL DEFAULT 0,
    estado TEXT NOT NULL DEFAULT 'Pendiente'
           CHECK(estado IN ('Pendiente', 'Completada', 'Retrasada', 'Prioritaria')),
    es_recurrente BOOLEAN NOT NULL DEFAULT 0,
    fecha_fin_recurrencia DATE,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (padre_tarea_id) REFERENCES Tareas_Pendientes(tarea_id),
    FOREIGN KEY (inscripcion_id) REFERENCES Inscripciones(inscripcion_id),
    FOREIGN KEY (actividad_id) REFERENCES Actividades(actividad_id)
);

-----------------------------------------------------------
-- CONSULTAS BASE (SETUP INICIAL)
-----------------------------------------------------------

-- Insertar el curso fantasma "Actividades Personales y Eventos"
INSERT INTO Cursos_Maestros (codigo, nombre, creditos)
VALUES ('GENERAL', 'Actividades Personales y Eventos', 0);