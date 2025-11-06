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
  database_connection.commit()
  entries_path = PUCalendarAppPaths.Config.DATABASE_DEFAULT_ENTRIES
  with open(entries_path, 'r', encoding="utf-8") as raw_file:
    entries_script = raw_file.read()
  database_cursor.executescript(entries_script)
  database_connection.commit()
  database_connection.close()
