"""
Widgets personalizados
-----------------------
Contenedores para diferentes propósitos específicos
"""
from qfluentwidgets import CardWidget
from qfluentwidgets import CaptionLabel
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QHBoxLayout
from qfluentwidgets.components.widgets.card_widget import CardSeparator
from qfluentwidgets import SubtitleLabel
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLayout
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QStyle
from config.text_keys import TextKey
from utils.i18n import _
from qfluentwidgets import StrongBodyLabel
from qfluentwidgets import ElevatedCardWidget


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

class AllClassesClassBox(ElevatedCardWidget):

    def __init__(self):
        super().__init__()
        self._init_gui()

    def _init_gui(self) -> None:
        container: QVBoxLayout = QVBoxLayout(self)
        top_container: QHBoxLayout = QHBoxLayout()
        self._color_label: QLabel = QLabel()
        self._color_label.setMaximumSize(30, 30)
        self._alias_label: StrongBodyLabel = StrongBodyLabel()
        top_container.addWidget(self._color_label)
        top_container.addWidget(self._alias_label)
        container.addLayout(top_container)
        container.addWidget(CardSeparator())
        
        # mas info específica
        # de momento es lo que se me ocurre poner

        self._prof_name: QLabel = QLabel(_(TextKey.PROFESSOR_LABEL))
        self._prof_mail: QLabel = QLabel(_(TextKey.PROFESSOR_MAIL_LABEL))
        self._section: QLabel = QLabel(_(TextKey.SECTION_LABEL))
        self._current_grade: QLabel = QLabel(_(TextKey.CURRENT_GRADE_LABEL))
        self._class_code: QLabel = QLabel(_(TextKey.CLASS_CODE_LABEL))

        self._shown_info_labels: dict[str, QLabel] = {}

        self._shown_info_labels['professor'] = self._prof_name
        self._shown_info_labels['professor_mail'] = self._prof_mail
        self._shown_info_labels['section'] = self._section
        self._shown_info_labels['current_grade'] = self._current_grade
        self._shown_info_labels['class_code'] = self._class_code

        container.addWidget(self._prof_name)
        container.addWidget(self._prof_mail)
        container.addWidget(self._section)
        container.addWidget(self._current_grade)
        container.addWidget(self._class_code)

    def load_data(self, data: dict) -> None:
        for key, value in data:
            if key in self._shown_info_labels:
                self._shown_info_labels.get(key).setText(
                    self._shown_info_labels.get(key).text() + value)
                
    def set_class_alias(self, alias: str) -> None:
        self._alias_label.setText(alias)
    
    def set_class_color(self, color: str) -> None:
        # Usar hex color #xxxxxx
        self._color_label.setStyleSheet(f'QLabel {{background: {color};}}')