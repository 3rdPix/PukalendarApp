from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QWidget

class CoursesView(QFrame):
    
    def __init__(self, parent: QWidget | None=None) -> None:
        super().__init__(parent)
        self.setObjectName('courses_view')