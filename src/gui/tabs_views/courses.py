from datetime import timedelta
from qfluentwidgets import PushButton
from PyQt6.QtCore import pyqtSignal
from config import PUCalendarAppPaths as pt
from gui.widgets.boxes import SingleClassCategoryBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QGridLayout
from qfluentwidgets import FlowLayout
from gui.widgets.boxes import AllClassesClassBox
from qfluentwidgets import SubtitleLabel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import Action
from qfluentwidgets import CommandBar
from qfluentwidgets import FluentIcon as FIF
from utils.i18n import _
from qfluentwidgets.components.widgets.card_widget import CardSeparator
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from qfluentwidgets import PrimaryToolButton
from gui.widgets.dialogs import NewClassDialog
from gui.widgets.misc import OpacityAniStackedWidget
from entities.courses import NRC
from qfluentwidgets import MessageDialog
from gui import PukalendarWidget
import logging


log = logging.getLogger("CoursesTab")


class CoursesView(QFrame, PukalendarWidget):
    SG_CoursesView_delete: pyqtSignal = pyqtSignal(NRC, name="SG_CoursesView_delete")
    new_class_dialog: NewClassDialog

    def __init__(self, parent: QWidget | None=None) -> None:
        super().__init__(parent)
        self.setObjectName('courses_view')
        self._create_layout()
        self._create_layers()
        self.new_class_dialog = NewClassDialog()

    def _create_layout(self) -> None:
        """
        Preparación de la interfaz de la pestaña
        """
        tab_layout: QVBoxLayout = QVBoxLayout(self)
        command_bar: CommandBar = CommandBar(self)
        command_bar.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        command_bar.addActions(self._create_command_bar_actions())
        tab_layout.addWidget(command_bar)
        tab_layout.addWidget(CardSeparator())
        self._stacked_area: OpacityAniStackedWidget = \
            OpacityAniStackedWidget()
        tab_layout.addWidget(self._stacked_area)

    def _create_command_bar_actions(self) -> list[Action]:
        actions: list = list()

        add_new = Action(FIF.ADD, _("MainWindow.Courses.CommandBar.AddNew"))
        add_new.triggered.connect(self._CB_add_new)
        actions.append(add_new)

        delete_puclass = Action(FIF.DELETE, _("MainWindow.Courses.CommandBar.Delete"))
        delete_puclass.triggered.connect(self._CB_del)
        actions.append(delete_puclass)

        edit_puclass = Action(FIF.EDIT, _("MainWindow.Courses.CommandBar.Edit"))
        edit_puclass.triggered.connect(self._CB_edit)
        actions.append(edit_puclass)

        set_scale = Action(FIF.IOT, _("MainWindow.Courses.CommandBar.Scale"))
        set_scale.triggered.connect(self._CB_scale)
        actions.append(set_scale)

        return actions
    
    def _CB_add_new(self) -> None:
        # Es mejor que sea una ventana propia
        self.new_class_dialog.show()

    def _CB_del(self) -> None:
        new = MessageDialog(
            _("MainWindow.Courses.SingleClassView.DeleteClassDialog.Title"),
            _("MainWindow.Courses.SingleClassView.DeleteClassDialog.Description"),
            self)
        new.accepted.connect(self.TR_delete_this_course)
        new.exec()

    def TR_delete_this_course(self) -> None:
        nrc = self._single_class_view._current_course_id
        self.SG_CoursesView_delete.emit(nrc)
        self.show_all_classes()

    def _CB_edit(self) -> None:
        pass

    def _CB_scale(self) -> None:
        pass

    def _create_layers(self) -> None:
        """
        Crea las capas del widget apilado
        La primera capa corresponde a información vacía cuando el usuario
        no tiene cursos agregados
        La segunda capa corresponde a la vista de todas las clases
        La tercera capa corresponde a información específica de una clase
        seleccionada
        """
        # Primera capa puede ser creada acá
        no_puclass_layer = QWidget()
        icon = QLabel()
        icon.setPixmap(QPixmap(pt.Resources.IMAGE_EMPTY_BOX))
        icon.setFixedSize(120, 120)
        icon.setScaledContents(True)
        subtitle = SubtitleLabel(_("MainWindow.Courses.NoClassView.NoClass"))
        layout = QVBoxLayout(no_puclass_layer)
        layout.addStretch()
        layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self._stacked_area.addWidget(no_puclass_layer)

        # Capa 2 
        self._all_classes_view: AllClassesView = AllClassesView()
        self._stacked_area.addWidget(self._all_classes_view)

        # Capa 3
        self._single_class_view: SingleClassView = SingleClassView()
        self._single_class_view.request_return.connect(self.show_all_classes)
        self._stacked_area.addWidget(self._single_class_view)

    def show_all_classes(self) -> None:
        self._stacked_area.setCurrentIndex(
            1 if self._all_classes_view.has_items else 0)
        cb: CommandBar = self.layout().itemAt(0).widget()
        cb.actions()[0].setEnabled(True)
        cb.actions()[1].setEnabled(False)
        cb.actions()[2].setEnabled(False)
        cb.actions()[3].setEnabled(False)

    def RQ_update_courses(self, courses_list: list[dict]) -> None:
        self._all_classes_view.clear()
        for course in courses_list:
            alias = course.get("user_alias")
            color = course.get("user_color")
            self._all_classes_view.add_class(alias, color, course)
        # ¿? Automáticamente mostrar segunda capa
        # -- weno pero usando su método para ajustar botones
        self.show_all_classes()
        # Al parecer tiene problemas si se pierde el foco
        self.setFocus()

    def RQ_show_SingleClassView(self, data: dict) -> None:
        self._single_class_view.load_data(data)
        self._stacked_area.setCurrentIndex(2)
        cb: CommandBar = self.layout().itemAt(0).widget()
        cb.actions()[0].setEnabled(False)
        cb.actions()[1].setEnabled(True)
        cb.actions()[2].setEnabled(True)
        cb.actions()[3].setEnabled(True)
        

