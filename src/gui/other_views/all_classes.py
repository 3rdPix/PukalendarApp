from qfluentwidgets import FlowLayout
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt
from gui.widgets.boxes import AllClassesClassBox


class AllClassesView(QFrame):

    def __init__(self) -> None:
        super().__init__(flags=Qt.WindowType.FramelessWindowHint)
        self._flow_container: FlowLayout = FlowLayout(self, True)

    def add_class(self, alias: str, color: str, data: dict={}) -> None:
        new_box: AllClassesClassBox = AllClassesClassBox()
        new_box.set_class_alias(alias)
        new_box.set_class_color(color)
        new_box.load_data(data)
        self._flow_container.addWidget(new_box)