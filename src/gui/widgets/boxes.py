"""
Widgets personalizados
-----------------------
Contenedores para diferentes propósitos específicos
"""
from qfluentwidgets import CardWidget
from qfluentwidgets.components.widgets.card_widget import CardSeparator
from qfluentwidgets import SubtitleLabel
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLayout
from PyQt6.QtCore import QSize


class HomeViewInfoBox(CardWidget):
    """
    A card widget with a title, made to display the
    summarized info in the home interface.
    By default, all instances of HomeViewInfoBox are synced to be
    of equal size, determined by the minimum max size required
    to display all content of the "biggest" box.
    You can change this for each instance by specifying the argument
    trackSize=False
    """

    def __init__(self, parent=None, trackSize: bool=True) -> None:
        super().__init__(parent)
        self._init_gui()
        self._tracking: bool = trackSize
        if self._tracking: _HomeViewInfoBoxManager.add_instance(self)

    def _init_gui(self) -> None:
        """
        Displays elements
        """
        self._card_layout: QVBoxLayout = QVBoxLayout(self)
        self._title_label: SubtitleLabel = SubtitleLabel(self)
        self._card_layout.addWidget(self._title_label)
        self._card_layout.addWidget(CardSeparator())

    def setTitle(self, card_title: str) -> None:
        self._title_label.setText(card_title)
        if self._tracking: _HomeViewInfoBoxManager.update_all_sizes()

    def insert_widget(self, widget: QWidget) -> None:
        self._card_layout.addWidget(widget)
        if self._tracking: _HomeViewInfoBoxManager.update_all_sizes()

    def insert_layout(self, layout: QLayout) -> None:
        self._card_layout.addLayout(layout)
        if self._tracking: _HomeViewInfoBoxManager.update_all_sizes()
        
class _HomeViewInfoBoxManager:
    """
    Keeps track of instances of HomeViewInfoBoxes to update
    the size, making them appear at the same size
    """
    instances = []

    @classmethod
    def add_instance(cls, instance):
        cls.instances.append(instance)
        cls.update_all_sizes()

    @classmethod
    def update_all_sizes(cls):
        max_width = 0
        max_height = 0

        for instance in cls.instances:
            size = instance.sizeHint()
            max_width = max(max_width, size.width())
            max_height = max(max_height, size.height())

        for instance in cls.instances:
            instance.setMinimumSize(QSize(max_width, max_height))