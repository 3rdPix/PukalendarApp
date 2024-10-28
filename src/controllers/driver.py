from PyQt6.QtCore import QObject
from config.static_paths import ApplicationPaths
from config.static_paths import PathKey
from entities.courses import Course
import pickle


class MainDriver(QObject):
    def __init__(self) -> None:
        self.courses: list[Course] = None
        super().__init__()
        try:
            with open(ApplicationPaths.get_path(PathKey.DATA_USR_COURSES), 'rb') as raw_file:
                self.courses: list[Course] = pickle.load(raw_file)
        except FileNotFoundError:
            with open(ApplicationPaths.get_path(PathKey.DATA_USR_COURSES), 'wb') as raw_file:
                raw_file.write(bytearray(b"\x00"))
        except pickle.UnpicklingError:
            with open(ApplicationPaths.get_path(PathKey.DATA_USR_COURSES), 'wb') as raw_file:
                raw_file.write(bytearray(b"\x00"))
        except EOFError:
            with open(ApplicationPaths.get_path(PathKey.DATA_USR_COURSES), 'wb') as raw_file:
                raw_file.write(bytearray(b"\x00"))
        finally:
            if not self.courses:
                self.courses: list[Course] = list()

    def closeEvent(self) -> None:
        with open(ApplicationPaths.get_path(PathKey.DATA_USR_COURSES), 'wb') as raw_file:
            pickle.dump(self.courses, raw_file)