-----------------------------------------------------------
-- CONSULTAS BASE (SETUP INICIAL)
-----------------------------------------------------------

-- Insertar el curso fantasma "Actividades Personales y Eventos"
INSERT INTO Cursos_Maestros (sigla, nombre, creditos)
VALUES ('GENERAL', 'Actividades Personales y Eventos', 0);

-- Insertar módulos horarios oficiales

-- Lunes
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Lun', 1, '08:20', '09:30', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Lun', 2, '09:40', '10:50', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Lun', 3,  '11:00', '12:10', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Lun', 4, '12:20', '13:30', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Lun', 5, '14:50', '16:00', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Lun', 6, '16:10', '17:20', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Lun', 7, '17:30', '18:40', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Lun', 8, '18:50', '20:00', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Lun', 9, '20:10', '21:20', 1);

-- Martes
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mar', 1, '08:20', '09:30', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mar', 2, '09:40', '10:50', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mar', 3, '11:00', '12:10', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mar', 4, '12:20', '13:30', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mar', 5, '14:50', '16:00', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mar', 6, '16:10', '17:20', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mar', 7, '17:30', '18:40', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mar', 8, '18:50', '20:00', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mar', 9, '20:10', '21:20', 1);

-- Miércoles
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mie', 1, '08:20', '09:30', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mie', 2, '09:40', '10:50', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mie', 3, '11:00', '12:10', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mie', 4, '12:20', '13:30', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mie', 5, '14:50', '16:00', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mie', 6, '16:10', '17:20', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mie', 7, '17:30', '18:40', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mie', 8, '18:50', '20:00', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Mie', 9, '20:10', '21:20', 1);

-- Jueves
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Jue', 1, '08:20', '09:30', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Jue', 2, '09:40', '10:50', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Jue', 3, '11:00', '12:10', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Jue', 4, '12:20', '13:30', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Jue', 5, '14:50', '16:00', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Jue', 6, '16:10', '17:20', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Jue', 7, '17:30', '18:40', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Jue', 8, '18:50', '20:00', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Jue', 9, '20:10', '21:20', 1);

-- Viernes
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Vie', 1, '08:20', '09:30', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Vie', 2, '09:40', '10:50', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Vie', 3, '11:00', '12:10', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Vie', 4, '12:20', '13:30', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Vie', 5, '14:50', '16:00', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Vie', 6, '16:10', '17:20', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Vie', 7, '17:30', '18:40', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Vie', 8, '18:50', '20:00', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Vie', 9, '20:10', '21:20', 1);

-- Sábado
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Sab', 1, '08:20', '09:30', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Sab', 2, '09:40', '10:50', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Sab', 3, '11:00', '12:10', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Sab', 4, '12:20', '13:30', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Sab', 5, '14:50', '16:00', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Sab', 6, '16:10', '17:20', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Sab', 7, '17:30', '18:40', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Sab', 8, '18:50', '20:00', 1);
INSERT INTO Modulos_Oficiales (dia_semana, numero_modulo, hora_inicio, hora_fin, valido)
VALUES ('Sab', 9, '20:10', '21:20', 1);