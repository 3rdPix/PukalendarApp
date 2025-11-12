from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QWidget
from common import PukalendarWidget

class AgendaView(QFrame, PukalendarWidget):
    
    def __init__(self, parent: QWidget | None=None) -> None:
        super().__init__(parent)
        self.setObjectName('agenda_view')