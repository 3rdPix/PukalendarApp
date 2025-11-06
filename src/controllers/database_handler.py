from typing import Iterable
from config import PUCalendarAppPaths
from os.path import exists
import sqlite3

if not exists(PUCalendarAppPaths.Config.DATABASE):
  database_connection = sqlite3.connect(PUCalendarAppPaths.Config.DATABASE)
  database_cursor = database_connection.cursor()
  schema_path = PUCalendarAppPaths.Config.DATABASE_SCHEMA
  with open(schema_path, 'r', encoding='utf-8') as raw_file:
    creation_script = raw_file.read()
  database_cursor.executescript(creation_script)
  # database_connection.commit()
  entries_path = PUCalendarAppPaths.Config.DATABASE_DEFAULT_ENTRIES
  with open(entries_path, 'r', encoding="utf-8") as raw_file:
    entries_script = raw_file.read()
  database_cursor.executescript(entries_script)
  database_connection.commit()
  database_connection.close()

class CourseAlreadyExists(Exception):
  def __init__(self, *args: object) -> None:
    self.alias, self.color = args
    super().__init__()


class DatabaseManager:
  def __init__(self) -> None:
    self.database_connection = sqlite3.connect(
      PUCalendarAppPaths.Config.DATABASE)
    self.database_cursor = self.database_connection.cursor()

  def create_course(self, sigla: str, nombre: str, creditos: int, periodo: str,
                    nrc: int, seccion: int, alias: str, color: str,
                    profesor: str|None=None, campus: str|None=None,
                    ) -> int:
    with self.database_connection:
      self.database_cursor.execute(
        """
        INSERT OR IGNORE INTO Cursos_Maestros (sigla, nombre, creditos)
        VALUES (?, ?, ?);
        """,
        (sigla, nombre, creditos))
      self.database_cursor.execute(
        """
        SELECT curso_maestro_id FROM Cursos_Maestros WHERE sigla = ?;
        """,
        (sigla,))
      master_id: int = self.database_cursor.fetchone()[0]

      self.database_cursor.execute(
        """
        SELECT alias, color FROM Inscripciones
        WHERE nrc = ? AND periodo = ?;
        """,
        (nrc, periodo))
      existing = self.database_cursor.fetchone()
      if existing is not None:
          raise CourseAlreadyExists(*existing)
      self.database_cursor.execute(
        """
        INSERT INTO Inscripciones (
        curso_maestro_id, periodo, nrc, profesor, campus, seccion,
        alias, color)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (master_id, periodo, nrc, profesor, campus, seccion, alias, color))
      return self.database_cursor.lastrowid or -1




algo = DatabaseManager()
try:
  print(algo.create_course("TEST8", "nombre", 1, "periods", 1, 1, "alias", "color"))
except CourseAlreadyExists as existente:
  print(existente.alias, existente.color)