class AllClassesView(QFrame, PukalendarWidget):
    SG_CoursesView_showSingleClass = pyqtSignal(NRC, name="SG_CoursesView_showSingleClass")

    def __init__(self) -> None:
        super().__init__(flags=Qt.WindowType.FramelessWindowHint)
        self._flow_container: FlowLayout = FlowLayout(self)

    def add_class(self, alias: str, color: str, data: dict={}) -> None:
        new_box: AllClassesClassBox = AllClassesClassBox()
        new_box.set_class_alias(alias)
        new_box.set_class_color(color)
        new_box.load_data(data)
        new_box.clicked.connect(
            lambda: self.SG_CoursesView_showSingleClass.emit(new_box.identifier))
        self._flow_container.addWidget(new_box)
    
    def read_container(self) -> bool:
        return bool(self._flow_container._items)
    
    has_items = property(read_container)

    def clear(self) -> None:
        self._flow_container.takeAllWidgets()

class SingleClassView(QFrame, PukalendarWidget):
    """
    Desplegamos las categorías
     - Información general
     - Horario
     - Calificaciones
     - Eventos / Tareas / Pendientes
    """
    request_return = pyqtSignal()
    SG_SingleClass_start_timer = pyqtSignal(NRC, name="SG_SingleClass_start_timer")
    SG_SingleClass_stop_timer = pyqtSignal(NRC, name="SG_SingleClass_stop_timer")

    def __init__(self) -> None:
        super().__init__(flags=Qt.WindowType.FramelessWindowHint)
        self._load_view()

    def _load_view(self) -> None:
        """
        <- [color] Nombre [color]
        --------------------------
              [general][horario]
              [calificaciones][eventos]
        """
        first_layout: QVBoxLayout = QVBoxLayout(self)
        top_layout: QHBoxLayout = QHBoxLayout()
        self._return_button: PrimaryToolButton = PrimaryToolButton(FIF.RETURN, self)
        self._return_button.clicked.connect(self.request_return.emit)
        self._left_stripe = QLabel()
        self._left_stripe.setFixedHeight(10)
        self._name_label = SubtitleLabel()
        self._right_stripe = QLabel()
        self._right_stripe.setFixedHeight(10)
        top_layout.addWidget(self._return_button)
        top_layout.addWidget(self._left_stripe, Qt.AlignmentFlag.AlignBottom)
        top_layout.addWidget(self._name_label)
        top_layout.addWidget(self._right_stripe, Qt.AlignmentFlag.AlignBottom)
        first_layout.addLayout(top_layout, 0)
        first_layout.addWidget(CardSeparator(), 0)

        bottom_layout: QGridLayout = QGridLayout()
        generic = self.__create_generic_box()
        self._schedule_cat_box: SingleClassCategoryBox = SingleClassCategoryBox(
            _("MainWindow.Courses.SingleClassView.Schedule"))
        self._grades_cat_box: SingleClassCategoryBox = SingleClassCategoryBox(
            _("MainWindow.Courses.SingleClassView.Grades"))
        events = self.__create_events_cat_box()
        bottom_layout.addWidget(generic, 0, 0)
        bottom_layout.addWidget(self._schedule_cat_box, 0, 1)
        bottom_layout.addWidget(self._grades_cat_box, 1, 0)
        bottom_layout.addWidget(events, 1, 1)
        first_layout.addLayout(bottom_layout, 1)

    def __create_events_cat_box(self) -> QWidget:
        self._events_cat_box: SingleClassCategoryBox = SingleClassCategoryBox(
            _("MainWindow.Courses.SingleClassView.Events"))
        self.start_timer_button = PushButton(FIF.PLAY, _("MainWindow.Courses.SingleClassView.ButtonStartTimer"))
        self.start_timer_button.clicked.connect(self.TR_start_timer_clicked)
        self.stop_timer_button = PushButton(FIF.PAUSE, _("MainWindow.Courses.SingleClassView.ButtonStopTimer"))
        self.stop_timer_button.clicked.connect(self.TR_stop_timer_clicked)
        how_much = SubtitleLabel()
        layout_general = QVBoxLayout()
        layout_general.addWidget(self.start_timer_button)
        layout_general.addWidget(self.stop_timer_button)
        layout_general.addWidget(how_much)
        self._events_cat_box.set_content_layout(layout_general)
        return self._events_cat_box

    def TR_start_timer_clicked(self) -> None:
        self.SG_SingleClass_start_timer.emit(self._current_course_id)
        self.start_timer_button.setEnabled(False)
        self.stop_timer_button.setEnabled(True)

    def TR_stop_timer_clicked(self) -> None:
        self.SG_SingleClass_stop_timer.emit(self._current_course_id)
        self.start_timer_button.setEnabled(True)
        self.stop_timer_button.setEnabled(False)


    def __create_generic_box(self) -> QWidget:
        if hasattr(self, "_generic_cat_box"): return None
        self._generic_cat_box: SingleClassCategoryBox = SingleClassCategoryBox(
            _("MainWindow.Courses.SingleClassView.General"))
        layout_general = QGridLayout()
        indicator_nrc = QLabel(
            _("MainWindow.Courses.SingleClassView.Indicator.NRC"))
        information_nrc = QLabel()
        indicator_code = QLabel(
            _("MainWindow.Courses.SingleClassView.Indicator.Code"))
        information_code = QLabel()
        indicator_professor = QLabel(
            _("MainWindow.Courses.SingleClassView.Indicator.Professor"))
        information_professor = QLabel()
        indicator_campus = QLabel(
            _("MainWindow.Courses.SingleClassView.Indicator.Campus"))
        information_campus = QLabel()
        indicator_section = QLabel(
            _("MainsWindow.Courses.SingleClassView.Indicator.Section"))
        information_section = QLabel()
        # De momento no es necesario parametrizar a este nivel
        layout_general.addWidget(indicator_nrc, 0, 0)
        layout_general.addWidget(information_nrc, 0, 1)
        layout_general.addWidget(indicator_code, 1, 0)
        layout_general.addWidget(information_code, 1, 1)
        layout_general.addWidget(indicator_professor, 2, 0)
        layout_general.addWidget(information_professor, 2, 1)
        layout_general.addWidget(indicator_campus, 3, 0)
        layout_general.addWidget(information_campus, 3, 1)
        layout_general.addWidget(indicator_section, 4, 0)
        layout_general.addWidget(information_section, 4, 1)
        self._generic_cat_box.set_content_layout(layout_general)
        return self._generic_cat_box

    def RQ_update_SingleClassView(self, course_dict: dict) -> None:
        self.load_data(course_dict)
        self.update()

    def load_data(self, course_data: dict) -> None:
        self._set_stripe_color(course_data.get("user_color"))
        self._name_label.setText(course_data.get("official_name"))
        self._current_course_id = course_data.get("official_nrc")
        log.debug(f"Course id:{self._current_course_id}")
        
        # Información general
        distr: QGridLayout = self._generic_cat_box.get_content_layout()
        distr.itemAtPosition(0, 1).widget().setText(
            str(course_data.get("official_nrc")))
        distr.itemAtPosition(1, 1).widget().setText(
            course_data.get("official_code"))
        distr.itemAtPosition(2, 1).widget().setText(
            course_data.get("official_professor"))
        distr.itemAtPosition(3, 1).widget().setText(
            course_data.get("official_campus"))
        distr.itemAtPosition(4, 1).widget().setText(
            course_data.get("official_section"))

        # Eventos
        distr: QVBoxLayout = self._events_cat_box.get_content_layout()
        # truchería para no ver los microsegundos
        cheating = timedelta(seconds=round(course_data.get("user_dedicated_time").total_seconds()))
        distr.itemAt(2).widget().setText(str(cheating))
        if course_data.get("course_on_session"):
            distr.itemAt(0).widget().setEnabled(False)
            distr.itemAt(1).widget().setEnabled(True)
        else:
            distr.itemAt(0).widget().setEnabled(True)
            distr.itemAt(1).widget().setEnabled(False)

    def _set_stripe_color(self, color: str) -> None:
        # Usar hexadecimal #xxxxxx
        self._left_stripe.setStyleSheet(f'QLabel {{background: {color};}}')
        self._right_stripe.setStyleSheet(f'QLabel {{background: {color};}}')