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
from common import PukalendarWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt
from logging import getLogger
from qfluentwidgets import PopUpAniStackedWidget
from PyQt6.QtWidgets import QGridLayout
from common.entities import CursoAplicacion
from PyQt6.QtGui import QBrush
from PyQt6.QtGui import QColor

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

    def __init__(self, data: CursoAplicacion) -> None:
        super().__init__()
        self.identifier = data.identificador
        self._init_gui(data)

    def _init_gui(self, data: CursoAplicacion) -> None:
        container = QVBoxLayout(self)
        top_container = QHBoxLayout()
        self._color_label = QLabel(parent=self)
        self._color_label.setMaximumWidth(4)
        self._color_label.setStyleSheet(f"QLabel{{background:{data.color}}}")
        self._alias_label = StrongBodyLabel(text=data.alias)
        top_container.addWidget(self._color_label)
        top_container.addWidget(self._alias_label,
                                alignment=Qt.AlignmentFlag.AlignLeft)
        container.addLayout(top_container)
        container.addWidget(CardSeparator())
        
        # mas info específica
        # de momento es lo que se me ocurre poner
        info_grid = QGridLayout()
        professor_indicator = QLabel(
            _("MainWindow.Courses.AllCourses.CardBox.Professor"))
        section_indicator = QLabel(
            _("MainWindow.Courses.AllCourses.CardBox.Section"))
        code_indicator = QLabel(
            _("MainWindow.Courses.AllCourses.CardBox.CourseCode"))
        self._prof_name = QLabel(text=data.profesor)
        self._section = QLabel(text=str(data.seccion))
        self._class_code = QLabel(text=data.sigla)

        info_grid.addWidget(professor_indicator, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        info_grid.addWidget(self._prof_name, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)
        info_grid.addWidget(section_indicator, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        info_grid.addWidget(self._section, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)
        info_grid.addWidget(code_indicator, 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        info_grid.addWidget(self._class_code, 2, 1, alignment=Qt.AlignmentFlag.AlignRight)
        container.addLayout(info_grid)


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


class SlideNavigator(QWidget, PukalendarWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(QHBoxLayout(self))
        self.content_container = PopUpAniStackedWidget(self)
        self.layout().addWidget(self.content_container)
        self.navigation_bar = QFrame(self, Qt.WindowType.Tool)
        self.layout().addWidget(self.navigation_bar)

        # Setup navigation bar
        self.navigation_bar.setLayout(QVBoxLayout(self.navigation_bar))
        self.navigation_bar.first_layout = QVBoxLayout(self.navigation_bar)
        self.navigation_bar.second_layout = QScrollArea(self.navigation_bar)
