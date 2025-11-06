-----------------------------------------------------------
-- CONSULTAS BASE (SETUP INICIAL)
-----------------------------------------------------------

-- Insertar el curso fantasma "Actividades Personales y Eventos"
INSERT INTO Cursos_Maestros (codigo, nombre, creditos)
VALUES ('GENERAL', 'Actividades Personales y Eventos', 0);

-- Insertar módulos horarios oficiales

-- Lunes
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Lun', '08:20', '09:30');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Lun', '09:40', '10:50');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Lun', '11:00', '12:10');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Lun', '12:20', '13:30');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Lun', '14:50', '16:00');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Lun', '16:10', '17:20');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Lun', '17:30', '18:40');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Lun', '18:50', '20:00');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Lun', '20:10', '21:20');

-- Martes
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mar', '08:20', '09:30');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mar', '09:40', '10:50');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mar', '11:00', '12:10');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mar', '12:20', '13:30');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mar', '14:50', '16:00');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mar', '16:10', '17:20');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mar', '17:30', '18:40');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mar', '18:50', '20:00');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mar', '20:10', '21:20');

-- Miércoles
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mie', '08:20', '09:30');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mie', '09:40', '10:50');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mie', '11:00', '12:10');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mie', '12:20', '13:30');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mie', '14:50', '16:00');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mie', '16:10', '17:20');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mie', '17:30', '18:40');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mie', '18:50', '20:00');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Mie', '20:10', '21:20');

-- Jueves
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Jue', '08:20', '09:30');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Jue', '09:40', '10:50');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Jue', '11:00', '12:10');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Jue', '12:20', '13:30');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Jue', '14:50', '16:00');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Jue', '16:10', '17:20');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Jue', '17:30', '18:40');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Jue', '18:50', '20:00');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Jue', '20:10', '21:20');

-- Viernes
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Vie', '08:20', '09:30');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Vie', '09:40', '10:50');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Vie', '11:00', '12:10');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Vie', '12:20', '13:30');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Vie', '14:50', '16:00');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Vie', '16:10', '17:20');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Vie', '17:30', '18:40');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Vie', '18:50', '20:00');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Vie', '20:10', '21:20');

-- Sábado
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Sab', '08:20', '09:30');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Sab', '09:40', '10:50');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Sab', '11:00', '12:10');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Sab', '12:20', '13:30');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Sab', '14:50', '16:00');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Sab', '16:10', '17:20');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Sab', '17:30', '18:40');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Sab', '18:50', '20:00');
INSERT INTO Modulos_Oficiales (dia_semana, hora_inicio, hora_fin)
VALUES ('Sab', '20:10', '21:20');