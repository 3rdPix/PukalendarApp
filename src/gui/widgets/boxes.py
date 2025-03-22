"""@private
Widgets personalizados
-----------------------
Contenedores para diferentes propósitos específicos
"""
from qfluentwidgets import SmoothScrollArea
from qfluentwidgets import CheckBox
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QScrollArea
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
from utils.i18n import _
from qfluentwidgets import StrongBodyLabel
from qfluentwidgets import ElevatedCardWidget
from gui import PukalendarWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt
from logging import getLogger

log = getLogger("Boxes")


class HomeViewInfoBox(CardWidget, PukalendarWidget):
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
        limit_width = 200
        limit_height = 200
        for instance in cls.instances:
            size = instance.sizeHint()
            max_width = max(max_width, size.width())
            max_height = max(max_height, size.height())
        max_width = min(max_width, limit_width)
        max_height = min(max_height, limit_height)
        for instance in cls.instances:
            instance.setMinimumSize(QSize(max_width, max_height))

class AllClassesClassBox(ElevatedCardWidget, PukalendarWidget):

    def __init__(self):
        super().__init__()
        self._init_gui()

    def _init_gui(self) -> None:
        container: QVBoxLayout = QVBoxLayout(self)
        top_container: QHBoxLayout = QHBoxLayout()
        self._color_label: QLabel = QLabel()
        self._color_label.setMaximumWidth(4)
        self._alias_label: StrongBodyLabel = StrongBodyLabel()
        top_container.addWidget(self._color_label)
        top_container.addWidget(self._alias_label)
        container.addLayout(top_container)
        container.addWidget(CardSeparator())
        
        # mas info específica
        # de momento es lo que se me ocurre poner

        self._prof_name: QLabel = QLabel(
            _("MainWindow.Courses.AllCourses.CardBox.Professor"))
        self._section: QLabel = QLabel(
            _("MainWindow.Courses.AllCourses.CardBox.Section"))
        #self._current_grade: QLabel = QLabel(
        #    _("MainWindow.Courses.AllCourses.CardBox.CurrentGrade"))
        self._class_code: QLabel = QLabel(
            _("MainWindow.Courses.AllCourses.CardBox.CourseCode"))

        self._shown_info_labels: dict[str, QLabel] = {}

        self._shown_info_labels['official_professor'] = self._prof_name
        self._shown_info_labels['official_section'] = self._section
        # self._shown_info_labels['current_grade'] = self._current_grade
        self._shown_info_labels['official_code'] = self._class_code

        container.addWidget(self._prof_name)
        # container.addWidget(self._prof_mail)
        container.addWidget(self._section)
        # container.addWidget(self._current_grade)
        container.addWidget(self._class_code)

    def load_data(self, data: dict) -> None:
        self.identifier = data.get("official_nrc")
        for key, value in data.items():
            if key in self._shown_info_labels:
                self._shown_info_labels.get(key).setText(
                    self._shown_info_labels.get(key).text()
                    + ": " + value)
                
    def set_class_alias(self, alias: str) -> None:
        self._alias_label.setText(alias)
    
    def set_class_color(self, color: str) -> None:
        # Usar hex color #xxxxxx
        self._color_label.setStyleSheet(f'QLabel {{background: {color};}}')

class SingleClassCategoryBox(CardWidget, PukalendarWidget):

    def __init__(self, title: str, parent=None) -> None:
        super().__init__(parent)
        self.title: str = title
        self.set_gui()

    def set_gui(self) -> None:
        self.layout_vertical: QVBoxLayout = QVBoxLayout(self)
        self.label_title = CaptionLabel(self.title)
        self.layout_vertical.addWidget(self.label_title ,0)
        self.layout_vertical.addWidget(CardSeparator(), 0)
    
    def set_content_layout(self, layout: QLayout) -> None:
        self.layout_vertical.addLayout(layout, 1)

    def get_content_layout(self) -> QLayout:
        return self.layout_vertical.itemAt(2)
    
class BulletTaskLabel(QFrame, PukalendarWidget):
    """
    Para la vista de una clase singular
    """
    SG_bullettask_status_changed = pyqtSignal(int, bool)

    def __init__(self, description: str, done: bool, bullet_id: int) -> None:
        super().__init__()
        self.bullet_id = bullet_id
        self.horizontal_set = QHBoxLayout(self)
        self.horizontal_set.setContentsMargins(5, 1, 0, 0)
        self.check_box = QCheckBox(description)
        self.check_box.setChecked(done)
        self.check_box.checkStateChanged.connect(self.status_changed)
        self.horizontal_set.addWidget(self.check_box)

    def status_changed(self, status) -> None:
        
        if status == Qt.CheckState.Checked:
            checked = True
        elif status == Qt.CheckState.Unchecked:
            checked = False
        else:
            log.error("A checkbox has an unkwown state")
        log.debug(f"Bullet marked as {checked}")
        self.SG_bullettask_status_changed.emit(self.bullet_id, checked)

class BulletTaskLabelStripe(QFrame):
    """
    Para la vista de más de una clase
    """


class BulletTaskListBox(SmoothScrollArea, PukalendarWidget):

    SG_bullettask_status_changed = pyqtSignal(int, bool)

    def __init__(self):
        super().__init__()
        self.main_widget = QFrame()
        self.vertical_layout = QVBoxLayout(self.main_widget)
        # self.vertical_layout.setContentsMargins(3, 0, 3, 0)
        self.vertical_layout.addStretch(1)
        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)

    def add_bullet(self, description: str, done: bool, bullet_id: int) -> None:
        new_bullet = BulletTaskLabel(description, done, bullet_id)
        new_bullet.SG_bullettask_status_changed.connect(
            self.TR_bullettask_status_changed)
        self.vertical_layout.insertWidget(0, new_bullet, stretch=0)

    def TR_bullettask_status_changed(self, bid: int, ckd: bool) -> None:
        self.SG_bullettask_status_changed.emit(bid, ckd)

    def clear_all_bullets(self) -> None:
        count = self.vertical_layout.count()
        for i in reversed(range(count - 1)):
            item = self.vertical_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    self.vertical_layout.removeWidget(widget)  # Elimina la referencia en el layout
                    widget.deleteLater()  # Marca el widget para ser eliminado correctamente
