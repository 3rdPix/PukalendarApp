from PyQt6.QtCore import QObject
from config import PUCalendarAppPaths as pt
from entities.courses import Course
import pickle


class MainDriver(QObject):
    def __init__(self) -> None:
        self.courses: list[Course] = None
        super().__init__()
        try:
            with open(pt.Config.USER_COURSES, 'rb') as raw_file:
                self.courses: list[Course] = pickle.load(raw_file)
        except FileNotFoundError:
            with open(pt.Config.USER_COURSES, 'wb') as raw_file:
                raw_file.write(bytearray(b"\x00"))
        except pickle.UnpicklingError:
            with open(pt.Config.USER_COURSES, 'wb') as raw_file:
                raw_file.write(bytearray(b"\x00"))
        except EOFError:
            with open(pt.Config.USER_COURSES, 'wb') as raw_file:
                raw_file.write(bytearray(b"\x00"))
        finally:
            if not self.courses:
                self.courses: list[Course] = list()

    def closeEvent(self) -> None:
        with open(pt.Config.USER_COURSES, 'wb') as raw_file:
            pickle.dump(self.courses, raw_file)